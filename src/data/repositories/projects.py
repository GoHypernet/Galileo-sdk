from typing import Any, Callable, Optional
from urllib.parse import urlunparse

import requests

from ..providers.auth import AuthProvider
from .settings import SettingsRepository


class ProjectsRepository:
    def __init__(
        self, settings_repository: SettingsRepository, auth_provider: AuthProvider
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider

    def _make_url(self, endpoint, params="", query="", fragment=""):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse(
            (
                schema,
                f"{addr}/galileo/user_interface/v1",
                endpoint,
                params,
                query,
                fragment,
            )
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
        try:
            r = request(url, json=data, headers=headers)
            return r
        except requests.exceptions.RequestException as e:
            print(e)

    def _post(self, *args, **kwargs):
        return self._request(requests.post, *args, **kwargs)

    def create_project(self):
        return self._post("/projects")

    def upload_single_file(self, project_id: str):
        return self._post(f"/projects/{project_id}/files")

    def run_job_on_station(self, project_id: str, station_id: str):
        return self._post(
            f"/projects/{project_id}/jobs", data={"station_id": station_id}
        )

    def run_job_on_machine(self, project_id: str, station_id: str, machine_id: str):
        return self._post(
            f"/projects/{project_id}/jobs",
            data={"station_id": station_id, "machine_id": machine_id},
        )
