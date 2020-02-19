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
        """
        Callback will execute upon a job launcher updated event

        :param func: Callback
        :return: None
        """
        self._events.on_job_launcher_updated(func)

    def on_job_launcher_results_downloaded(
        self, func: Callable[[JobLauncherResultsDownloadedEvent], None]
    ):
        """
        Callback will execute upon a job launcher results downloaded event

        :param func: Callback
        :return: None
        """
        self._events.on_job_launcher_results_downloaded(func)

    def on_station_job_updated(self, func: Callable[[StationJobUpdatedEvent], None]):
        """
        Callback will execute upon a station job updated event

        :param func: Callback
        :return: None
        """
        self._events.on_station_job_updated(func)

    def on_job_top(self, func: Callable[[JobTopEvent], None]):
        """
        Callback will execute upon a job top event

        :param func: Callback
        :return: None
        """
        self._events.on_job_top(func)

    def on_job_log(self, func: Callable[[JobLogEvent], None]):
        """
        Callback will execute upon a job log event

        :param func:
        :return: None
        """
        self._events.on_job_log(func)

    def request_stop_job(self, job_id: str):
        """
        Request to stop job - sent by launcher

        :param job_id: job's id
        :return: {"job": Job}
        """
        return self._jobs_service.request_stop_job(job_id)

    def request_pause_job(self, job_id: str):
        """
        Request to pause job - sent by launcher

        :param job_id: job's id
        :return: {"job": Job}
        """
        return self._jobs_service.request_pause_job(job_id)

    def request_start_job(self, job_id: str):
        """
        Start running the job

        :param job_id: job's id
        :return: {"job": Job}
        """
        return self._jobs_service.request_start_job(job_id)

    def request_top_from_job(self, job_id: str):
        """
        Request results of Top from docker - sent by launcher

        :param job_id: job's id
        :return: boolean
        """
        return self._jobs_service.request_top_from_job(job_id)

    def request_logs_from_job(self, job_id: str):
        """
        Request results of logs from docker - sent by launcher

        :param job_id: job id
        :return: boolean
        """
        return self._jobs_service.request_logs_from_job(job_id)

    def list_jobs(
        self,
        jobids: Optional[List[str]] = None,
        receiverids: Optional[List[str]] = None,
        oaids: Optional[List[str]] = None,
        userids: Optional[List[str]] = None,
        stationids: Optional[List[str]] = None,
        statuses: Optional[List[str]] = None,
        page: Optional[int] = 1,
        items: Optional[int] = 25,
    ):
        """
        List of your jobs

        :param jobids: Filter by job ids
        :param receiverids: Filter by receiver ids
        :param oaids: Filter by offer acceptance ids
        :param userids: Filter by user ids
        :param stationids: Filter by station ids
        :param statuses: Filter by statuses
        :param page: Filter by page
        :param items: Filter by items
        :return: {"jobs": [Jobs]}
        """
        return self._jobs_service.list_jobs(
            jobids=jobids,
            receiverids=receiverids,
            oaids=oaids,
            userids=userids,
            stationids=stationids,
            statuses=statuses,
            page=page,
            items=items,
        )

    def download_job_results(self, job_id: str, path: str):
        """
        Download your job results when job is completed

        :param job_id: job's id
        :param path: path to directory, where results will be saved
        :return: None
        """
        return self._jobs_service.download_job_results(job_id, path)
