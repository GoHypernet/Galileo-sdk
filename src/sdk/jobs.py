from typing import Callable, List, Optional

from ..business.objects.jobs import (JobLauncherResultsDownloadedEvent,
                                     JobLauncherUpdatedEvent, JobLogEvent,
                                     JobsEvents, JobTopEvent,
                                     StationJobUpdatedEvent)
from ..business.services.jobs import JobsService


class JobsSdk:
    _jobs_service: JobsService
    _events: JobsEvents

    def __init__(self, jobs_service: JobsService, events: JobsEvents):
        self._jobs_service = jobs_service
        self._events = events

    def on_job_launcher_updated(self, func: Callable[[JobLauncherUpdatedEvent], None]):
        self._events.on_job_launcher_updated(func)

    def on_job_launcher_results_downloaded(
        self, func: Callable[[JobLauncherResultsDownloadedEvent], None]
    ):
        self._events.on_job_launcher_results_downloaded(func)

    def on_station_job_updated(self, func: Callable[[StationJobUpdatedEvent], None]):
        self._events.on_station_job_updated(func)

    def on_job_top(self, func: Callable[[JobTopEvent], None]):
        self._events.on_job_top(func)

    def on_job_log(self, func: Callable[[JobLogEvent], None]):
        self._events.on_job_log(func)

    def request_send_job(self):
        return self._jobs_service.request_send_job()

    def request_send_job_completed(self, job_id: str):
        return self._jobs_service.request_send_job_completed(job_id)

    def request_receive_job(self, job_id: str):
        return self._jobs_service.request_receive_job(job_id)

    def submit_job(self, job_id: str):
        return self._jobs_service.submit_job(job_id)

    def request_stop_job(self, job_id: str):
        return self._jobs_service.request_stop_job(job_id)

    def request_pause_job(self, job_id: str):
        return self._jobs_service.request_pause_job(job_id)

    def request_top_from_job(self, job_id: str):
        return self._jobs_service.request_top_from_job(job_id)

    def request_logs_from_job(self, job_id: str):
        return self._jobs_service.request_logs_from_job(job_id)

    def list_jobs(
        self,
        jobids: Optional[List[str]] = None,
        receiverids: Optional[List[str]] = None,
        senderids: Optional[List[str]] = None,
        oaids: Optional[List[str]] = None,
        userids: Optional[List[str]] = None,
        stationids: Optional[List[str]] = None,
        statuses: Optional[List[str]] = None,
        page: Optional[int] = 1,
        items: Optional[int] = 25,
    ):
        return self._jobs_service.list_jobs(
            jobids=jobids,
            receiverids=receiverids,
            senderids=senderids,
            oaids=oaids,
            userids=userids,
            stationids=stationids,
            statuses=statuses,
            page=page,
            items=items,
        )
