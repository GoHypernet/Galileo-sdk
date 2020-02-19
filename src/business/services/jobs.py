from typing import List, Optional

from ...data.repositories.jobs import JobsRepository
from ..utils.generate_query_str import generate_query_str


class JobsService:
    def __init__(self, jobs_repo: JobsRepository):
        self._jobs_repo = jobs_repo

    def request_send_job(self):
        r = self._jobs_repo.request_send_job()
        return r.json()

    def request_send_job_completed(
        self, destination_mid: str, file_name: str, station_id: str
    ):
        r = self._jobs_repo.request_send_job_completed(
            destination_mid, file_name, station_id
        )
        return r.json()

    def request_receive_job(self, job_id: str):
        r = self._jobs_repo.request_receive_job(job_id)
        return r.json()

    def request_receive_job_completed(self, job_id: str):
        r = self._jobs_repo.request_receive_job_completed(job_id)
        return r.status_code == 200

    def submit_job(self, job_id: str):
        r = self._jobs_repo.submit_job(job_id)
        return r.json()

    def request_stop_job(self, job_id: str):
        r = self._jobs_repo.request_stop_job(job_id)
        return r.json()

    def request_pause_job(self, job_id: str):
        r = self._jobs_repo.request_pause_job(job_id)
        return r.json()

    def request_top_from_job(self, job_id: str):
        r = self._jobs_repo.request_top_from_job(job_id)
        return r.status_code == 200

    def request_logs_from_job(self, job_id: str):
        r = self._jobs_repo.request_logs_from_jobs(job_id)
        return r.status_code == 200

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
        """
        List all current jobs

        :param page: optional, page #
        :param items: optional, item per page
        :param jobids: optional, filter by job id
        :param receiverids: optional, filter by receiver's id
        :param senderids: optional, filter by sender's id
        :param oaids: optional, filter by oaid
        :param userids: optional, filter by user's id
        :param stationids: optional, filter by station's id
        :param statuses: optional, filter by job's status
        :return: response with object {'jobs', [<jobs>]}
        """

        query = generate_query_str(
            {
                "page": page,
                "items": items,
                "jobids": jobids,
                "receiverids": receiverids,
                "senderids": senderids,
                "oaids": oaids,
                "userids": userids,
                "stationids": stationids,
                "statuses": statuses,
            },
        )
        r = self._jobs_repo.list_jobs(query)

        return r.json()
