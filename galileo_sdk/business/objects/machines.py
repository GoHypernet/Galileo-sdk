import enum
from typing import Callable, Optional

from ...business.objects.event import EventEmitter


class EMachineStatus(enum.Enum):
    offline = 0  # machine is offline as an LZ
    online = 1  # machine is online as an LZ
    default = offline


class Machine:
    def __init__(
        self,
        name: str,
        userid: str,
        status: EMachineStatus,
        gpu: str,
        cpu: str,
        os: str,
        arch: str,
        memory: str,
        jobs_in_queue: int = 0,
        running_jobs_limit: int = 1,
        running_jobs: int = 0,
        mid: Optional[str] = None,
    ):
        # Defaults
        self.mid = mid
        self.name = name
        self.userid = userid
        self.status = status
        self.gpu = gpu
        self.cpu = cpu
        self.os = os
        self.arch = arch
        self.memory = memory
        self.jobs_in_queue = jobs_in_queue
        self.running_jobs_limit = running_jobs_limit
        self.running_jobs = running_jobs


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
