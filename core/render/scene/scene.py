import pygame

from core.interfaces.tickable import Tickable
from core.interfaces.renderable import Renderable
from core.interfaces.listener import EventListener

from core.entity.entity_manager import EntityManager

from core.physics.world import World

class Scene(Tickable, Renderable, EventListener):
    def __init__(self) -> None:
        EventListener.__init__(self)

        self.entity_manager: EntityManager = EntityManager()
        self.world: World = World(1920, 1080)

    def tick(self, deltatime: float) -> None:
        ...

    def render(self, surface: pygame.Surface, deltatime: float) -> None:
        ...