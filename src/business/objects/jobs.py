import enum
from datetime import datetime
from typing import Callable, List, Optional

from ...business.objects.event import EventEmitter


class EJobStatus(enum.Enum):
    uploaded = 0  # job has been uploaded
    submitted = 1  # LZ has been or is cleared to download job
    downloaded = 2  # Job has been downloaded by LZ
    building_image = 3  # Building docker image
    building_container = 4  # Buiding docker container
    start_requested = 5  # Start
    running = 6
    pause_requested = 7
    paused = 8
    stop_requested = 9
    stopped = 10
    exited = 11
    collecting_results = 12
    posting_results = 13
    terminated = 14
    completed = 15
    removed_by_host = 16
    unknown = 17  # Just in case arbitrary update occurs
    post_processing = 18
    started = 19


class EJobRunningStatus(enum.Enum):
    not_running = 0  # job isn't running
    running = 1  # job is running


class EPaymentStatus(enum.Enum):
    current = 0  # all paid
    payment_due = 1  # Missing a payment
    delinquent = 2  # Delinquent on payments
    missing_offer = 3  # No valid offer found


class JobStatus:
    def __init__(
        self,
        timestamp: datetime,
        status: EJobStatus,
        jobstatusid: Optional[str] = None,
        jobid: Optional[str] = None,
    ):
        self.jobstatusid = jobstatusid
        self.jobid = jobid
        self.timestamp = timestamp
        self.status = status


class Job:
    """
    Details of a job
    """

    def __init__(
        self,
        userid: str,
        senderid: str,
        receiverid: str,
        time_created: datetime = datetime.now(),
        last_updated: datetime = datetime.now(),
        status: EJobStatus = EJobStatus.uploaded,
        container: str = "",
        name: str = "",
        stationid: Optional[str] = None,
        state: EJobRunningStatus = EJobRunningStatus.not_running,
        oaid: Optional[str] = None,
        pay_status: EPaymentStatus = EPaymentStatus.current,
        pay_interval: int = 0,
        total_runtime: int = 0,
        status_history: List[JobStatus] = [],
        jobid: Optional[str] = None,
    ):
        self.jobid = jobid
        self.senderid = senderid
        self.receiverid = receiverid
        self.time_created = time_created
        self.last_updated = last_updated
        self.status = status
        self.container = container
        self.name = name
        self.stationid = stationid
        self.userid = userid
        self.state = state
        self.oaid = oaid
        self.pay_status = pay_status
        self.pay_interval = pay_interval
        self.total_runtime = total_runtime
        self.status_history = status_history


class JobLauncherUpdatedEvent:
    def __init__(self, job: Job):
        self.job = job


class JobLauncherResultsDownloadedEvent:
    def __init__(self, resultsid: str, status: str):
        self.resultsid: str = resultsid
        self.status: str = status


class StationJobUpdatedEvent:
    def __init__(self, job: Job):
        self.job = job


class JobTopEvent:
    def __init__(self, job: Job, top):
        self.job = job
        self.top = top


class JobLogEvent:
    def __init__(self, job: Job, log):
        self.job = job
        self.log = log


class JobsEvents:
    _events: EventEmitter

    def __init__(self):
        self._events = EventEmitter()

    def on_job_launcher_updated(self, func: Callable[[JobLauncherUpdatedEvent], None]):
        self._events.on("job_launcher_updated", func)

    def job_launcher_updated(self, event: JobLauncherUpdatedEvent):
        self._events.emit("job_launcher_updated", event)

    def on_job_launcher_results_downloaded(
        self, func: Callable[[JobLauncherResultsDownloadedEvent], None]
    ):
        self._events.on("job_launcher_results_downloaded", func)

    def job_launcher_results_downloaded(self, event: JobLauncherResultsDownloadedEvent):
        self._events.emit("job_launcher_results_downloaded", event)

    def on_station_job_updated(self, func: Callable[[StationJobUpdatedEvent], None]):
        self._events.on("station_job_updated", func)

    def station_job_updated(self, event: StationJobUpdatedEvent):
        self._events.emit("station_job_updated", event)

    def on_job_top(self, func: Callable[[JobTopEvent], None]):
        self._events.on("top", func)

    def job_top(self, event: JobTopEvent):
        self._events.emit("top", event)

    def on_job_log(self, func: Callable[[JobLogEvent], None]):
        self._events.on("log", func)

    def job_log(self, event: JobLogEvent):
        self._events.emit("log", event)
