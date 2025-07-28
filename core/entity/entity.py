import pygame

from core.game_object import GameObject
from core.interfaces.tickable import Tickable
from core.interfaces.renderable import Renderable
from core.interfaces.listener import EventListener

from core.entity.sprite import Sprite, SpriteTable, SpriteAnimation
from core.direction import Direction

class Entity(GameObject, Tickable, Renderable, EventListener):
    def __init__(self, position: pygame.Vector2 = pygame.Vector2(0, 0), velocity: pygame.Vector2 = pygame.Vector2(0, 0), size: pygame.Vector2 = pygame.Vector2(20, 20), sprite_table: SpriteTable | None = None, default_sprite: str | None = None) -> None:
        super().__init__(position)
        EventListener.__init__(self)

        self._velocity: pygame.Vector2 = velocity
        self._size: pygame.Vector2 = size
        self._sprite_table: SpriteTable | None = sprite_table
        self._default_sprite: str | None = default_sprite
        self._current_sprite: Sprite | SpriteAnimation | None = self._sprite_table.get_sprite(self._default_sprite) if self._sprite_table and self._default_sprite else None

    @property
    def velocity(self) -> pygame.Vector2:
        return self._velocity
    
    @velocity.setter
    def velocity(self, velocity: pygame.Vector2) -> None:
        self._velocity = velocity

    @property
    def size(self) -> pygame.Vector2:
        return self._size
    
    @size.setter
    def size(self, size: pygame.Vector2) -> None:
        self._size = size

    @property
    def current_sprite(self) -> Sprite | None:
        return self._current_sprite

    def get_collider_rect(self) -> pygame.Rect:
        return pygame.Rect(self._position, self._size)
    
    def _apply_velocity(self, deltatime: float) -> None:
        if self.velocity.length_squared() > 0:
            self._position += self._velocity * deltatime

    def set_sprite(self, name: str) -> None:
        if self._sprite_table is None:
            raise ValueError("Sprite table is not set for this entity.")
        
        sprite: Sprite | SpriteAnimation = self._sprite_table.get_sprite(name, return_sprite_animation_instance = True)
        self._current_sprite = sprite

    def reset_sprite(self) -> None:
        if self._current_sprite:
            self._current_sprite.reset()

    def set_sprite_rotation(self, rotation: float) -> None:
        if self._current_sprite:
            self._current_sprite.rotation = rotation

    def set_sprite_direction(self, direction: Direction) -> None:
        self._sprite_table.set_movement_direction(direction)

    def cycle_animation_sprite(self, name: str) -> None:
        sprite: SpriteAnimation = self._sprite_table.get_animation_sprite(name)
        sprite.cycle()

    def tick(self, deltatime: float) -> None:
        self._apply_velocity(deltatime)

    def render(self, screen: pygame.Surface, deltatime: float) -> None:
        if self._current_sprite:
            # mask: pygame.mask.Mask = pygame.mask.from_surface(self._current_sprite.get_rendered_image())
            # mask_surface: pygame.Surface = mask.to_surface()
            # Check rect collision first, then check mask collision

            screen.blit(self._current_sprite.get_rendered_image(), self._position)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.get_collider_rect())
            pygame.draw.rect(screen, (255, 255, 255,), self.get_collider_rect(), 1)