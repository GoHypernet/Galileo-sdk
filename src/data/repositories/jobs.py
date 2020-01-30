from typing import Any, Callable, Optional
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

    def _make_url(self, endpoint, params="", query="", fragment=""):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse((schema, backend, endpoint, params, query, fragment))

    def _request(
        self,
        request: Callable,
        endpoint: str,
        data=Optional[Any],
        params=Optional[str],
        query=Optional[str],
        fragment=Optional[str],
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
        return self._get("/job/upload_request")

    def request_send_job_completed(self, destination_mid, file_name, station_id):
        return self._post("/jobs", {destination_mid, file_name, station_id})

    def request_receive_job(self, job_id):
        return self._get(f"/jobs/{job_id}/results/location")

    def request_receive_job_completed(self, job_id):
        return self._get(f"/jobs/{job_id}/results/download_completed")

    def submit_job(self, job_id):
        return self._put(f"/jobs/{job_id}/run")

    def request_stop_job(self, job_id):
        """

        :param job_id:
        :return:
        """
        return self._put(f"/jobs/{job_id}/stop")

    def request_pause_job(self, job_id):
        """
        Request to pause job - sent by launcher

        :param job_id: job's id
        :return: response with object {"job": Job}
        """
        return self._put(f"/jobs/{job_id}/pause")

    def request_start_job(self, job_id):
        """
        Request start job - sent by launcher

        :param job_id: job's id
        :return: response with object {"job": Job}
        """
        return self._put(f"/jobs/{job_id}/start")

    def request_top_from_job(self, job_id):
        """
        Request results of Top from docker - sent by launcher

        :param job_id: job's id
        :return: boolean, True on success
        """
        return self._get(f"/jobs/{job_id}/top")

    def request_logs_from_jobs(self, job_id):
        """
        Request results of logs from docker - sent by launcher

        :param job_id: job id
        :return: boolean, True on success
        """
        return self._get(f"/jobs/{job_id}/logs")

    def list_jobs(
        self,
        page=1,
        items=25,
        jobids=None,
        receiverids=None,
        senderids=None,
        oaids=None,
        userids=None,
        stationids=None,
        statuses=None,
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
        :return: response with object {'jobs', [<job>]}
        """
        return self._get(
            "/jobs",
            {
                page,
                items,
                jobids,
                receiverids,
                senderids,
                oaids,
                userids,
                stationids,
                statuses,
            },
        )
