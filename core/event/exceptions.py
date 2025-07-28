from typing import Any

class InvalidEventException(Exception):
    def __init__(self, event: Any) -> None:
        super().__init__(f"Expected type \"str\" but got type \"{type(event).__name__}\" instead")