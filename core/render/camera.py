import pygame

from typing import Any, Tuple, overload

from core.interfaces.listener import EventListener
from core.interfaces.tickable import Tickable
from core.game_object import GameObject
from core.entity.entity import Entity

class Camera(Tickable, EventListener):
    def __init__(self, display: pygame.Surface) -> None:
        EventListener.__init__(self)

        self._display: pygame.Surface = display
        self._position: pygame.Vector2 = pygame.Vector2(0, 0)
        self._target: GameObject | None = None
        self._bounds: pygame.Rect | None = None
        self._zoom: float = 1.0

    def get_display_size(self) -> Tuple[int, int]:
        return self._display.get_size()
    
    def get_display_width(self) -> int:
        return self._display.get_width()

    def get_display_height(self) -> int:
        return self._display.get_height()
    
    @property
    def position(self) -> pygame.Vector2:
        return self._position
    
    @position.setter
    def position(self, position: pygame.Vector2) -> None:
        self._position = position

    @property
    def target(self) -> GameObject | None:
        return self._target
    
    @target.setter
    def target(self, target: GameObject) -> None:
        self._target = target

    @property
    def bounds(self) -> pygame.Rect | None:
        return self._bounds
    
    @bounds.setter
    def bounds(self, bounds: pygame.Rect) -> None:
        self._bounds = bounds

    @property
    def zoom(self) -> float:
        return self._zoom
    
    @zoom.setter
    def zoom(self, zoom: float) -> None:
        assert zoom > 0
        self._zoom = zoom

    def _clamp_to_bounds(self) -> None:
        if self.bounds is None:
            return
        
        display_width: int = self.get_display_width()
        display_height: int = self.get_display_height()

        clamped_x: float = max(self.bounds.left, min(self.position.x, self.bounds.right - display_width))
        clamped_y: float = max(self.bounds.top, min(self.position.y, self.bounds.bottom - display_height))

        self.position = pygame.Vector2(clamped_x, clamped_y)

    def tick(self, deltatime: float) -> None:
        if self.target is not None:
            if isinstance(self.target, Entity):
                target_x: float = self.target.position.x + self.target.size.x / 2 - self.get_display_width() / 2
                target_y: float = self.target.position.y + self.target.size.y / 2 - self.get_display_height() / 2
            else:
                target_x: float = self.target.position.x - self.get_display_width() / 2
                target_y: float = self.target.position.y - self.get_display_height() / 2

            self.position = pygame.Vector2(target_x, target_y)
        
        if self.bounds is not None:
            self._clamp_to_bounds()

    @overload
    def apply(self, obj: pygame.Rect) -> pygame.Rect:
        ...

    @overload
    def apply(self, obj: Tuple[float, float]) -> Tuple[int, int]:
        ...

    @overload
    def apply(self, obj: pygame.Vector2) -> pygame.Vector2:
        ...

    def apply(self, obj: pygame.Rect | Tuple[float, float] | pygame.Vector2) -> Any:
        if isinstance(obj, pygame.Rect):
            return pygame.Rect(
                (obj.left - self.position.x) * self.zoom,
                (obj.top - self.position.y) * self.zoom,
                obj.width * self.zoom,
                obj.height * self.zoom
            )
        elif isinstance(obj, (tuple, list)) and len(obj) == 2:
            return (
                int((obj[0] - self.position.x) * self.zoom),
                int((obj[1] - self.position.y) * self.zoom)
            )
        elif isinstance(obj, pygame.Vector2):
            return pygame.Vector2((obj - self.position) * self.zoom)
        else:
            raise TypeError(f"Unsupported type passed to Camera.apply(): {type(obj)}")