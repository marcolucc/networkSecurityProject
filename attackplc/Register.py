from abc import ABC, abstractmethod
from typing import Optional, Callable


class Register(ABC):
    REGISTER_TYPE_DISCRETE_INPUT = 'D'
    REGISTER_TYPE_COIL = 'C'
    REGISTER_TYPE_INPUT_REGISTER = 'I'
    REGISTER_TYPE_HOLDING_REGISTER = 'H'

    @abstractmethod
    def read(self, timeout_ms=1000) -> Optional[int]:
        '''
            read latest value (blocking)
            return None if read was not successful 
        '''

    @abstractmethod
    def read_async(self, callback: Callable[[int], None], timeout_ms=1000):
        '''
            read latest value (not blocking)
            callbaks gets the value, or None if the read was not sucessful
        '''

    @abstractmethod
    def start_polling(self, interval_ms: int, callback: Callable[[int], None]) -> bool:
        ''' 
            start polling and call function on value change
            return True if polling started correctly
        '''

    @abstractmethod
    def stop_polling(self):
        '''
            stop all polling (if no started don't do anything)
        '''

    @abstractmethod
    def read_cache(self) -> Optional[int]:
        '''
            read value form cache (return None if polling not started or no value available)
        '''

    @abstractmethod
    def write(self, value: int, timeout_ms=1000) -> Optional[int]:
        '''
            write new value to the register (blocking)
            NOTE: doesn't call the polling callback, but updates the cache
            return the written value in case of success, otherwise None
            throws ValueError if input value is out of range
        '''

    @abstractmethod
    def write_async(self, value: int, callback: Callable[[int], None], timeout_ms=1000):
        '''
            write new value to the regiser (async)
            NOTE: does't call the polling callback, but updates the cache
            callback return the written value in case of success, otherwise None
            throws ValueError if input vlaue is out of range
        '''
