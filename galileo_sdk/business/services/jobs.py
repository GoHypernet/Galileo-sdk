import os
from typing import List, Optional

from galileo_sdk.business.objects import Job, UpdateJobRequest
from galileo_sdk.business.objects.jobs import FileListing, TopProcess

from ...data.repositories.jobs import JobsRepository
from ..objects.exceptions import JobsException
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
        return r.json()

    def submit_job(self, job_id: str):
        r = self._jobs_repo.submit_job(job_id)
        return r.json()

    def request_stop_job(self, job_id: str) -> Job:
        return self._jobs_repo.request_stop_job(job_id)

    def request_pause_job(self, job_id: str) -> Job:
        return self._jobs_repo.request_pause_job(job_id)

    def request_start_job(self, job_id: str) -> Job:
        return self._jobs_repo.request_start_job(job_id)

    def request_top_from_job(self, job_id: str) -> List[TopProcess]:
        return self._jobs_repo.request_top_from_job(job_id)

    def request_logs_from_job(self, job_id: str) -> str:
        return self._jobs_repo.request_logs_from_jobs(job_id)

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
        query: str = generate_query_str(
            {
                "page": page,
                "items": items,
                "jobids": jobids,
                "receiverids": receiverids,
                "oaids": oaids,
                "userids": userids,
                "stationids": stationids,
                "statuses": statuses,
            },
        )
        return self._jobs_repo.list_jobs(query)

    def download_job_results(self, job_id: str, path: str) -> List[str]:
        files: List[FileListing] = self._jobs_repo.get_results_url(job_id)

        if not files:
            raise JobsException(job_id, "No files to download")

        files_downloaded: List[str] = []

        for file in files:
            response = self._jobs_repo.download_results(
                job_id,
                generate_query_str({"filename": file.filename, "path": file.path}),
                os.path.join(path, file.filename),
            )
            files_downloaded.append(response)

        return files_downloaded

    def update_job(self, request: UpdateJobRequest) -> Job:
        return self._jobs_repo.update_job(request)

    def request_kill_job(self, job_id: str) -> Job:
        return self._jobs_repo.request_kill_job(job_id)
