from typing import Callable, Any
from enum import Enum

from core.event.exceptions import InvalidEventException

_bus_subscribers: dict[str, list[dict]] = {}

class EventBus:
    @staticmethod
    def subscribe(event: Enum | str, callback: Callable, /, *, priority: int = 1) -> int | None:
        """Subscribes a method to an event."""
        result = EventBus.validate_event(event)
        if result is None:
            return 0
        
        if isinstance(event, Enum):
            event = event.value

        # instance = getattr(callback, "__self__", None)
        # if instance is None or not isinstance(instance, EventListener):
        #     raise TypeError(f"Method '{callback.__name__}' must belong to a subclass of EventListener")

        if event not in _bus_subscribers:
            _bus_subscribers[event] = []

        _bus_subscribers[event].append({"callback": callback, "priority": priority})
        _bus_subscribers[event].sort(key = lambda sub: sub["priority"], reverse = True)

    @staticmethod
    def unsubscribe(event: Enum | str, callback: Callable, /) -> int | None:
        """Unsubscribes a method from an event."""
        result = EventBus.validate_event(event)
        if result is None:
            return 0
        
        if isinstance(event, Enum):
            event = event.value

        if event in _bus_subscribers:
            _bus_subscribers[event] = [
                sub for sub in _bus_subscribers[event] if sub["callback"] != callback
            ]

    @staticmethod
    def emit(event: Enum | str, /, *args, **kwargs) -> int:
        """Calls an event with optional data, invoking subscribed callbacks."""
        result = EventBus.validate_event(event)
        if result is None:
            return 0
        
        if isinstance(event, Enum):
            event = event.value

        call_count = 0
        if event in _bus_subscribers:
            for subscriber in _bus_subscribers[event]:
                subscriber["callback"](*args, **kwargs)
                call_count += 1

        return call_count

    @staticmethod
    def validate_event(event: Any, /) -> int | None:
        """Validates that an event is an Enum or string."""
        if not isinstance(event, (Enum, str)):
            raise InvalidEventException(event)
        return 1

# class EventBusContextManager:
#     """Context-managed event subscription with auto-unsubscribe on exit."""

#     def __init__(self) -> None:
#         self.__bus_subscribers: dict[str, list[dict]] = {}

#     def on(self, event: Enum | str, /, *, priority: int = 1) -> Callable:
#         """Decorator to subscribe a method with enforced EventListener membership."""

#         if isinstance(event, Enum):
#             event = event.value
            
#         def wrapper(callback: Callable) -> Callable:
#             instance = getattr(callback, "__self__", None)
#             if instance is None or not isinstance(instance, EventListener):
#                 raise TypeError(f"Method '{callback.__name__}' must belong to a subclass of EventListener")

#             EventBus.subscribe(event, callback, priority = priority)
#             if event not in self.__bus_subscribers:
#                 self.__bus_subscribers[event] = []
#             self.__bus_subscribers[event].append({"callback": callback, "priority": priority})
#             return callback
#         return wrapper

#     def __enter__(self) -> 'EventBusContextManager':
#         return self

#     def __exit__(self, exc_type, exc_value, traceback) -> None:
#         for event, subscribers in self.__bus_subscribers.items():
#             for subscriber in subscribers:
#                 EventBus.unsubscribe(event, subscriber["callback"])
