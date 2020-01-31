from typing import Callable

from ...business.objects.event import EventEmitter


class MachineStatusUpdateEvent:
    def __init__(self, mid: str, status: str):
        self.mid = mid
        self.status = status


class MachinesEvents:
    _events: EventEmitter

    def __init__(self):
        self._events = EventEmitter()

    def on_machine_status_update(
        self, func: Callable[[MachineStatusUpdateEvent], None]
    ):
        self._events.on("machine/status_updated", func)

    def machine_status_update(self, event: MachineStatusUpdateEvent):
        self._events.emit("machine/status_updated", event)
