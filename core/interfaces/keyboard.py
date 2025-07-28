from abc import ABC, abstractmethod

from core.input.keyboard.key import Key
from core.input.action import InputAction

from core.event.bus import EventBus
from core.event.events import EngineEvent

class KeyboardListener(ABC):
    def __init__(self) -> None:
        EventBus.subscribe(EngineEvent.KEY, self.on_key)
        EventBus.subscribe(EngineEvent.KEYDOWN, self.on_key_down)
        EventBus.subscribe(EngineEvent.KEYUP, self.on_key_up)

    @abstractmethod
    def on_key(self, key: Key, action: InputAction) -> None:
        ...

    @abstractmethod
    def on_key_down(self, key: Key) -> None:
        ...

    @abstractmethod
    def on_key_up(self, key: Key) -> None:
        ...