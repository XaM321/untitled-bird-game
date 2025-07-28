import pygame

from core.event.bus import EventBus
from core.event.events import EngineEvent
from core.interfaces.listener import EventListener

class Mouse(EventListener):
    _position: pygame.Vector2 = pygame.Vector2(0, 0)
    _buttons: dict[int, bool] = {}

    @staticmethod
    def init() -> None:
        EventBus.subscribe(EngineEvent.MOUSEBUTTONDOWN, lambda button: Mouse._set_pressed(button, True))
        EventBus.subscribe(EngineEvent.MOUSEBUTTONUP, lambda button: Mouse._set_pressed(button, False))
        EventBus.subscribe(EngineEvent.MOUSEMOTION, lambda old_position, new_position, relative_position, buttons: Mouse._set_position(new_position))

    @staticmethod
    def get_position() -> pygame.Vector2:
        return Mouse._position
    
    @staticmethod
    def get_x() -> pygame.Vector2:
        return Mouse._position.x
    
    @staticmethod
    def get_y() -> pygame.Vector2:
        return Mouse._position.y
    
    @staticmethod
    def _set_position(position: pygame.Vector2) -> None:
        Mouse._position = position

    @staticmethod
    def _set_x(x: int) -> None:
        Mouse._position.x = x

    @staticmethod
    def _set_y(y: int) -> None:
        Mouse._position.y = y
    
    @staticmethod
    def get_pressed(button: int) -> bool:
        return Mouse._buttons[button]
    
    @staticmethod
    def _set_pressed(button: int, pressed: bool) -> None:
        Mouse._buttons[button] = pressed