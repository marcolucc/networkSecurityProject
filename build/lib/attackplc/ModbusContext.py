import sys
import logging

from queue import Queue
from typing import Any, Dict, List
from threading import Event
from configparser import ConfigParser

from attackplc.ModbusInterface import ModbusInterface
from attackplc.Context import Context
from attackplc.ModbusRegister import ModbusRegister


class ModbusContext(Context):
    def __init__(self, config: ConfigParser, interfaces: Dict[str, ModbusInterface]):
        self._config = config
        self._interfaces = interfaces
        self._registers: List[ModbusRegister] = []
        self._msg_to_process = Event()
        self._stop = Event()
        self._stop_message = ''
        self._stop_code = 0
        self._queue = Queue()

    def register(self, plc_id: str, register_type: str, register_address: int) -> ModbusRegister:
        return ModbusRegister(self, self._interfaces[plc_id], register_type, register_address)

    def param(self, name: str, default=None) -> Any:
        return self._config.get('params', name, fallback=default)

    def stop(self, return_code=0, message=''):
        self._stop_code = return_code
        self._stop_message = message
        self._stop.set()

    def run(self):
        while not self._stop.is_set():
            self._msg_to_process.wait(1)
            self._msg_to_process.clear()

            while not self._queue.empty():
                callback = self._queue.get()
                callback()

        for interface in self._interfaces.values():
            interface.stop()

        logging.info('EXIT: %s %s', self._stop_code, self._stop_message)

        sys.exit(self._stop_code)

    def enqueue_callback(self, callback):
        self._queue.put(callback)
        self._msg_to_process.set()
