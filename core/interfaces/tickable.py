from abc import ABC, abstractmethod

from core.event.bus import EventBus
from core.event.events import EngineEvent

class Tickable(ABC):
    def __init__(self) -> None:
        EventBus.subscribe(EngineEvent.TICK, self.tick)

    @abstractmethod
    def tick(self, deltatime: float) -> None:
        ...