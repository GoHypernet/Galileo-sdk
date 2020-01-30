from typing import Any, Callable, List, Optional
from urllib.parse import urlunparse

import requests

from ..providers.auth import AuthProvider
from .settings import SettingsRepository


class JobsRepository:
    def __init__(
        self, settings_repository: SettingsRepository, auth_provider: AuthProvider,
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider

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
        return urlunparse((schema, addr, endpoint, params, query, fragment))

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
        return request(url, json=data, headers=headers)

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request(requests.post, *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request(requests.put, *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._request(requests.delete, *args, **kwargs)

    def request_send_job(self):
        """
        Sending job request requires you to upload the job to Google Storage

        :return: location: Google Storage URL where you can upload job
        """
        return self._get("/job/upload_request")

    def request_send_job_completed(
        self, destination_mid: str, file_name: str, station_id: str
    ):
        """
        After finishing your upload to Google Storage, inform that the job is ready to go

        :param destination_mid: landing zone id
        :param file_name: job's name
        :param station_id: station you're sending the job through
        :return: {"job" : Job}
        """
        return self._post(
            "/jobs",
            {
                "destination_mid": destination_mid,
                "filename": file_name,
                "stationid": station_id,
            },
        )

    def request_receive_job(self, job_id: str):
        """
        :param job_id: job's id
        :return: {"location": URL, "filename": filename}
        """
        return self._get(f"/jobs/{job_id}/results/location")

    def request_receive_job_completed(self, job_id: str):
        """
        :param job_id: job's id
        :return: boolean, True for success
        """
        return self._put(f"/jobs/{job_id}/results/download_complete")

    def submit_job(self, job_id: str):
        """
        Start running the job

        :param job_id: job's id
        :return: {"job": Job}
        """
        return self._put(f"/jobs/{job_id}/run")

    def request_stop_job(self, job_id: str):
        """
        Request to stop a job - sent by launcher

        :param job_id: job's id
        :return: response with object {"job": Job}
        """
        return self._put(f"/jobs/{job_id}/stop")

    def request_pause_job(self, job_id: str):
        """
        Request to pause job - sent by launcher

        :param job_id: job's id
        :return: response with object {"job": Job}
        """
        return self._put(f"/jobs/{job_id}/pause")

    def request_start_job(self, job_id: str):
        """
        Request start job - sent by launcher

        :param job_id: job's id
        :return: response with object {"job": Job}
        """
        return self._put(f"/jobs/{job_id}/start")

    def request_top_from_job(self, job_id: str):
        """
        Request results of Top from docker - sent by launcher

        :param job_id: job's id
        :return: boolean, True on success
        """
        return self._get(f"/jobs/{job_id}/top")

    def request_logs_from_jobs(self, job_id: str):
        """
        Request results of logs from docker - sent by launcher

        :param job_id: job id
        :return: boolean, True on success
        """
        return self._get(f"/jobs/{job_id}/logs")

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
        return self._get(
            "/jobs",
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
