from abc import ABC
from typing import Self

from core.logger import Logger

class InstanceProvider(ABC):
    _instance: 'InstanceProvider' = None
    _logger: Logger = Logger("InstanceProvider")

    def __init__(self) -> None:
        if InstanceProvider._instance is not None:
            raise RuntimeError("Singleton instance already instantiated!")
        
    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def create_instance(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = cls(*args, **kwargs)
            return cls._instance
        
        cls._logger.warn(f"Instance of {cls.__name__} already created, returning existing instance")
        return cls._instance