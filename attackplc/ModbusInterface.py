import math
import time
import logging

from typing import Callable, Dict, Tuple, List, Optional
from threading import Event, Thread
from dataclasses import dataclass

from modbus_tk import modbus_tcp, defines

from attackplc.Register import Register

log = logging.getLogger(__name__)


@dataclass
class PollInfo:
    callback: Callable[[int], None]
    poll_interval_ms: int
    last_poll_time_ms: int


class ModbusInterface:
    def __init__(self, host: str, port: int, slave_address=1, timeout_seconds=5):
        self._slave_address = slave_address
        self._interface = modbus_tcp.TcpMaster(host, port, timeout_seconds)
        self._cache: Dict[Tuple[str, int], int] = {}
        self._poll_list: Dict[Tuple[str, int], PollInfo] = {}
        self._wait_event: Optional[Event] = None
        self._stop_event: Optional[Event] = None
        self._thread: Optional[Thread] = None

    def connect(self):
        return
        #self._interface.open()

    def _run_sync(self, function_code: int, address, params=None):
        return self._interface.execute(self._slave_address, function_code, address, 1, params)

    def _run_async(self, function_code: int, callback, params=None):
        raise NotImplementedError()

    def _get_read_function_code(self, register_type: str):
        if register_type == Register.REGISTER_TYPE_INPUT_REGISTER:
            return defines.READ_INPUT_REGISTERS
        if register_type == Register.REGISTER_TYPE_HOLDING_REGISTER:
            return defines.READ_HOLDING_REGISTERS
        if register_type == Register.REGISTER_TYPE_DISCRETE_INPUT:
            return defines.READ_DISCRETE_INPUTS
        if register_type == Register.REGISTER_TYPE_COIL:
            return defines.READ_COILS
        raise ValueError('unknown register type')

    def _get_write_function_code(self, register_type: str):
        if register_type == Register.REGISTER_TYPE_INPUT_REGISTER:
            raise RuntimeError('input register is not writable')
        if register_type == Register.REGISTER_TYPE_HOLDING_REGISTER:
            return defines.WRITE_SINGLE_REGISTER
        if register_type == Register.REGISTER_TYPE_DISCRETE_INPUT:
            raise RuntimeError('discrete input is not writable')
        if register_type == Register.REGISTER_TYPE_COIL:
            return defines.WRITE_SINGLE_COIL
        raise ValueError('unknown register type')

    def read(self, register_type: str, address: int):
        log.debug(f'read register {register_type}{address}')

        function_code = self._get_read_function_code(register_type)

        result = self._run_sync(function_code, address)
        if not result:
            log.warn(f'read error {result}')
            return None

        value = result[0]

        self._cache_write(register_type, address, value)

        return value

    def write(self, register_type: str, address: int, value: int):
        log.debug(f'write {value} to register {register_type}{address}')

        function_code = self._get_write_function_code(register_type)

        result = self._run_sync(function_code, address, value)
        log.debug(f'write result {result}')

        self._cache_write(register_type, address, value)

    def read_async(self, register_type: str, address: int, callback):
        log.debug(f'read async register {register_type}{address}')

        function_code = self._get_read_function_code(register_type)

        self._run_async(function_code, address, callback)

    def write_async(self, register_type: str, address: int, value, callback):
        log.debug(f'write async {value} to register {register_type}{address}')

        function_code = self._get_write_function_code(register_type)

        self._run_async(function_code, address, value, callback)

    def _cache_write(self, register_type: str, address: int, value: int):
        log.debug(f'update cache for {register_type}{address} to {value}')

        self._cache[(register_type, address)] = value

    def read_cache(self, register_type: str, address: int):
        log.debug(f'reading register {register_type}{address} from cache')

        return self._cache.get((register_type, address))

    def add_polling_register(self, register_type, address, callback, interval_ms):
        log.info(f'start polling register {register_type}{address} every {interval_ms}ms')

        self._stop_thread()
        self._poll_list[(register_type, address)] = PollInfo(callback, interval_ms, 0)
        self._start_thread()

    def remove_polling_register(self, register_type, address):
        log.info(f'stop polling register {register_type}{address}')

        self._stop_thread()
        del self._poll_list[(register_type, address)]

        if len(self._poll_list):
            # no more polling registers, stop polling thread
            self._start_thread()

    def _start_thread(self):
        log.debug('start poll thread')
        if not self._thread:
            self._stop_event = Event()
            self._thread = Thread(target=lambda: self._poll_thread(), name=f'poller thread')
            self._thread.start()

        if self._wait_event:
            self._wait_event.set()

    def _stop_thread(self):
        log.debug('stop poll thread')
        if not self._thread:
            return

        self._stop_event.set()
        self._thread.join()
        self._thread = None

        log.info('thread exited')

    def _poll_thread(self):
        log.debug('poll thread entry')

        while True:
            log.debug('evaluate poll cycle')

            next_poll_time_ms = 2**64
            for key, value in self._poll_list.items():
                current_time_ms = math.floor(time.time() * 1000)

                next_poll_ms = value.last_poll_time_ms + value.poll_interval_ms
                if next_poll_ms <= current_time_ms:
                    self._poll_register(key, value)

                    current_time_ms = math.floor(time.time() * 1000)
                    value.last_poll_time_ms = current_time_ms
                    next_poll_ms = current_time_ms + value.poll_interval_ms

                next_poll_time_ms = min(next_poll_time_ms, next_poll_ms)

            current_time_ms = math.floor(time.time() * 1000)
            ms_to_wait = next_poll_time_ms - current_time_ms

            log.debug(f'next poll cycle in {ms_to_wait}ms')
            if ms_to_wait > 0:
                self._wait_event = Event()
                self._wait_event.wait(ms_to_wait / 1000)
                self._wait_event = None

            if self._stop_event.is_set():
                return

    def _poll_register(self, key: Tuple[str, int], value: PollInfo):
        register_type, address = key
        log.debug(f'polling register {register_type}{address}')

        cached_value = self.read_cache(register_type, address)
        result = self.read(register_type, address)

        if result is not None and cached_value != result:
            value.callback(result)

    def stop(self):
        log.info('stopping interface')
        self._stop_thread()
        self._interface.close()
