from galileo_sdk.business.services.jobs import JobsService
from .event import EventsSdk
from ..business.objects.jobs import UpdateJobRequest


class JobsSdk(EventsSdk):
    def __init__(self, jobs_service, connector=None, events=None):
        self._jobs_service = jobs_service
        super(JobsSdk, self).__init__(
            connector=connector,
            events=events,
        )

    def on_job_launcher_updated(self, func):
        """
        Callback will execute upon a job launcher updated event

        :param func: Callable[[JobLauncherUpdatedEvent], None]
        :return: None
        """
        self._set_event_handler("jobs")
        self._events.on_job_launcher_updated(func)

    def on_job_launcher_submitted(self, func):
        """

        :param func: Callable[[JobLauncherSubmittedEvent]
        :return: None
        """
        self._set_event_handler("jobs")
        self._events.on_job_launcher_submitted(func)

    def on_station_job_updated(self, func):
        """
        Callback will execute upon a station job updated event

        :param func: Callable[[StationJobUpdatedEvent], None]
        :return: None
        """
        self._set_event_handler("jobs")
        self._events.on_station_job_updated(func)

    def request_stop_job(self, job_id):
        """
        Request to stop job - sent by launcher

        :param job_id: str
        :return: Job
        """
        return self._jobs_service.request_stop_job(job_id)

    def request_pause_job(self, job_id):
        """
        Request to pause job - sent by launcher

        :param job_id: str
        :return: Job
        """
        return self._jobs_service.request_pause_job(job_id)

    def request_start_job(self, job_id):
        """
        Start running the job

        :param job_id: str
        :return: Job
        """
        return self._jobs_service.request_start_job(job_id)

    def request_top_from_job(self, job_id):
        """
        Request results of Top from docker - sent by launcher

        :param job_id: str
        :return: List[TopProcess]: list of top processes
        """
        return self._jobs_service.request_top_from_job(job_id)

    def request_logs_from_job(self, job_id):
        """
        Request results of logs from docker - sent by launcher

        :param job_id: str
        :return: string
        """
        return self._jobs_service.request_logs_from_job(job_id)

    def list_jobs(
        self,
        job_ids=None,
        receiver_ids=None,
        user_ids=None,
        station_ids=None,
        statuses=None,
        page=1,
        items=25,
        mission_ids=None,
        archived=False,
        receiver_archived=False,
        partial_names=None,
        lzs=None,
        owner_ids=None,
        sort_by=None,
        sort_order=None,
    ):
        """
        Get a filtered list of all jobs run under your Galileo account.
        
        :param job_ids: List[str]: Filter by job ids
        :param receiver_ids: List[str]: Filter by receiver ids
        :param user_ids: List[str]: Filter by user ids
        :param station_ids: List[str]: Filter by station ids
        :param statuses: List[str]: Filter by statuses
        :param page: int: Filter by page
        :param items: int: Filter by items
        :param mission_ids: List[str]: Filter by mission ids 
        :param archived: boolean: Filter by archived
        :param receiver_archived: boolean: Filter by receiver archived
        :param partial_names: List[str]: Filter by partial names
        :param lzs: List[str]: Filter by lz id
        :param owner_ids: List[str]: Filter by owner id
        :param sort_by: EJobSort
        :param sort_order: str: "asc" or "desc"
        :return: List[Job]
        
        Example:
        
            >>> jobs = galileo.jobs.list_jobs(items=25)
            >>> for job in jobs:
            >>>     print(job.name)
        """
        return self._jobs_service.list_jobs(
            job_ids=job_ids,
            receiver_ids=receiver_ids,
            user_ids=user_ids,
            station_ids=station_ids,
            statuses=statuses,
            page=page,
            items=items,
            mission_ids=mission_ids,
            archived=archived,
            receiver_archived=receiver_archived,
            partial_names=partial_names,
            lz_ids=lzs,
            owner_ids=owner_ids,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    def download_job_results(self, job_id, path, nonce=None):
        """
        Download your job results when job is completed

        :param job_id: str
        :param path: str: path to directory, where results will be saved
        :param nonce: str: can still download the file if provide an auth token
        :return: List[str]: list of filenames that were downloaded

        Example:
            >>> job_id = "my_job_id"
            >>> path = "results_folder"
            >>> results = galileo.jobs.download_job_results(job_id, path)
        """
        return self._jobs_service.download_job_results(job_id,
                                                       path,
                                                       nonce=nonce)

    def update_job(self, job_id, archived=None):
        """ Updates an existing job

        :param job_id:
        :param archived: bool: Archive a job
        return: Job


        Example:
            >>> job_id = "my_job_id"
            >>> galileo.jobs.update_job(job_id, archived=True)        
        """
        request = UpdateJobRequest(job_id, archived)

        return self._jobs_service.update_job(request)

    def request_kill_job(self, job_id):
        """
        Request to kill a job

        :param job_id: str
        :return: Job

        Example:
            >>> job_id = "my_job_id"
            >>> galileo.jobs.request_kill_job(job_id)
        """
        return self._jobs_service.request_kill_job(job_id)

    def download_and_extract_job_results(self, job_id, path, nonce=None):
        """
        Download and extract your job results when job is completed

        :param job_id: str
        :param path: str: path to directory, where results will be saved
        :param nonce: str: can still download the file if provide an auth token
        :return: List[str]: list of filenames that were downloaded

        Example:
            >>> job_id = "my_job_id"
            >>> path = "results_folder"
            >>> results = galileo.jobs.download_and_extract_job_results(job_id, path)
        """
        return self._jobs_service.download_and_extract_job_results(job_id,
                                                                   path,
                                                                   nonce=nonce)
