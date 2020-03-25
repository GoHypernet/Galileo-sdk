from galileo_sdk.compat import urlunparse, requests

from galileo_sdk.business.objects.projects import (DirectoryListing,
                                                   FileListing, Project)
from galileo_sdk.data.repositories.jobs import job_dict_to_job


class ProjectsRepository:
    def __init__(
        self, settings_repository, auth_provider, namespace,
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider
        self._namespace = namespace

    def _make_url(self, endpoint, params="", query="", fragment=""):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse(
            (
                schema,
                "{addr}{namespace}".format(addr=addr, namespace=self._namespace),
                endpoint,
                params,
                query,
                fragment,
            )
        )

    def _request(
        self,
        request,
        endpoint,
        data=None,
        params=None,
        query=None,
        fragment=None,
        files=None,
        filename=None,
    ):
        url = self._make_url(endpoint, params, query, fragment)
        access_token = self._auth_provider.get_access_token()
        headers = {
            "Authorization": "Bearer {access_token}".format(access_token=access_token)
        }

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

    def list_projects(self, query):
        response = self._get("/projects", query=query)
        json = response.json()
        projects = json["projects"]
        return [project_dict_to_project(project) for project in projects]

    def create_project(self, name, description):
        response = self._post("/projects", {"name": name, "description": description})
        json = response.json()
        project = json["project"]
        return project_dict_to_project(project)

    def upload_single_file(self, project_id, file, filename):
        r = self._post(
            "/projects/{project_id}/files".format(project_id=project_id),
            files=file,
            filename=filename,
        )
        return r.json()

    def run_job_on_station(self, project_id, station_id):
        response = self._post(
            "/projects/{project_id}/jobs".format(project_id=project_id),
            data={"station_id": station_id},
        )
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def run_job_on_machine(self, project_id, station_id, machine_id):
        response = self._post(
            "/projects/{project_id}/jobs".format(project_id=project_id),
            data={"station_id": station_id, "machine_id": machine_id},
        )
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def inspect_project(self, project_id):
        response = self._get("/projects/{project_id}".format(project_id=project_id))
        json = response.json()
        return directory_dict_to_directory_listing(json)


def directory_dict_to_directory_listing(directory):
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


def file_dict_to_file_listing(file):
    return FileListing(
        file["filename"],
        file["modification_date"],
        file["creation_date"],
        file["file_size"],
        file["nonce"],
    )


def project_dict_to_project(project):
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
