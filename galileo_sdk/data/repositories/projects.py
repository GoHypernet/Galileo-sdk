from typing import Any, Callable, List, Optional
from urllib.parse import urlunparse

import requests

from galileo_sdk.business.objects.jobs import Job
from galileo_sdk.business.objects.projects import (DirectoryListing,
                                                   FileListing, Project)
from galileo_sdk.data.repositories.jobs import job_dict_to_job

from ..providers.auth import AuthProvider
from .settings import SettingsRepository


class ProjectsRepository:
    def __init__(
        self,
        settings_repository: SettingsRepository,
        auth_provider: AuthProvider,
        namespace: str,
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider
        self._namespace = namespace

    def _make_url(self, endpoint, params="", query="", fragment=""):
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

    def list_projects(self, query: str) -> List[Project]:
        response = self._get("/projects", query=query)
        json: dict = response.json()
        projects: List[dict] = json["projects"]
        return [project_dict_to_project(project) for project in projects]

    def create_project(self, name: str, description: str) -> Project:
        response = self._post("/projects", {"name": name, "description": description})
        json: dict = response.json()
        project: dict = json["project"]
        return project_dict_to_project(project)

    def upload_single_file(self, project_id: str, file: Any, filename: str) -> bool:
        r = self._post(f"/projects/{project_id}/files", files=file, filename=filename)
        return r.json()

    def run_job_on_station(self, project_id: str, station_id: str) -> Job:
        response = self._post(
            f"/projects/{project_id}/jobs", data={"station_id": station_id}
        )
        json: dict = response.json()
        job: dict = json["job"]
        return job_dict_to_job(job)

    def run_job_on_machine(
        self, project_id: str, station_id: str, machine_id: str
    ) -> Job:
        response = self._post(
            f"/projects/{project_id}/jobs",
            data={"station_id": station_id, "machine_id": machine_id},
        )
        json: dict = response.json()
        job: dict = json["job"]
        return job_dict_to_job(job)

    def inspect_project(self, project_id: str) -> DirectoryListing:
        response = self._get(f"/projects/{project_id}")
        json: dict = response.json()
        return directory_dict_to_directory_listing(json)


def directory_dict_to_directory_listing(directory: dict):
    return DirectoryListing(
        directory["storage_id"],
        directory["path"],
        [
            directory_dict_to_directory_listing(listing)
            if "storage_id" in listing
            else file_dict_to_file_listing(listing)
            for listing in directory["listings"]
        ],
    )


def file_dict_to_file_listing(file: dict):
    return FileListing(
        file["filename"],
        file["modification_date"],
        file["creation_date"],
        file["file_size"],
        file["nonce"],
    )


def project_dict_to_project(project: dict):
    return Project(
        project["id"],
        project["name"],
        project["description"],
        project["source_storage_id"],
        project["source_path"],
        project["destination_storage_id"],
        project["destination_path"],
        project["user_id"],
        project["creation_timestamp"],
    )
