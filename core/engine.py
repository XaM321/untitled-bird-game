import pygame
import sys

from core.logger import Logger
from core.event.bus import EventBus
from core.event.events import EngineEvent
from core.input.action import InputAction
from core.input.keyboard.key import Key, Mods, KeyMod
from core.input.keyboard.keyboard import Keyboard
from core.input.mouse.mouse import Mouse
from core.input.mouse.button import MouseButton
from core.render.scene.scene_manager import SceneManager
from core.interfaces.listener import EventListener
from core.interfaces.tickable import Tickable
from core.interfaces.renderable import Renderable
from core.flags import Flags

class Engine(Tickable, Renderable, EventListener):
    def __init__(self, flags: int = 0b0) -> None:
        EventListener.__init__(self)

        self._version: str = "1.0.0"
        self._running: bool = False
        self.logger: Logger = Logger("Engine")
        self._flags: int = flags
        
        self.screen = pygame.display.set_mode((2560, 1440), pygame.DOUBLEBUF | pygame.NOFRAME, vsync = 1)
        self.display: pygame.Surface = pygame.Surface((1920, 1080))
        self.fps: int = 0
        self._deltatime: float = 0.0
        self._clock: pygame.time.Clock = pygame.time.Clock()

    @property
    def running(self) -> bool:
        return self._running
    
    @property
    def flags(self) -> int:
        return self._flags
    
    def init(self) -> None:
        Mouse.init()
        Keyboard.init()

        if not pygame.font.get_init():
            pygame.font.init()
        
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    
    def _tick(self, deltatime: float) -> None:
        EventBus.emit(EngineEvent.TICK, deltatime)

    def _render(self, surface: pygame.Surface, deltatime: float) -> None:
        EventBus.emit(EngineEvent.RENDER, surface, deltatime)
        self.screen.blit(pygame.transform.scale(surface, self.screen.get_size()), (0, 0))

    def _on_key_down(self, key: Key) -> None:
        EventBus.emit(EngineEvent.KEY, key, InputAction.KEYDOWN)
        EventBus.emit(EngineEvent.KEYDOWN, key)

    def _on_key_up(self, key: Key) -> None:
        EventBus.emit(EngineEvent.KEY, key, InputAction.KEYUP)
        EventBus.emit(EngineEvent.KEYUP, key)

    def _on_mouse_down(self, button: MouseButton) -> None:
        EventBus.emit(EngineEvent.MOUSE, button, InputAction.MOUSEBUTTONDOWN)
        EventBus.emit(EngineEvent.MOUSEBUTTONDOWN, button)

    def _on_mouse_up(self, button: MouseButton) -> None:
        EventBus.emit(EngineEvent.MOUSE, button, InputAction.MOUSEBUTTONUP)
        EventBus.emit(EngineEvent.MOUSEBUTTONUP, button)

    def _on_mouse_motion(self, old_position: pygame.Vector2, new_position: pygame.Vector2, relative_position: pygame.Vector2, buttons: list[int]) -> None:
        EventBus.emit(EngineEvent.MOUSE, old_position, new_position, relative_position, buttons, InputAction.MOUSEMOTION)
        EventBus.emit(EngineEvent.MOUSEMOTION, old_position, new_position, relative_position, buttons)

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                self._on_key_down(Key(event.key, event.scancode, event.unicode, Mods(event.mod)))
            elif event.type == pygame.KEYUP:
                self._on_key_up(Key(event.key, event.scancode, event.unicode, Mods(event.mod)))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._on_mouse_down(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._on_mouse_up(event.button)
            elif event.type == pygame.MOUSEMOTION:
                self._on_mouse_motion(Mouse.get_position(), pygame.Vector2(event.pos), pygame.Vector2(event.rel), event.buttons)
    
    def start(self) -> None:
        self.logger.info(f"Initialising engine v{self._version} | pygame-ce {pygame.version.ver} | SDL {'.'.join([str(_) for _ in pygame.get_sdl_version()])} | python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

        self._running = True

        self.init()
        self.scene_manager: SceneManager = SceneManager()

        EventBus.emit(EngineEvent.START)
        self._mainloop()

    def stop(self) -> None:
        self.logger.info("Engine stopping...")
        self._running = False

    def _mainloop(self) -> None:
        while self.running:
            self._handle_events()

            self._tick(self._deltatime)
            self._render(self.display, self._deltatime)

            pygame.display.flip()
            self._deltatime = self._clock.tick(self.fps) / 1000.0

        pygame.quit()