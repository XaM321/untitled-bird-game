import pygame

from core.engine import Engine
from core.input.keyboard.keyboard import Keyboard
from core.input.keyboard.key import Key
from core.render.scene.scene import Scene

from player import Player

from Box2D import b2Body

class Game(Engine):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption("Bird Game")

        self.player: Player = Player()
        self.scene: Scene = Scene()
        self.player_body: b2Body = self.scene.world.create_dynamic_body(self.player.position, self.player.size.x, self.player.size.y)

    def tick(self, deltatime: float) -> None:
        if Keyboard.get_pressed(Key.KEY_ESCAPE):
            self.stop()

        self.player_body.position = self.scene.world.to_b2_position(self.player.position, self.player.size.x, self.player.size.y)

    def render(self, surface: pygame.Surface, deltatime: float) -> None:
        surface.fill((0, 0, 0))

        # ground_vertices = [(self.player_body.transform * v) * 20 for v in self.player_body.fixtures[0].shape.vertices]
        # ground_vertices = [(v[0], 1080 - v[1]) for v in ground_vertices]
        # pygame.draw.polygon(surface, (0, 50, 50), ground_vertices)

if __name__ == "__main__":
    game = Game()
    game.start()