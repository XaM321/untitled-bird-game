from typing import Type
from abc import ABC

from core.interfaces.tickable import Tickable
from core.interfaces.renderable import Renderable
from core.interfaces.keyboard import KeyboardListener
from core.interfaces.mouse import MouseListener

class EventListener(ABC):
    def __init__(self) -> None:
        _events: list[Type] = [Tickable, Renderable, KeyboardListener, MouseListener]

        for event in _events:
            if isinstance(self, event):
                event.__init__(self)