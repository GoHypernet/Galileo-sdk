from ...business.objects.event import EventEmitter


class ProjectsEvents:
    _events: EventEmitter

    def __init__(self):
        self._events = EventEmitter()
