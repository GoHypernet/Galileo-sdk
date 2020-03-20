from datetime import datetime
from typing import Any, Callable, List, Optional
from urllib.parse import urlunparse

import requests

from galileo_sdk.business.objects import (EJobStatus, Job, JobStatus,
                                          UpdateJobRequest)
from galileo_sdk.business.objects.jobs import (FileListing, TopDetails,
                                               TopProcess)

from ..providers.auth import AuthProvider
from .settings import SettingsRepository


class JobsRepository:
    def __init__(
        self,
        settings_repository: SettingsRepository,
        auth_provider: AuthProvider,
        namespace: str,
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider
        self._namespace = namespace

    def _make_url(
        self,
        endpoint: str,
        params: Optional[str] = "",
        query: Optional[str] = "",
        fragment: Optional[str] = "",
    ):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse(
            (schema, f"{addr}{self._namespace}", endpoint, params, query, fragment,)
        )

    def _request(
        self,
        request: Callable,
        endpoint: str,
        data: Optional[Any] = None,
        params: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
    ):
        url = self._make_url(endpoint, params, query, fragment)
        access_token = self._auth_provider.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        r = request(url, json=data, headers=headers)
        r.raise_for_status()
        return r

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request(requests.post, *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request(requests.put, *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._request(requests.delete, *args, **kwargs)

    def request_send_job(self):
        return self._get("/job/upload_request")

    def request_send_job_completed(
        self, destination_mid: str, file_name: str, station_id: str
    ):
        return self._post(
            "/jobs",
            {
                "destination_mid": destination_mid,
                "filename": file_name,
                "stationid": station_id,
            },
        )

    def request_receive_job(self, job_id: str):
        return self._get(f"/jobs/{job_id}/results/location")

    def request_receive_job_completed(self, job_id: str):
        return self._put(f"/jobs/{job_id}/results/download_complete")

    def submit_job(self, job_id: str):
        return self._put(f"/jobs/{job_id}/run")

    def request_stop_job(self, job_id: str) -> Job:
        response = self._put(f"/jobs/{job_id}/stop")
        json: dict = response.json()
        job: dict = json["job"]
        return job_dict_to_job(job)

    def request_pause_job(self, job_id: str) -> Job:
        response = self._put(f"/jobs/{job_id}/pause")
        json: dict = response.json()
        job: dict = json["job"]
        return job_dict_to_job(job)

    def request_start_job(self, job_id: str) -> Job:
        response = self._put(f"/jobs/{job_id}/start")
        json: dict = response.json()
        job: dict = json["job"]
        return job_dict_to_job(job)

    def request_top_from_job(self, job_id: str) -> List[TopProcess]:
        response = self._get(f"/jobs/{job_id}/top")
        json: dict = response.json()
        top: dict = json["top"]
        return [
            top_dict_to_jobs_top(process, top["Titles"]) for process in top["Processes"]
        ]

    def request_logs_from_jobs(self, job_id: str) -> str:
        response = self._get(f"/jobs/{job_id}/logs")
        json: dict = response.json()
        logs: str = json["logs"]
        return logs

    def list_jobs(self, query: str) -> List[Job]:
        response = self._get("/jobs", query=query)
        json: dict = response.json()
        jobs: List[dict] = json["jobs"]
        return [job_dict_to_job(job) for job in jobs]

    def get_results_url(self, job_id: str) -> List[FileListing]:
        response = self._get(f"/jobs/{job_id}/results")
        json: dict = response.json()
        files: List[dict] = json["files"]
        return [file_dict_to_file_listing(file) for file in files]

    def download_results(self, job_id: str, query: str, filename: str) -> str:
        with self._get(f"/jobs/{job_id}/results", query=query) as r:
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
        return filename

    def update_job(self, request: UpdateJobRequest) -> Job:
        response = self._put(f"/jobs/{request.job_id}", {"archived": request.archived})
        json: dict = response.json()
        job: dict = json["job"]
        return job_dict_to_job(job)

    def request_kill_job(self, job_id: str) -> Job:
        response = self._put(f"/jobs/{job_id}/kill")
        json: dict = response.json()
        job: dict = json["job"]
        return job_dict_to_job(job)


def top_dict_to_jobs_top(process: List[str], titles: List[str]) -> TopProcess:
    return TopProcess(
        [TopDetails(title, detail) for detail, title in zip(process, titles)]
    )


def file_dict_to_file_listing(file: dict) -> FileListing:
    return FileListing(file["filename"], file["path"])


def job_dict_to_job(job: dict) -> Job:
    return Job(
        job["jobid"],
        job["receiverid"],
        job["project_id"],
        datetime.fromtimestamp(job["time_created"]),
        datetime.fromtimestamp(job["last_updated"]),
        job["status"],
        job["container"],
        job["name"],
        job["stationid"],
        job["userid"],
        job["state"],
        job["oaid"],
        job["pay_status"],
        job["pay_interval"],
        job["total_runtime"],
        job["archived"],
        [
            job_status_dict_to_job_status(job_status)
            for job_status in job["status_history"]
        ],
    )


def job_status_dict_to_job_status(job_status: dict) -> JobStatus:
    status = JobStatus(
        datetime.fromtimestamp(job_status["timestamp"]),
        EJobStatus[job_status["status"]],
    )
    status.jobstatusid = (
        job_status["jobstatusid"] if "jobstatusid" in job_status else None
    )
    status.jobid = job_status["jobid"] if "jobid" in job_status else None
    return status
