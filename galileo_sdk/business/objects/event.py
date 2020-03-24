from collections import defaultdict


class EventEmitter:
    def __init__(self):
        self._registered_listeners = defaultdict(list)

    def on(self, event_name, handler):
        self._registered_listeners[event_name].append(handler)

    def emit(self, event_name, *args, **kwargs):
        handlers = self._registered_listeners[event_name]
        for handler in handlers:
            handler(*args, **kwargs)
