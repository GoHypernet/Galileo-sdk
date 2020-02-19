from typing import Any, Callable, List, Optional
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
        files: Optional[Any] = None,
        filename: Optional[str] = None,
    ):
        url = self._make_url(endpoint, params, query, fragment)
        access_token = self._auth_provider.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}

        if files is None:
            r = request(url, json=data, headers=headers)
        else:
            headers["filename"] = filename
            headers["Content-Type"] = "application/octet-stream"
            r = request(url, json=data, headers=headers, data=files)

        r.raise_for_status()
        return r

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request(requests.post, *args, **kwargs)

    def list_projects(self, query: str):
        return self._get("/projects", query=query)

    def create_project(self, name: str, description: str):
        return self._post("/projects", {"name": name, "description": description})

    def upload_single_file(self, project_id: str, file: Any, filename: str):
        return self._post(
            f"/projects/{project_id}/files", files=file, filename=filename
        )

    def run_job_on_station(self, project_id: str, station_id: str):
        return self._post(
            f"/projects/{project_id}/jobs", data={"station_id": station_id}
        )

    def run_job_on_machine(self, project_id: str, station_id: str, machine_id: str):
        return self._post(
            f"/projects/{project_id}/jobs",
            data={"station_id": station_id, "machine_id": machine_id},
        )
