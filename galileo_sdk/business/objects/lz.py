import enum

from ...business.objects.event import EventEmitter


class ELzStatus(enum.Enum):
    offline = 0  # machine is offline as an LZ
    online = 1  # machine is online as an LZ
    default = offline


class Lz:
    def __init__(
        self,
        name,
        user_id,
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
        """
        Landing Zone Object

        :param name: Optional[List[str]]: Human readable name name of the Landing Zone
        :param user_id: Optional[List[str]]: User ID the LZ belongs to
        :param status: Optional[List[str]]: Status of the Landing Zone (i.e. online or offline)
        :param lz_id: Optional[int]: UUID of the Landing Zone
        :param gpu_count: Optional[int]: Number of GPUs the LZ has
        :param cpu_count: Optional[List[str]]: Number of CPUs the LZ has
        :param operating_system: Optional[bool]: Operating system used by host (i.e. Windows or Linux)
        :param arch: Chipset architecture of the container runtime (i.e. x86, Arm7, etc.)
        :param memory_amount: Amount of memory available on the LZ
        :param memory: Amount of memory available on the LZ
        :param job_runner: Used internally
        :param container_technology: Runtime technology(i.e. Slurm, Singularity, Docker)
        """
        self.lz_id = lz_id
        self.name = name
        self.userid = user_id
        self.status = status
        self.gpu_count = gpu_count
        self.cpu_count = cpu_count
        self.operating_system = operating_system
        self.job_runner = job_runner
        self.arch = arch
        self.memory = memory
        self.memory_amount = memory_amount
        self.container_technology = container_technology

    def __str__(self):
        operating_system_str = "Windows" if self.operating_system else "Linux"
        return "{operating_system} LZ: {name}".format(
            operating_system=operating_system_str, name=self.name)

    def __repr__(self):
        return str(self)


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


class UpdateLzRequest:
    """Class representing a request to update a Landing Zone
    """
    def __init__(
        self,
        lz_id,
        name=None,
        active=None,
    ):
        """
        :param lz_id: UUID of the LZ to update
        :type lz_id: str
        :param name: Updated name, defaults to None
        :type name: str, optional
        :param active: Set the LZ to be active or inactive, defaults to None
        :type active: bool, optional
        """
        self.lz_id = lz_id
        self.name = name
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
