import pygame

from core.entity.entity import Entity
from core.entity.sprite import Sprite, SpriteAnimation, SpriteTable
from core.input.keyboard.keyboard import Keyboard
from core.input.keyboard.key import Key
from core.direction import Direction

class Player(Entity):
    def __init__(self) -> None:
        sprites: SpriteTable = SpriteTable()
        sprites.add_sprite("bird_air_flap", Sprite(pygame.image.load("assets/flapping/airflaps1.png")))
        sprites.add_sprite("bird_mid_air", Sprite(pygame.image.load("assets/flapping/airflaps2.png")))
        sprites.add_sprite("bird_air", Sprite(pygame.image.load("assets/flapping/airflaps3.png")))
        sprites.add_sprite("bird_leg", Sprite(pygame.image.load("assets/bird_leg.png")))
        sprites.add_sprite("bird_still_flap", Sprite(pygame.image.load("assets/bird_still_flap.png")))
        sprites.add_sprite("bird_still", Sprite(pygame.image.load("assets/bird_still.png")))
        sprites.add_sprite("bird_swoop", Sprite(pygame.image.load("assets/bird_swoop2.png")))
        sprites.add_animation_sprites(SpriteAnimation("walking", [Sprite(pygame.image.load("assets/bird_standing.png")), Sprite(pygame.image.load("assets/bird_walk.png"))]))

        super().__init__(pygame.Vector2(0, 0), pygame.Vector2(0, 0), pygame.Vector2(50, 50), sprites, "bird_swoop")

        self._soaring: bool = False
        self._gravity: float = 9.81
        self._direction: Direction = Direction.LEFT
        self._flapping: bool = False
        self._flap_timer: float = 0.0
        self._start_flapping_timer: float = 0.0
        self._end_flapping_timer: float = 0.0
        self._last_swooping_rotation: float = 0.0
        self._time_since_last_step: float = 0.0

        self.rot = 0

    def is_on_ground(self) -> bool:
        return self.position.y >= 1080 - self.size.y
    
    def distance_from_ground(self) -> float:
        return 1080 - self.position.y - self.size.y
    
    def get_maximum_horizontal_velocity(self) -> float:
        return 300.0 if self.is_on_ground() else 600.0
    
    def update_direction(self) -> None:
        if self.velocity.x < 0:
            self._direction = Direction.LEFT
        elif self.velocity.x > 0:
            self._direction = Direction.RIGHT

    def check_movement_inputs(self) -> None:
        if Keyboard.get_pressed(Key.KEY_A):
            self.velocity.x -= 10
        elif Keyboard.get_pressed(Key.KEY_D):
            self.velocity.x += 10
        else:
            if not self.is_on_ground():
                self.velocity.x *= 0.98
            else:
                self.velocity.x *= 0.9

            if abs(self.velocity.x) < 1:
                self.velocity.x = 0

        if Keyboard.get_pressed(Key.KEY_W) and not self._flapping:
            self.velocity.y -= 30 if not self.is_on_ground() else 120

    def find_swooping_rotation(self) -> float:
        rotation_ratio = lambda velocity: -(velocity ** 2) + 1
        velocity_ratio: float = self.velocity.x / self.get_maximum_horizontal_velocity()
        rotation: float = -rotation_ratio(velocity_ratio) * 30 # 30 degrees maximum rotation

        return rotation
    
    def find_swooping_into_flapping_rotation(self) -> float:
        rotation_ratio = lambda velocity: -(velocity ** 2) + 1
        time_ratio: float = self._start_flapping_timer / 0.25
        rotation: float = rotation_ratio(time_ratio) * (30 - abs(self._last_swooping_rotation))
        needed_rotation: float = 30 - abs(rotation - self._last_swooping_rotation)

        return -(abs(self._last_swooping_rotation) + needed_rotation)
    
    def find_flapping_into_swooping_rotation(self) -> float:
        rotation_ratio = lambda velocity: -(velocity ** 2) + 1
        time_ratio: float = self._end_flapping_timer / 0.35
        rotation: float = rotation_ratio(time_ratio) * (30 - abs(self._last_swooping_rotation))
        needed_rotation: float = abs(rotation - self._last_swooping_rotation)

        return -(abs(self._last_swooping_rotation) + needed_rotation)
    
    def update_sprite(self) -> None:
        self.set_sprite_rotation(0.0)

        if self.velocity.x < 0:
            self._direction = Direction.LEFT
            self.set_sprite_direction(self._direction)
        elif self.velocity.x > 0:
            self._direction = Direction.RIGHT
            self.set_sprite_direction(self._direction)

        if self.is_on_ground():
            if self._time_since_last_step > 0.2:
                self._time_since_last_step = 0.0
                self.cycle_animation_sprite("walking")

            self.set_sprite("walking")
        else:
            if abs(self.velocity.x) < 50:
                if self._flapping and Keyboard.get_pressed(Key.KEY_W):
                    self.set_sprite("bird_still_flap")
                else:
                    self.set_sprite("bird_still")
            else:
                if self.distance_from_ground() <= 35:
                    if Keyboard.get_pressed(Key.KEY_W):
                        self.set_sprite("bird_air_flap")
                    else:
                        self.set_sprite("bird_air")
                else:
                    if Keyboard.get_pressed(Key.KEY_W):
                        if self._start_flapping_timer > 0.25:
                            if self._flapping:
                                self.set_sprite("bird_air_flap")
                            else:
                                self.set_sprite("bird_air")
                        else:
                            self.set_sprite_rotation(self.find_swooping_into_flapping_rotation())
                            self.set_sprite("bird_swoop")
                    else:
                        if self._end_flapping_timer > 0.35:
                            self.set_sprite_rotation(self.find_swooping_rotation())
                            self.set_sprite("bird_swoop")
                        else:
                            self.set_sprite_rotation(self.find_flapping_into_swooping_rotation())
                            self.set_sprite("bird_swoop")

    def tick(self, deltatime: float) -> None:
        super().tick(deltatime)
        self.update_direction()

        if self.is_on_ground():
            self.position.y = 1080 - self.size.y
            self.velocity.y = 0
        else:
            self.velocity.y += self._gravity

        if not self.is_on_ground() and not Keyboard.get_pressed(Key.KEY_W) and abs(self.velocity.x) > 100 and self.velocity.y > 0:
            self._soaring = True
            self._gravity = 1.0
        else:
            self._soaring = False
            self._gravity = 9.81

        if self._soaring:
            self.velocity.y -= self.velocity.y * 1.6 * deltatime
            if self._direction == Direction.RIGHT:
                self.velocity.x += self.velocity.y * 1.6 * deltatime
            elif self._direction == Direction.LEFT:
                self.velocity.x -= self.velocity.y * 1.6 * deltatime

        self.check_movement_inputs()
        self.velocity.x = max(min(self.get_maximum_horizontal_velocity(), self.velocity.x), -self.get_maximum_horizontal_velocity())
        self.velocity.y = max(-200, self.velocity.y)

        if self._flap_timer > 0.1:
            self._flapping = not self._flapping
            self._flap_timer = 0.0

        if self.is_on_ground() and abs(self.velocity.x) > 1:
            self._time_since_last_step += deltatime
        elif self.is_on_ground():
            if isinstance(self.current_sprite, SpriteAnimation):
                if self.current_sprite.name == "walking":
                    self.current_sprite.index = 0

        self.update_sprite()

        self._flap_timer += deltatime

        if Keyboard.get_pressed(Key.KEY_W):
            self._start_flapping_timer += deltatime
            self._end_flapping_timer = 0.0
        else:
            self._last_swooping_rotation = self.find_swooping_rotation()
            self._start_flapping_timer = 0.0
            self._end_flapping_timer += deltatime