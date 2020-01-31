from collections import defaultdict
from typing import Callable, List


class EventEmitter:
    def __init__(self):
        self._registered_listeners = defaultdict(list)

    def on(self, event_name: str, handler: Callable):
        self._registered_listeners[event_name].append(handler)

    def emit(self, event_name: str, *args, **kwargs):
        handlers: List[Callable] = self._registered_listeners[event_name]
        for handler in handlers:
            handler(*args, **kwargs)
