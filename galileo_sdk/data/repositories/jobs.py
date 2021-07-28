from datetime import datetime
import os

from galileo_sdk.business.objects import EJobStatus, Job, JobStatus, UpdateJobRequest
from galileo_sdk.business.objects.jobs import TopDetails, TopProcess
from galileo_sdk.business.objects.missions import FileListing
from galileo_sdk.data.repositories import RequestsRepository

import sys

_ver = sys.version_info

is_py2 = _ver[0] == 2
is_py3 = _ver[0] == 3


#TODO Check some of these endpoints
class JobsRepository(RequestsRepository):
    def __init__(
        self,
        settings_repository,
        auth_provider,
        namespace,
    ):
        super(JobsRepository, self).__init__(
            settings_repository=settings_repository,
            auth_provider=auth_provider,
            namespace=namespace,
        )

    """
    #FIXME: POTENTIALLY OUT OF DATE
    """

    def request_send_job(self):
        return self._get("/job/upload_request")

    def request_send_job_completed(self, destination_mid, filename,
                                   station_id):
        """
        FIXME: Potentially out of date
        """
        return self._post(
            "/jobs",
            {
                "destination_mid": destination_mid,
                "filename": filename,
                "stationid": station_id,
            },
        )

    def request_receive_job(self, job_id):
        """
        FIXME Potentially incorrect endpoint
        """
        return self._get(
            "/jobs/{job_id}/results/location".format(job_id=job_id))

    def request_receive_job_completed(self, job_id):
        """
        FIXME Potentially incorrect endpoint
        """
        return self._put(
            "/jobs/{job_id}/results/download_complete".format(job_id=job_id))

    def submit_job(self, job_id):
        """
        FIXME: To submit a job, we need to use a mission/project endpoint:
                /projects/{project_id}/jobs
                To resume a job, we PUT to the job/{job_id}/start endpoint
        """
        return self._put("/jobs/{job_id}/run".format(job_id=job_id))

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
        response = self._put("/jobs/{job_id}/stop".format(job_id=job_id))
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def request_pause_job(self, job_id):
        """
        Pauses a running job. It can be resumed with start

        :param job_id: Job Id of the job to pause
        :type job_id: str
        :return: The paused job
        :rtype: Job
        """
        response = self._put("/jobs/{job_id}/pause".format(job_id=job_id))
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def request_start_job(self, job_id):
        """
        Resumes a paused job.

        :param job_id: Job Id of the job to resume
        :type job_id: str
        :return: The resumed job
        :rtype: Job
        """
        response = self._put("/jobs/{job_id}/start".format(job_id=job_id))
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def request_top_from_job(self, job_id):
        """
        Gets the results of Top from docker- a report on resource usage of the job

        :param job_id: Job Id of the job to get the top from
        :type job_id: str
        :return: The top of the job from docker
        :rtype: TopProcess
        """
        response = self._get("/jobs/{job_id}/top".format(job_id=job_id))
        json = response.json()
        top = json["top"]
        return [
            top_dict_to_jobs_top(process, top["Titles"])
            for process in top["Processes"]
        ]

    def request_logs_from_jobs(self, job_id):
        """
        Get the logs for the job

        :param job_id: Job Id of the job to get the logs from
        :type job_id: str
        :return: Job Logs
        :rtype: Dict
        """
        response = self._get("/jobs/{job_id}/logs".format(job_id=job_id))
        json = response.json()
        logs = json["logs"]
        return logs

    def list_jobs(self, query):
        """
        Gets a filtered list of jobs

        :param query: Parameters to filter the list of jobs with
        :type query: str
        :return: List of jobs
        :rtype: List[Job]
        """
        response = self._get("/jobs", query=query)
        json = response.json()
        jobs = json["jobs"]
        return [job_dict_to_job(job) for job in jobs]

    def get_results_metadata(self, job_id):
        """
        Gets the jobs results metadata

        :param job_id: Job Id of the job to get the results from
        :type job_id: str
        :return: Results file
        :rtype: List[FileListing]
        """
        response = self._get("/jobs/{job_id}/results".format(job_id=job_id))
        json = response.json()
        files = json["files"]
        return [file_dict_to_file_listing(file) for file in files]

    def download_results(self, job_id, query, filename):
        """
        Downloads the results of the job

        :param job_id: Job Id of the job to download the results from
        :type job_id: str
        :param query: Filter parameters for the results
        :type query: str
        :param filename: Filename to save the results to 
        :type filename: str
        :return: saved filename
        :rtype: str
        """
        dir = os.path.dirname(filename)
        if not os.path.exists(dir):
            os.mkdir(dir)

        if is_py3:
            with self._get(
                    "/jobs/{job_id}/results".format(job_id=job_id),
                    query=query,
                    filename=filename,
            ) as r:
                with open(filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
        elif is_py2:
            r = self._get("/jobs/{job_id}/results".format(job_id=job_id),
                          query=query)
            f = open(filename, "wb")
            f.write(r.json_obj)

        return filename

    def update_job(self, request):
        """
        Updates a job. You can archive or unarchive a job only.

        :param request: The request to update the job with
        :type request: UpdateJobRequest
        :return: The updated job
        :rtype: Job
        """
        response = self._put(
            "/jobs/{job_id}".format(job_id=request.job_id),
            {"archived": request.archived},
        )
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def request_kill_job(self, job_id):
        """
        Kills a job. This can be done at any phase of running a job, and terminates the job immediately. 
        Results may exist if they were already posted but otherwise no results will be posted.

        :param job_id: Job Id of the job to kill
        :type job_id: str
        :return: Killed job
        :rtype: Job
        """
        response = self._put("/jobs/{job_id}/kill".format(job_id=job_id))
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)


