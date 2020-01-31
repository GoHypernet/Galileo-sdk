from typing import Callable

from ...business.objects.event import EventEmitter


class JobLauncherUpdatedEvent:
    def __init__(self, job):
        # TODO: type Job
        self.job = job


class JobLauncherResultsDownloadedEvent:
    def __init__(self, resultsid: str, status: str):
        self.resultsid: str = resultsid
        self.status: str = status


class StationJobUpdatedEvent:
    def __init__(self, job):
        self.job = job


class JobTopEvent:
    def __init__(self, job, top):
        self.job = job
        self.top = top


class JobLogEvent:
    def __init__(self, job, log):
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
