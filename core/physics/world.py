import pygame

from core.logger import Logger
from core.interfaces.tickable import Tickable
from core.interfaces.renderable import Renderable
from core.interfaces.listener import EventListener

from Box2D import b2World, b2PolygonShape, b2BodyDef, b2Body
from typing import Final, overload

PPM: Final[int | float] = 20
PHYSICS_STEP: Final[float] = 1 / 60
VEL_ITERS: Final[int] = 6
POS_ITERS: Final[int] = 2

class World(b2World, Tickable, Renderable):
    def __init__(self, width: int, height: int, gravity: float = -9.8) -> None:
        super().__init__((0, gravity), doSleep = True)
        EventListener.__init__(self)

        self._logger: Logger = Logger("World")
        self._gravity: float = gravity
        self._width: int = width
        self._height: int = height
        self._ground_body: b2BodyDef = self._create_ground_body()
        self._bodies: list[b2Body] = [self.create_dynamic_body((200, 0), 40, 40), self.create_dynamic_body((210, 100), 40, 40), self.create_dynamic_body((600, 0), 40, 40)]

        # for body in bodies
        # .render() if body instanceof MyBodyClass
        # ^^^^^^ implementation

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def gravity(self) -> float:
        return self._gravity
    
    @property
    def width(self) -> int:
        return self._width
    
    @property
    def height(self) -> int:
        return self._height
    
    def pixels_to_metres(self, pixels: int) -> int | float:
        return pixels / PPM
    
    @overload
    def screen_to_world(self, position: pygame.Vector2) -> pygame.Vector2:
        ...

    @overload
    def screen_to_world(self, position: tuple[int, int]) -> tuple[int, int]:
        ...

    def screen_to_world(self, position: pygame.Vector2 | tuple[int, int]) -> pygame.Vector2 | tuple[int, int]:
        if isinstance(position, pygame.Vector2):
            return pygame.Vector2(self.pixels_to_metres(position.x), self.pixels_to_metres(self._height - position.y))
        elif isinstance(position, tuple):
            return (self.pixels_to_metres(position[0]), self.pixels_to_metres(self._height - position[1]))
        else:
            self.logger.warn(f"Invalid position type passed to {self}.screen_to_world(...)")
            return position
        
    @overload
    def world_to_screen(self, position: pygame.Vector2) -> pygame.Vector2:
        ...

    @overload
    def world_to_screen(self, position: tuple[int, int]) -> tuple[int, int]:
        ...

    def world_to_screen(self, position: pygame.Vector2 | tuple[int, int]) -> pygame.Vector2 | tuple[int, int]:
        if isinstance(position, pygame.Vector2):
            return pygame.Vector2(int(position.x * PPM), int(self._height - position.y * PPM))
        elif isinstance(position, tuple):
            return (int(position[0] * PPM), int(self._height - position[1] * PPM))
        else:
            self.logger.warn(f"Invalid position type passed to {self}.world_to_screen(...)")
            return position
    
    @overload
    def to_b2_position(self, position: pygame.Vector2, width: int, height: int) -> pygame.Vector2:
        ...

    @overload
    def to_b2_position(self, position: tuple[float, float], width: int, height: int) -> tuple[float, float]:
        ...

    def to_b2_position(self, position: pygame.Vector2 | tuple[float, float], width: int, height: int) -> pygame.Vector2 | tuple[float, float]:
        if isinstance(position, pygame.Vector2):
            return self.screen_to_world(pygame.Vector2(position.x + width / 2, position.y + height / 2))
        elif isinstance(position, tuple):
            return self.screen_to_world((position[0] + width / 2, position[1] + height / 2))
        else:
            self.logger.warn(f"Invalid position type passed to {self}.to_b2_position(...)")
            return position
        
    @overload
    def from_b2_position(self, position: pygame.Vector2, width: int, height: int) -> pygame.Vector2:
        ...

    @overload
    def from_b2_position(self, position: tuple[float, float], width: int, height: int) -> tuple[float, float]:
        ...

    def from_b2_position(self, position: pygame.Vector2 | tuple[float, float], width: int, height: int) -> pygame.Vector2 | tuple[float, float]:
        if isinstance(position, pygame.Vector2):
            return self.screen_to_world(pygame.Vector2(position.x - width / 2, position.y - height / 2))
        elif isinstance(position, tuple):
            return self.screen_to_world((position[0] - width / 2, position[1] - height / 2))
        else:
            self.logger.warn(f"Invalid position type passed to {self}.from_b2_position(...)")
            return position
    
    def _create_ground_body(self) -> b2BodyDef:
        ground_height: int = 10
        ground_height_metres: float = self.pixels_to_metres(ground_height)
        ground: b2BodyDef = self.CreateStaticBody(
            position = self.to_b2_position((0, self._height ), self._width, ground_height),
            shapes = b2PolygonShape(box = (self.pixels_to_metres(self._width / 2), ground_height_metres))
        )

        for fixture in ground.fixtures:
            fixture.restitution = 0.05

        return ground
    
    @overload
    def create_dynamic_body(self, position: pygame.Vector2, width: int, height: int, *, density: float = 1.0, friction: float = 0.3, restitution: float = 0.5) -> b2Body:
        ...

    @overload
    def create_dynamic_body(self, position: tuple[int, int], width: int, height: int, *, density: float = 1.0, friction: float = 0.3, restitution: float = 0.5) -> b2Body:
        ...

    def create_dynamic_body(self, position: pygame.Vector2 | tuple[int, int], width: int, height: int, *, density: float = 1.0, friction: float = 0.3, restitution: float = 0.5) -> b2Body:
        body: b2Body = self.CreateDynamicBody(position = self.to_b2_position(position, width, height))
        body.CreatePolygonFixture(
            box = (self.pixels_to_metres(width / 2), self.pixels_to_metres(height / 2)),
            density = density,
            friction = friction,
            restitution = restitution
        )

        return body
    
    @overload
    def create_kinematic_body(self, position: pygame.Vector2, width: int, height: int) -> b2Body:
        ...

    @overload
    def create_kinematic_body(self, position: tuple[int, int], width: int, height: int) -> b2Body:
        ...

    def create_kinematic_body(self, position: pygame.Vector2 | tuple[int, int], width: int, height: int) -> b2Body:
        body: b2Body = self.CreateKinematicBody(position = self.to_b2_position(position, width, height))
        body.CreatePolygonFixture(
            box = (self.pixels_to_metres(width / 2), self.pixels_to_metres(height / 2)),
            density = 1
        )

        return body
    
    def tick(self, deltatime: float) -> None:
        self.Step(PHYSICS_STEP, VEL_ITERS, POS_ITERS)

    def render(self, surface: pygame.Surface, deltatime: float) -> None:
        ground_vertices = [(self._ground_body.transform * v) * PPM for v in self._ground_body.fixtures[0].shape.vertices]
        ground_vertices = [(v[0], self._height - v[1]) for v in ground_vertices]
        pygame.draw.polygon(surface, (255, 50, 50), ground_vertices)

        for body in self._bodies:
            vertices = [(body.transform * vertex) * PPM for vertex in body.fixtures[0].shape.vertices]
            vertices = [(v[0], self._height - v[1]) for v in vertices]

            pygame.draw.polygon(surface, (255, 255, 255), vertices)