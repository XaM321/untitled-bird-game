from enum import Enum

class InputAction(Enum):
    KEYDOWN = "keydown"
    KEYUP = "keyup"
    MOUSEBUTTONDOWN = "mousebuttondown"
    MOUSEBUTTONUP = "mousebuttonup"
    MOUSEMOTION = "mousemotion"