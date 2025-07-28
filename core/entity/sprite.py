import pygame

from core.direction import Direction
from core.logger import Logger

class Sprite():
    def __init__(self, image: pygame.Surface, direction: Direction = Direction.LEFT, rotation: float = 0.0) -> None:
        self.image: pygame.Surface = image.convert_alpha()
        self._original_direction: Direction = direction
        self.direction: Direction = direction
        self.rotation: float = rotation

    def get_rendered_image(self) -> pygame.Surface:
        _image: pygame.Surface = self.image.copy()

        if self.rotation != 0.0:
            _image = pygame.transform.rotate(_image, self.rotation)
        
        if self._original_direction == Direction.LEFT:
            if self.direction != Direction.LEFT:
                _image = pygame.transform.flip(_image, True, False)
        elif self._original_direction == Direction.RIGHT:
            if self.direction != Direction.RIGHT:
                _image = pygame.transform.flip(_image, True, False)
            
        return _image
    
    def reset(self) -> None:
        self.direction = self._original_direction
        self.rotation = 0.0

class SpriteAnimation():
    def __init__(self, name: str, sprites: list[Sprite], rotation: float = 0.0, start_index: int = 0) -> None:
        self.name: str = name
        self.sprites: list[Sprite] = sprites
        self.rotation: float = rotation
        self.index: int = start_index

    def get_rendered_image(self) -> pygame.Surface:
        _image: pygame.Surface = self.sprites[self.index].image.copy()

        if self.rotation != 0.0:
            _image = pygame.transform.rotate(_image, self.rotation)
        
        if self.sprites[self.index]._original_direction == Direction.LEFT:
            if self.sprites[self.index].direction != Direction.LEFT:
                _image = pygame.transform.flip(_image, True, False)
        elif self.sprites[self.index]._original_direction == Direction.RIGHT:
            if self.sprites[self.index].direction != Direction.RIGHT:
                _image = pygame.transform.flip(_image, True, False)
        
        return _image

    def cycle(self) -> None:
        if self.index + 1 == len(self.sprites):
            self.index = 0
        else:
            self.index += 1

class SpriteTable():
    def __init__(self) -> None:
        self._sprites: dict[str, Sprite] = {}
        self._animation_sprites: dict[str, SpriteAnimation] = {}
        self.logger: Logger = Logger("SpriteTable")

    @property
    def sprites(self) -> dict[str, Sprite]:
        return self._sprites
    
    @sprites.setter
    def sprites(self, sprites: dict[str, Sprite]) -> None:
        self._sprites = sprites

    def add_sprite(self, name: str, sprite: Sprite) -> None:
        if name in self._sprites:
            self.logger.error(f"Sprite with name '{name}' already exists.")
            raise ValueError(f"Sprite with name '{name}' already exists.")
        
        self._sprites[name] = sprite

    def add_animation_sprites(self, sprite_animation: SpriteAnimation):
        if sprite_animation.name in self._animation_sprites:
            self.logger.error(f"Animation sprite with name '{sprite_animation.name}' already exists.")
            raise ValueError(f"Animation sprite with name '{sprite_animation.name}' already exists.")
        else:
            self._animation_sprites[sprite_animation.name] = sprite_animation

    def get_sprite(self, name: str, *, return_sprite_animation_instance: bool = False) -> Sprite:
        if name not in self._sprites:
            if name in self._animation_sprites:
                if return_sprite_animation_instance:
                    return self.get_animation_sprite(name)
                return self.get_animation_sprite_at_index(name, 0)
            
            self.logger.error(f"Sprite with name '{name}' does not exist.")
            raise KeyError(f"Sprite with name '{name}' does not exist.")
        
        return self._sprites[name]
    
    def get_animation_sprite(self, name: str) -> SpriteAnimation:
        if name not in self._animation_sprites:
            self.logger.error(f"Animation sprite with name '{name}' does not exist.")
            raise KeyError(f"Animation sprite with name '{name}' does not exist.")
        
        return self._animation_sprites[name]

    def get_animation_sprite_at_index(self, name: str, index: int) -> Sprite:
        if name not in self._animation_sprites:
            self.logger.error(f"Animation sprite with name '{name}' does not exist.")
            raise KeyError(f"Animation sprite with name '{name}' does not exist.")
        
        try:
            return self._animation_sprites[name].sprites[index]
        except IndexError as exception:
            self.logger.error(f"Index {index} out of bounds for animation sprite '{name}'")
            raise exception
    
    def set_movement_direction(self, direction: Direction) -> None:
        for sprite in self._sprites.values():
            sprite.direction = direction

        for animation in self._animation_sprites.values():
            for sprite in animation.sprites:
                sprite.direction = direction