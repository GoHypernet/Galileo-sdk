import enum

from ...business.objects.event import EventEmitter


class EMachineStatus(enum.Enum):
    offline = 0  # machine is offline as an LZ
    online = 1  # machine is online as an LZ
    default = offline


class Machine:
    def __init__(
        self, name, userid, status, mid, gpu, cpu, os, arch, memory, running_jobs_limit,
    ):
        self.mid = mid
        self.name = name
        self.userid = userid
        self.status = status
        self.gpu = gpu
        self.cpu = cpu
        self.os = os
        self.arch = arch
        self.memory = memory
        self.running_jobs_limit = running_jobs_limit


class MachineStatusUpdateEvent:
    def __init__(self, mid, status):
        self.mid = mid
        self.status = status


class MachineRegisteredEvent:
    def __init__(self, machine):
        self.machine = machine


class MachineHardwareUpdateEvent:
    def __init__(self, machine):
        self.machine = machine


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


class MachinesEvents:
    def __init__(self):
        self._events = EventEmitter()

    def on_machine_status_update(self, func):
        self._events.on("machine/status_updated", func)

    def machine_status_update(self, event):
        self._events.emit("machine/status_updated", event)

    def on_machine_registered(self, func):
        self._events.on("machine/registered", func)

    def machine_registered(self, event):
        self._events.emit("machine/registered", event)

    def on_machine_hardware_update(self, func):
        self._events.on("machine/hardware_updated", func)

    def machine_hardware_update(self, event):
        self._events.emit("machine/hardware_updated", event)
