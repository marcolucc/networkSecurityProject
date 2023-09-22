from attackplc.Register import Register

from abc import ABC, abstractmethod
from typing import Any
from pymodbus.client import ModbusTcpClient
from time import sleep


class Context(ABC):
    STOP_SUCCESS = 0
    STOP_FAILURE = 1

    @abstractmethod
    def register(self, plc_id: str, register_type: str, register_address: int) -> Register:
        '''
            return an instance for a register
        '''

    @abstractmethod
    def param(self, name: str, default=None) -> Any:
        '''
            get a configuration param
            if not found, return the default value (default of the default is None)
        '''

    @abstractmethod
    def stop(self, return_code=0, message=''):
        '''
            stop a running attack and exit
            return code 0 means success, otherwise failure
        '''
