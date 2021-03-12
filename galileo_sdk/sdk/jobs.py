from .event import EventsSdk
from ..business.objects.jobs import UpdateJobRequest


class JobsSdk(EventsSdk):
    def __init__(self, jobs_service, connector=None, events=None):
        self._jobs_service = jobs_service
        super(JobsSdk, self).__init__(
            connector=connector, events=events,
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
        jobids=None,
        receiverids=None,
        oaids=None,
        userids=None,
        stationids=None,
        statuses=None,
        page=1,
        items=25,
        projectids=None,
        archived=False,
        receiver_archived=False,
        partial_names=None,
        machines=None,
        ownerids=None,
        sort_by=None,
        sort_order=None,
    ):
        """
        Get a filtered list of all jobs run under your Galileo account.
        
        :param jobids: List[str]: Filter by job ids
        :param receiverids: List[str]: Filter by receiver ids
        :param oaids: List[str]: Filter by offer acceptance ids
        :param userids: List[str]: Filter by user ids
        :param stationids: List[str]: Filter by station ids
        :param statuses: List[str]: Filter by statuses
        :param page: int: Filter by page
        :param items: int: Filter by items
        :param projectids: List[str]: Filter by projectid
        :param archived: boolean: Filter by archived
        :param receiver_archived: boolean: Filter by receiver archived
        :param partial_names: List[str]: Filter by partial names
        :param machines: List[str]: Filter by machines id
        :param ownerids: List[str]: Filter by ownerid
        :param sort_by: EJobSort
        :param sort_order: str: "asc" or "desc"
        :return: List[Job]
        
        Example:
        
            >>> jobs = galileo.jobs.list_jobs(items=25)
            >>> for job in jobs:
            >>>     print(job.name)
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
            projectids=projectids,
            archived=archived,
            receiver_archived=receiver_archived,
            partial_names=partial_names,
            lz=machines,
            ownerids=ownerids,
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
        """
        return self._jobs_service.download_job_results(job_id, path, nonce)

    def update_job(self, job_id, archived=None):
        """ Updates an existing job

        :param job_id:
        :param archived: bool: Archive a job
        return: Job
        """
        request = UpdateJobRequest(job_id, archived)

        return self._jobs_service.update_job(request)

    def request_kill_job(self, job_id):
        """
        Request to kill a job

        :param job_id: str
        :return: Job
        """
        return self._jobs_service.request_kill_job(job_id)

    def download_and_extract_job_results(self, job_id, path, nonce=None):
        """
        Download and extract your job results when job is completed

        :param job_id: str
        :param path: str: path to directory, where results will be saved
        :param nonce: str: can still download the file if provide an auth token
        :return: List[str]: list of filenames that were downloaded
        """
        return self._jobs_service.download_and_extract_job_results(job_id, path, nonce)
