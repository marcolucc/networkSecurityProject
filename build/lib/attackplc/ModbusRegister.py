from typing import Optional, Callable

from attackplc.Context import Context
from attackplc.Register import Register
from attackplc.ModbusInterface import ModbusInterface


class ModbusRegister(Register):
    def __init__(self, ctx, interface: ModbusInterface, register_type: str, address: int) -> None:
        self._ctx = ctx
        self._interface = interface
        self._address = address
        self._register_type = register_type

    # wraps the callback and enqueue it to make the run on the main thread
    def make_callback(self, callback):
        def f(*args, **kwargs):
            def g():
                callback(*args, **kwargs)
            self._ctx.enqueue_callback(g)
        return f

    def read(self, timeout_ms=1000) -> Optional[int]:
        return self._interface.read(self._register_type, self._address)

    def read_async(self, callback: Callable[[int], None], timeout_ms=1000):
        return self._interface.read_async(self._register_type, self._address, self.make_callback(callback))

    def start_polling(self, interval_ms: int, callback: Callable[[int], None]) -> bool:
        self._interface.add_polling_register(self._register_type, self._address, self.make_callback(callback), interval_ms)

    def stop_polling(self):
        self._interface.remove_polling_register(self._register_type, self._address)

    def read_cache(self) -> Optional[int]:
        self._interface.read_cache(self._register_type, self._address)

    def write(self, value: int, timeout_ms=1000) -> Optional[int]:
        return self._interface.write(self._register_type, self._address, value)

    def write_async(self, value: int, callback: Callable[[int], None], timeout_ms=1000):
        return self._interface.write_async(self._register_type, self._address, value, self.make_callback(callback))
