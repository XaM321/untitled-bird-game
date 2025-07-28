from typing import overload

from core.event.bus import EventBus
from core.event.events import EngineEvent
from core.interfaces.listener import EventListener

from core.input.keyboard.key import Key

class Keyboard(EventListener):
    _keys: dict[int, bool] = {}

    @staticmethod
    def init() -> None:
        for name, value in vars(Key).items():
            if name.startswith("KEY_") and isinstance(value, int):
                Keyboard._keys[value] = False
                
        EventBus.subscribe(EngineEvent.KEYDOWN, lambda key: Keyboard._set_pressed(key, True))
        EventBus.subscribe(EngineEvent.KEYUP, lambda key: Keyboard._set_pressed(key, False))

    @overload
    @staticmethod
    def get_pressed(key: int) -> bool:
        ...

    @overload
    @staticmethod
    def get_pressed(key: Key) -> bool:
        ...
        
    def get_pressed(key: Key | int) -> bool:
        if isinstance(key, Key):
            return Keyboard._keys[key.code]
        elif isinstance(key, int):
            return Keyboard._keys[key]
        
    @staticmethod
    def _set_pressed(key: Key, pressed: bool) -> None:
        Keyboard._keys[key.code] = pressed