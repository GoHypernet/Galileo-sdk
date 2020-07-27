from galileo_sdk.compat import urlunparse, requests

from galileo_sdk.business.objects.projects import (
    DirectoryListing,
    FileListing,
    Project,
    ProjectType,
    HECRASProject,
    PythonProject,
    JuliaProject,
    RProject,
    STATAProject,
    OctaveProject,
    SWMM5Project,
    AutoDockVinaProject,
    BioconductorProject,
    BlenderProject,
    QuantumEspressoProject,
    MatLabProject,
    FLO2DProject,
)
from galileo_sdk.data.repositories.jobs import (
    job_dict_to_job,
    file_dict_to_file_listing,
)


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

    def _delete(self, *args, **kwargs):
        return self._request(requests.delete, *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request(requests.put, *args, **kwargs)

    def list_projects(self, query):
        response = self._get("/projects", query=query)
        json = response.json()
        projects = json["projects"]
        return [project_dict_to_project(project) for project in projects]

    def create_project(self, create_project_request):
        body = {
            "name": create_project_request.name,
            "description": create_project_request.description,
            "source_storage_id": create_project_request.source_storage_id,
            "destination_storage_id": create_project_request.destination_storage_id,
            "source_path": create_project_request.source_path,
            "destination_path": create_project_request.destination_path,
            "project_type_id": create_project_request.project_type_id,
        }
        self._add_project_type_params(body, create_project_request)
        response = self._post("/projects", body)
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

    def run_job_on_lz(self, project_id, station_id, lz_id):
        response = self._post(
            "/projects/{project_id}/jobs".format(project_id=project_id),
            data={"station_id": station_id, "machine_id": lz_id},
        )
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def get_project_files(self, project_id):
        response = self._get(
            "/projects/{project_id}/files".format(project_id=project_id)
        )
        json = response.json()
        json = json["files"]
        return [file_dict_to_file_listing(file) for file in json]

    def delete_project(self, project_id):
        self._delete("/projects/{project_id}".format(project_id=project_id))
        return project_id

    def update_project(self, project_id, update_project_request):
        response = self._put(
            "/projects/{project_id}".format(project_id=project_id),
            data={
                "name": update_project_request.name,
                "description": update_project_request.description,
                "source_storage_id": update_project_request.source_storage_id,
                "source_path": update_project_request.source_path,
                "destination_path": update_project_request.destination_path,
                "settings": update_project_request.settings,
            },
        )
        json = response.json()
        return True

    def delete_project_files(self, project_id):
        self._delete("projects/{project_id}".format(project_project_id=project_id))
        return project_id

    def get_project_types(self):
        response = self._get("/projecttypes/summaries")
        json = response.json()
        projecttypes = json["project_types"]
        return [
            projecttype_dict_to_projecttype(projecttype) for projecttype in projecttypes
        ]

    def _add_project_type_params(self, body, create_project_request):
        if isinstance(create_project_request, HECRASProject):
            body["plan"] = create_project_request.plan
            body["files_to_run"] = create_project_request.files_to_run
            body["nfs"] = create_project_request.nfs
            body["input_path"] = create_project_request.input_path
            body["output_path"] = create_project_request.output_path
        elif (
            isinstance(create_project_request, PythonProject)
            or isinstance(create_project_request, JuliaProject)
            or isinstance(create_project_request, STATAProject)
        ):
            body["filename"] = create_project_request.filename
            body["cpu"] = create_project_request.cpu_count
            body["arg"] = (create_project_request.arg,)
            body["dependencies"] = {
                dependency.name: dependency.version
                for dependency in create_project_request.dependencies
            }
            body["env"] = create_project_request.env
        elif isinstance(create_project_request, RProject):
            body["filename"] = create_project_request.filename
            body["cpu"] = create_project_request.cpu_count
            body["arg"] = create_project_request.arg
            body["dependencies"] = (
                {
                    dependency.name: dependency.version
                    for dependency in create_project_request.dependencies
                }
                if create_project_request.dependencies
                else {}
            )
            body["cran_dependencies"] = (
                {
                    dependency.name: dependency.version
                    for dependency in create_project_request.dependencies
                }
                if create_project_request.cran_dependencies
                else {}
            )
            body["env"] = create_project_request.env
        elif (
            isinstance(create_project_request, SWMM5Project)
            or isinstance(create_project_request, QuantumEspressoProject)
            or isinstance(create_project_request, MatLabProject)
            or isinstance(create_project_request, FLO2DProject)
        ):
            body["filename"] = create_project_request.filename
        elif isinstance(create_project_request, OctaveProject):
            body["filename"] = create_project_request.filename
            body["dependencies"] = {
                dependency.name: dependency.version
                for dependency in create_project_request.dependencies
            }
            body["arg"] = create_project_request.arg
        elif isinstance(create_project_request, AutoDockVinaProject):
            body["FILENAME"] = create_project_request.filename
        elif isinstance(create_project_request, BioconductorProject):
            pass
        elif isinstance(create_project_request, BlenderProject):
            body["copy_in_path"] = create_project_request.copy_in_path
            body["copy_container_path"] = create_project_request.copy_container_path


def projecttype_dict_to_projecttype(projecttype):
    return ProjectType(
        projecttype["id"],
        projecttype["name"],
        projecttype["description"],
        projecttype["version"],
    )


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
        project["project_type_id"],
    )
