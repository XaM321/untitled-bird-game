import pygame

from typing import overload

from core.entity.entity import Entity

from core.interfaces.tickable import Tickable
from core.interfaces.renderable import Renderable
from core.interfaces.listener import EventListener

class EntityManager(Tickable, Renderable, EventListener):
    def __init__(self) -> None:
        EventListener.__init__(self)
        self._entities: list[Entity] = []

    @property
    def entities(self) -> list[Entity]:
        return self._entities
    
    @overload
    def add(self, entity: Entity) -> None:
        ...

    @overload
    def add(self, entities: list[Entity]) -> None:
        ...

    @overload
    def add(self, *entities: Entity) -> None:
        ...

    def add(self, *entities: Entity | list[Entity]) -> None:
        if len(entities) == 1:
            if isinstance(entities[0], list):
                self.add(*entities[0])
            else:
                self._add_entity(entities[0])
        else:
            for entity in entities:
                self._add_entity(entity)

    def _add_entity(self, entity: Entity) -> None:
        if entity not in self._entities:
            self._entities.append(entity)

    def remove(self, entity: Entity) -> None:
        if entity in self._entities:
            self._entities.remove(entity)

    def tick(self, deltatime: float) -> None:
        ...

    def render(self, screen: pygame.Surface, deltatime: float) -> None:
        ...