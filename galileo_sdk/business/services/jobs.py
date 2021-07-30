import os
import zipfile

from ..objects.exceptions import JobsException
from ..utils.generate_query_str import generate_query_str
from galileo_sdk.compat import quote


# TODO: Check some endpoints
class JobsService:
    def __init__(self, jobs_repo, profile_repo):
        """
        Jobs Service

        :param jobs_repo: Jobs Repository
        :type jobs_repo: JobsRepository 
        :param profile_repo: Profile Repository
        :type profile_repo: ProfileRepository
        """
        self._jobs_repo = jobs_repo
        self._profile_repo = profile_repo

    def request_send_job(self):
        """
        FIXME: Potentially out of date
        """
        r = self._jobs_repo.request_send_job()
        return r.json()

    def request_send_job_completed(self, destination_mid, file_name,
                                   station_id):
        """
        FIXME: Potentially out of date
        """
        r = self._jobs_repo.request_send_job_completed(destination_mid,
                                                       file_name, station_id)
        return r.json()

    def request_receive_job(self, job_id):
        """
        FIXME Potentially incorrect endpoint
        """
        r = self._jobs_repo.request_receive_job(job_id)
        return r.json()

    def request_receive_job_completed(self, job_id):
        """
        FIXME Potentially incorrect endpoint
        """
        r = self._jobs_repo.request_receive_job_completed(job_id)
        return r.json()

    def submit_job(self, job_id):
        """
        FIXME: To submit a job, we need to use a mission/project endpoint:
                /projects/{project_id}/jobs
                To resume a job, we PUT to the job/{job_id}/start endpoint
        """
        r = self._jobs_repo.submit_job(job_id)
        return r.json()

    def request_stop_job(self, job_id):
        """
        Stops a job from running. 
        This is a soft stop, the job has a chance to spin down, but it is not resumeable.
        Results will be posted if any were generated.

        :param job_id: Job Id of the job to stop
        :type job_id: str
        :return: The stopped job
        :rtype: Job
        """
        return self._jobs_repo.request_stop_job(job_id)

    def request_pause_job(self, job_id):
        """
        Pauses a running job. It can be resumed with start

        :param job_id: Job Id of the job to pause
        :type job_id: str
        :return: The paused job
        :rtype: Job
        """
        return self._jobs_repo.request_pause_job(job_id)

    def request_start_job(self, job_id):
        """
        Resumes a paused job.

        :param job_id: Job Id of the job to resume
        :type job_id: str
        :return: The resumed job
        :rtype: Job
        """
        return self._jobs_repo.request_start_job(job_id)

    def request_top_from_job(self, job_id):
        """
        Gets the results of Top from docker- a report on resource usage of the job

        :param job_id: Job Id of the job to get the top from
        :type job_id: str
        :return: The top of the job from docker
        :rtype: TopProcess
        """
        return self._jobs_repo.request_top_from_job(job_id)

    def request_logs_from_job(self, job_id):
        """
        Get the logs for the job

        :param job_id: Job Id of the job to get the logs from
        :type job_id: str
        :return: Job Logs
        :rtype: Dict
        """
        return self._jobs_repo.request_logs_from_jobs(job_id)

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
        lz_ids=None,
        owner_ids=None,
        sort_by=None,
        sort_order=None,
    ):
        """
        Get a filtered list of jobs

        :param job_ids: Job Ids to filter by, defaults to None
        :type job_ids: List[str], optional
        :param receiver_ids: Receiver ids to filter by, defaults to None
        :type receiver_ids: List[str], optional
        :param user_ids: User ids to filter by, defaults to None
        :type user_ids: List[str], optional
        :param station_ids: Station ids to filter by, defaults to None
        :type station_ids: List[str], optional
        :param statuses: Statuses to filter by, defaults to None
        :type statuses: List[EJobStatus], optional
        :param page: Number of pages of results, defaults to 1
        :type page: int, optional
        :param items: How many items per page in request, defaults to 25
        :type items: int, optional
        :param mission_ids: Mission ids to filter by, defaults to None
        :type mission_ids: List[str], optional
        :param archived: Search only archived missions, defaults to False
        :type archived: bool, optional
        :param receiver_archived: Filter by jobs archived by the receiver, defaults to False
        :type receiver_archived: bool, optional
        :param partial_names: Filter by partial names, defaults to None
        :type partial_names: List[str], optional
        :param lz_ids: Filter by Landing Zone ids, defaults to None
        :type lz_ids: List[str], optional
        :param owner_ids: Filter by owner user ids, defaults to None
        :type owner_ids: List[str], optional
        :param sort_by: How to sort the jobs by, defaults to None
        :type sort_by: str, optional
        :param sort_order: Sort order of list of jobs, defaults to None
        :type sort_order: str, optional
        :return: List of jobs
        :rtype: List[Job]
        """
        if user_ids is None:
            self_profile = self._profile_repo.self()
            user_ids = [self_profile.user_id]
        query = generate_query_str(
            {
                "page": page,
                "items": items,
                "jobids": job_ids,
                "receiverids": receiver_ids,
                "userids": user_ids,
                "stationids": station_ids,
                "statuses": statuses,
                "projectids": mission_ids,
                "archived": archived,
                "receiver_archived": receiver_archived,
                "partial_names": partial_names,
                "machines": lz_ids,
                "ownerids": owner_ids,
                "sort_by": sort_by,
                "sort_order": sort_order,
            }, )
        return self._jobs_repo.list_jobs(query)

    def download_job_results(self, job_id, path, nonce=None):
        """
        Gets the jobs results file

        :param job_id: Job Id of the job to get the results from
        :type job_id: str
        :param path: File path to store results
        :type path: str
        :param nonce: arbitrary number that can be used just once in a cryptographic communication, defaults to None
        :type nonce: int, optional
        :raises JobsException: No results for the job
        :return: The job results paths
        :rtype: List[str]
        """
        files = self._jobs_repo.get_results_metadata(job_id)

        if not files:
            raise JobsException(job_id, "No files to download")

        files_downloaded = []

        for file in files:
            absolute_path = os.path.join(path, file.filename)
            self._jobs_repo.download_results(
                job_id,
                generate_query_str({
                    "filename": quote(file.filename, safe=""),
                    "path": file.path,
                    "nonce": nonce,
                }),
                os.path.join(path, file.filename),
            )
            files_downloaded.append(absolute_path)

        return files_downloaded

    def download_and_extract_job_results(self, job_id, path, nonce=None):
        """
        Gets the jobs results file and extracts it

        :param job_id: Job Id of the job to get the results from
        :type job_id: str
        :param path: File path to store results
        :type path: str
        :param nonce: arbitrary number that can be used just once in a cryptographic communication, defaults to None
        :type nonce: int, optional
        """
        files_downloaded = self.download_job_results(job_id, path, nonce)
        for file in files_downloaded:
            dir = file.rsplit(".zip", 1)[0]
            if not os.path.exists(dir):
                os.mkdir(dir)
            with zipfile.ZipFile(file) as zf:
                zf.extractall(dir)

    def update_job(self, request):
        """
        Updates a job. You can archive or unarchive a job only.

        :param request: The request to update the job with
        :type request: UpdateJobRequest
        :return: The updated job
        :rtype: Job
        """
        return self._jobs_repo.update_job(request)

    def request_kill_job(self, job_id):
        """
        Kills a job. This can be done at any phase of running a job, and terminates the job immediately. 
        Results may exist if they were already posted but otherwise no results will be posted.

        :param job_id: Job Id of the job to kill
        :type job_id: str
        :return: Killed job
        :rtype: Job
        """
        return self._jobs_repo.request_kill_job(job_id)
