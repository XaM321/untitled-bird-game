import pygame

from abc import ABC, abstractmethod

from core.input.mouse.button import MouseButton
from core.input.action import InputAction

from core.event.bus import EventBus
from core.event.events import EngineEvent

class MouseListener(ABC):
    def __init__(self) -> None:
        EventBus.subscribe(EngineEvent.MOUSE, self.on_mouse_button)
        EventBus.subscribe(EngineEvent.MOUSEBUTTONDOWN, self.on_mouse_down)
        EventBus.subscribe(EngineEvent.MOUSEBUTTONUP, self.on_mouse_up)
        EventBus.subscribe(EngineEvent.MOUSEMOTION, self.on_mouse_motion)

    @abstractmethod
    def on_mouse_button(self, position: pygame.Vector2, button: MouseButton, action: InputAction) -> None:
        ...

    @abstractmethod
    def on_mouse_down(self, position: pygame.Vector2, button: MouseButton) -> None:
        ...

    @abstractmethod
    def on_mouse_up(self, position: pygame.Vector2, button: MouseButton) -> None:
        ...

    @abstractmethod
    def on_mouse_motion(self, old_position: pygame.Vector2, new_position: pygame.Vector2, relative_position: pygame.Vector2, buttons: list[int]) -> None:
        ...