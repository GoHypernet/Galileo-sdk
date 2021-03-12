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
            "public": create_project_request.public,
        }
        if create_project_request.settings is not None:
            body.update(create_project_request.settings)
        response = self._post("/projects", data=body)
        json = response.json()
        project = json["project"]
        return project_dict_to_project(project)

    def upload_single_file(self, mission_id, file, filename):
        r = self._post(
            "/projects/{mission_id}/files".format(mission_id=mission_id),
            files=file,
            filename=filename,
        )
        return r.json()

    def run_job_on_station(self, mission_id, station_id, cpu_count=None, memory_amount=None, gpu_count=None):
        response = self._post(
            "/projects/{mission_id}/jobs".format(mission_id=mission_id),
            data={"station_id": station_id, "cpu_count": cpu_count, "memory_amount": memory_amount, "gpu_count": gpu_count},
        )
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def run_job_on_lz(self, mission_id, station_id, lz_id, cpu_count=None, memory_amount=None, gpu_count=None):
        response = self._post(
            "/projects/{mission_id}/jobs".format(mission_id=mission_id),
            data={"station_id": station_id, "machine_id": lz_id, "cpu_count": cpu_count, "memory_amount": memory_amount, "gpu_count": gpu_count},
        )
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def get_mission_files(self, mission_id):
        response = self._get(
            "/projects/{mission_id}/files".format(mission_id=mission_id)
        )
        json = response.json()
        json = json["files"]
        return [file_dict_to_file_listing(file) for file in json]

    def delete_mission(self, mission_id):
        response = self._delete("/projects/{mission_id}".format(mission_id=mission_id))
        return response.json()

    def update_mission(self, update_project_request):
        body = {
            "id": update_project_request.mission_id,
            "name": update_project_request.name,
            "description": update_project_request.description,
            "source_storage_id": update_project_request.source_storage_id,
            "source_path": update_project_request.source_path,
            "destination_path": update_project_request.destination_path,
            "public":update_project_request.public
        }
        if update_project_request.settings is not None:
            body.update({"settings": update_project_request.settings})

        response = self._put(
            "/projects/{mission_id}".format(
                mission_id=update_project_request.mission_id
            ),
            data=body,
        )
        json = response.json()
        return json

    def delete_file(self, mission_id, query):
        self._delete(
            "projects/{mission_id}/files".format(mission_id=mission_id), query=query
        )
        return mission_id

    def list_mission_types(self):
        response = self._get("/projecttypes/summaries")
        json = response.json()
        projecttypes = json["project_types"]
        return [
            projecttype_dict_to_projecttype(projecttype) for projecttype in projecttypes
        ]

    def get_mission_type(self, query):
        response = self._get("/projecttypes", query=query)
        json = response.json()
        projecttype = json["projecttypes"]
        return projecttype_dict_to_projecttype(projecttype[0])


def projecttype_dict_to_projecttype(projecttype):
    return MissionType(
        projecttype["id"],
        projecttype["name"],
        projecttype["description"],
        projecttype["version"],
        projecttype.get("active", None),
        projecttype.get("container_type", None),
        projecttype.get("wizard_spec", None),
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
        project["mission_type_id"],
        project.get("updated_timestamp", None),
        project.get("organization_id", None),
        project.get("settings", None),
        project.get("mission_type_name"),
        project.get("public", None)
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
        jobid=job["jobid"],
        receiverid=job["receiverid"],
        project_id=job["project_id"],
        time_created=datetime.fromtimestamp(job["time_created"]),
        last_updated=datetime.fromtimestamp(job["last_updated"]),
        status=job["status"],
        name=job["name"],
        cpu_count=job["cpu_count"],
        gpu_count=job["gpu_count"],
        memory_amount=job["memory_amount"],
        enable_tunnel=job["enable_tunnel"],
        tunnel_url=job["tunnel_url"],
        tunnel_port=job["tunnel_port"],
        stationid=job["stationid"],
        userid=job["userid"],
        state=job["state"],
        pay_status=job["pay_status"],
        pay_interval=job["pay_interval"],
        total_runtime=job["total_runtime"],
        archived=job["archived"],
        status_history=[
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
