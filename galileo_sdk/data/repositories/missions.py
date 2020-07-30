from datetime import datetime

from galileo_sdk.business.objects.missions import DirectoryListing, Mission, MissionType
from galileo_sdk.business.objects import EJobStatus, Job, JobStatus
from galileo_sdk.business.objects.missions import FileListing
from galileo_sdk.data.repositories import RequestsRepository


class MissionsRepository(RequestsRepository):
    def __init__(
        self, settings_repository, auth_provider, namespace,
    ):
        super(MissionsRepository, self).__init__(
            settings_repository=settings_repository,
            auth_provider=auth_provider,
            namespace=namespace,
        )

    def list_missions(self, query):
        response = self._get("/projects", query=query)
        json = response.json()
        projects = json["projects"]
        return [project_dict_to_project(project) for project in projects]

    def create_mission(self, create_project_request):
        body = {
            "name": create_project_request.name,
            "description": create_project_request.description,
            "source_storage_id": create_project_request.source_storage_id,
            "destination_storage_id": create_project_request.destination_storage_id,
            "source_path": create_project_request.source_path,
            "destination_path": create_project_request.destination_path,
            "project_type_id": create_project_request.project_type_id,
        }
        response = self._post("/projects", body)
        json = response.json()
        project = json["project"]
        return project_dict_to_project(project)

    def upload_single_file(self, mission_id, file, filename):
        r = self._post(
            "/projects/{project_id}/files".format(project_id=mission_id),
            files=file,
            filename=filename,
        )
        return r.json()

    def run_job_on_station(self, mission_id, station_id):
        response = self._post(
            "/projects/{project_id}/jobs".format(project_id=mission_id),
            data={"station_id": station_id},
        )
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def run_job_on_lz(self, mission_id, station_id, lz_id):
        response = self._post(
            "/projects/{project_id}/jobs".format(project_id=mission_id),
            data={"station_id": station_id, "machine_id": lz_id},
        )
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def get_mission_files(self, mission_id):
        response = self._get(
            "/projects/{project_id}/files".format(project_id=mission_id)
        )
        json = response.json()
        json = json["files"]
        return [file_dict_to_file_listing(file) for file in json]

    def delete_mission(self, mission_id):
        response = self._delete("/projects/{project_id}".format(project_id=mission_id))
        return response.json()

    def update_mission(self, update_project_request):
        response = self._put(
            "/projects/{project_id}".format(
                project_id=update_project_request.mission_id
            ),
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
        return json

    def delete_file(self, mission_id, query):
        self._delete(
            "projects/{project_id}/files".format(project_id=mission_id), query=query
        )
        return mission_id

    def list_mission_types(self):
        response = self._get("/projecttypes/summaries")
        json = response.json()
        projecttypes = json["project_types"]
        return [
            projecttype_dict_to_projecttype(projecttype) for projecttype in projecttypes
        ]

    def get_mission_type(self, mission_type_id):
        response = self._get(
            "/projecttypes/{mission_type_id}".format(mission_type_id=mission_type_id)
        )
        return projecttype_dict_to_projecttype(response)


def projecttype_dict_to_projecttype(projecttype):
    return MissionType(
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
    return Mission(
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


def file_dict_to_file_listing(file):
    return FileListing(
        file["filename"],
        file["path"],
        file.get("modification_date", None),
        file.get("creation_date", None),
        file.get("file_size", None),
        file.get("nonce", None),
    )


def job_dict_to_job(job):
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


def job_status_dict_to_job_status(job_status):
    status = JobStatus(
        datetime.fromtimestamp(job_status["timestamp"]),
        EJobStatus[job_status["status"]],
    )
    status.jobstatusid = (
        job_status["jobstatusid"] if "jobstatusid" in job_status else None
    )
    status.jobid = job_status["jobid"] if "jobid" in job_status else None
    return status
