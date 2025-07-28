import pygame

from core.render.scene.scene import Scene

from core.interfaces.tickable import Tickable
from core.interfaces.renderable import Renderable
from core.interfaces.listener import EventListener

class SceneManager(Tickable, Renderable, EventListener):
    def __init__(self) -> None:
        EventListener.__init__(self)
        self._scene_stack: list[Scene] = []

    def push(self, scene: Scene) -> None:
        self._scene_stack.append(scene)

    def pop(self) -> Scene | None:
        if self.current() is None:
            return None
        
        return self._scene_stack.pop(0)
    
    def current(self) -> Scene | None:
        if len(self._scene_stack) == 0:
            return None

        return self._scene_stack[0]
    
    def insert(self, scene: Scene, index: int) -> None:
        self._scene_stack.insert(index, scene)

    def tick(self, deltatime: float) -> None:
        if self.current() is None:
            return

        self.current().tick(deltatime)

    def render(self, surface: pygame.Surface, deltatime: float) -> None:
        if self.current() is None:
            return
        
        self.current().render(surface, deltatime)