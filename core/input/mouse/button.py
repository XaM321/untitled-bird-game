class MouseButton():
    BUTTON_LEFT: int = 0
    BUTTON_MIDDLE: int = 1
    BUTTON_RIGHT: int = 2

    def __init__(self, button: int) -> None:
        self._button: int = button

    def is_button(self, button: int) -> bool:
        return self._button == button

    @property
    def button(self) -> int:
        return self._button
    
    @classmethod
    def left(cls) -> 'MouseButton':
        return cls(MouseButton.BUTTON_LEFT)
    
    @classmethod
    def middle(cls) -> 'MouseButton':
        return cls(MouseButton.BUTTON_MIDDLE)
    
    @classmethod
    def right(cls) -> 'MouseButton':
        return cls(MouseButton.BUTTON_RIGHT)