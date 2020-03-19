from typing import Callable, List, Optional

from galileo_sdk.business.objects import (Job, JobLauncherUpdatedEvent,
                                          JobsEvents, StationJobUpdatedEvent,
                                          UpdateJobRequest)
from galileo_sdk.business.objects.jobs import (JobLauncherSubmittedEvent,
                                               TopProcess)

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

        :param func: Callable[[JobLauncherUpdatedEvent], None]
        :return: None
        """
        self._events.on_job_launcher_updated(func)

    def on_job_launcher_submitted(
        self, func: Callable[[JobLauncherSubmittedEvent], None]
    ):
        """

        :param func: Callable[[JobLauncherSubmittedEvent]
        :return: None
        """
        self._events.on_job_launcher_submitted(func)

    def on_station_job_updated(self, func: Callable[[StationJobUpdatedEvent], None]):
        """
        Callback will execute upon a station job updated event

        :param func: Callable[[StationJobUpdatedEvent], None]
        :return: None
        """
        self._events.on_station_job_updated(func)

    def request_stop_job(self, job_id: str) -> Job:
        """
        Request to stop job - sent by launcher

        :param job_id: job's id
        :return: Job
        """
        return self._jobs_service.request_stop_job(job_id)

    def request_pause_job(self, job_id: str) -> Job:
        """
        Request to pause job - sent by launcher

        :param job_id: job's id
        :return: Job
        """
        return self._jobs_service.request_pause_job(job_id)

    def request_start_job(self, job_id: str) -> Job:
        """
        Start running the job

        :param job_id: job's id
        :return: Job
        """
        return self._jobs_service.request_start_job(job_id)

    def request_top_from_job(self, job_id: str) -> List[TopProcess]:
        """
        Request results of Top from docker - sent by launcher

        :param job_id: job's id
        :return: List[TopProcess]: list of top processes
        """
        return self._jobs_service.request_top_from_job(job_id)

    def request_logs_from_job(self, job_id: str) -> str:
        """
        Request results of logs from docker - sent by launcher

        :param job_id: job id
        :return: string
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
    ) -> List[Job]:
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
        :return: List[Job]
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

    def download_job_results(self, job_id: str, path: str) -> List[str]:
        """
        Download your job results when job is completed

        :param job_id: job's id
        :param path: path to directory, where results will be saved
        :return: List[str]: list of filenames that were downloaded
        """
        return self._jobs_service.download_job_results(job_id, path)

    def update_job(self, request: UpdateJobRequest) -> Job:
        """ Updates an existing job

        :param request: An UpdateJobRequest object
        return: Job
        """

        return self._jobs_service.update_job(request)

    def request_kill_job(self, job_id: str) -> Job:
        """
        Request to kill a job

        :param job_id: job's id
        :return: Job
        """
        return self._jobs_service.request_kill_job(job_id)
