import pygame

from core.entity.entity import Entity
from core.entity.sprite import SpriteTable

from typing import TYPE_CHECKING, override
from Box2D import b2Body

if TYPE_CHECKING:
    from core.physics.world import World

class PhysicsEntity(Entity):
    def __init__(self, world: 'World', position: pygame.Vector2 = pygame.Vector2(0, 0), size: pygame.Vector2 = pygame.Vector2(20, 20), sprite_table: SpriteTable | None = None, default_sprite: str | None = None) -> None:
        self._world: 'World' = world
        super().__init__(position, size, sprite_table, default_sprite)

        self._body: b2Body = self.world.create_dynamic_body(self.position, self.size.x, self.size.y, restitution = 0.1)
        self._body.fixedRotation = True

        self._velocity: pygame.Vector2 = pygame.Vector2(self._body.linearVelocity[0], self._body.linearVelocity[1])
        self._body.gravityScale = 0.5
        
    @property
    def world(self) -> 'World':
        return self._world
    
    @property
    def velocity(self) -> pygame.Vector2:
        return self._velocity
    
    def tick(self, deltatime: float) -> None:
        self._velocity = pygame.Vector2(self._body.linearVelocity[0], self._body.linearVelocity[1])
    
    @override
    def render(self, surface: pygame.Surface, deltatime: float) -> None:
        ...