import enum

from ...business.objects.event import EventEmitter


class EMachineStatus(enum.Enum):
    offline = 0  # machine is offline as an LZ
    online = 1  # machine is online as an LZ
    default = offline


class Lz:
    def __init__(
        self,
        name,
        userid,
        status,
        lz_id,
        gpu_count,
        cpu_count,
        operating_system,
        arch,
        memory_amount,
        memory,
        job_runner,
        container_technology,
    ):
        self.lz_id = lz_id
        self.name = name
        self.userid = userid
        self.status = status
        self.gpu_count = gpu_count
        self.cpu_count = cpu_count
        self.operating_system = operating_system
        self.job_runner = job_runner
        self.arch = arch
        self.memory = memory
        self.memory_amount = memory_amount
        self.container_technology = container_technology


class LzStatusUpdateEvent:
    def __init__(self, lz_id, status):
        self.lz_id = lz_id
        self.status = status


class LzRegisteredEvent:
    def __init__(self, lz):
        self.lz = lz


class LzHardwareUpdateEvent:
    def __init__(self, lz):
        self.lz = lz


class UpdateMachineRequest:
    def __init__(
        self,
        mid,
        name=None,
        gpu=None,
        cpu=None,
        os=None,
        arch=None,
        memory=None,
        running_jobs_limit=None,
        active=None,
    ):
        self.mid = mid
        self.name = name
        self.gpu = gpu
        self.cpu = cpu
        self.os = os
        self.arch = arch
        self.memory = memory
        self.running_jobs_limit = running_jobs_limit
        self.active = active


class LzEvents:
    def __init__(self):
        self._events = EventEmitter()

    def on_lz_status_update(self, func):
        self._events.on("machine/status_updated", func)

    def lz_status_update(self, event):
        self._events.emit("machine/status_updated", event)

    def on_lz_registered(self, func):
        self._events.on("machine/registered", func)

    def lz_registered(self, event):
        self._events.emit("machine/registered", event)

    def on_lz_hardware_update(self, func):
        self._events.on("machine/hardware_updated", func)

    def lz_hardware_update(self, event):
        self._events.emit("machine/hardware_updated", event)