def top_dict_to_jobs_top(process, titles):
    """
    Convert Top process to object

    :param process: Docker Process
    :type process: List[str]
    :param titles: Tile for the process
    :type titles: List[str]
    :return: List of top processes
    :rtype: List[TopProcess]
    """
    return TopProcess(
        [TopDetails(title, detail) for detail, title in zip(process, titles)])


def file_dict_to_file_listing(file):
    """
    Convert file dictionary to FileListing object

    :param file: File dictionary
    :type file: Dict 
    :return: File Listing
    :rtype: FileListing
    """
    return FileListing(
        file["filename"],
        file["path"],
        file.get("modification_date", None),
        file.get("creation_date", None),
        file.get("file_size", None),
        file.get("nonce", None),
    )


def job_dict_to_job(job):
    """
    Convert job dictionary to Job object

    :param job: Job Response
    :type job: Dict
    :return: Job Object
    :rtype: Job
    """
    print(job)

    return Job(
        job["jobid"],
        job["receiverid"],
        job["project_id"],
        datetime.fromtimestamp(job["time_created"]),
        datetime.fromtimestamp(job["last_updated"]),
        job["status"],
        job["cpu_count"],
        job["gpu_count"],
        job["memory_amount"],
        job["enable_tunnel"],
        job["tunnel_port"],
        job["tunnel_url"],
        job["name"],
        job["stationid"],
        job["userid"],
        job["state"],
        job["pay_status"],
        job["pay_interval"],
        job["total_runtime"],
        job["archived"],
        [
            job_status_dict_to_job_status(job_status)
            for job_status in job["status_history"]
        ],
    )


def job_status_dict_to_job_status(job_status):
    """
    Convert job status dictionary to JobStatus object

    :param job_status: Job Status Response
    :type job_status: Dict
    :return: Job Status Object
    :rtype: EJJobStatus
    """
    status = JobStatus(
        datetime.fromtimestamp(job_status["timestamp"]),
        EJobStatus[job_status["status"]],
    )
    status.jobstatusid = (job_status["jobstatusid"]
                          if "jobstatusid" in job_status else None)
    status.jobid = job_status["jobid"] if "jobid" in job_status else None
    return status
