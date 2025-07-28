import pygame

class GameObject():
    def __init__(self, position: pygame.Vector2 = pygame.Vector2(0, 0)) -> None:
        self._position: pygame.Vector2 = position

    @property
    def position(self) -> pygame.Vector2:
        return self._position
    
    @position.setter
    def position(self, position: pygame.Vector2) -> None:
        self._position = position