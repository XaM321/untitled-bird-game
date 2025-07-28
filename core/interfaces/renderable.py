import pygame

from abc import ABC, abstractmethod

from core.event.bus import EventBus
from core.event.events import EngineEvent

class Renderable(ABC):
    def __init__(self) -> None:
        EventBus.subscribe(EngineEvent.RENDER, self.render)

    @abstractmethod
    def render(self, surface: pygame.Surface, deltatime: float) -> None:
        ...