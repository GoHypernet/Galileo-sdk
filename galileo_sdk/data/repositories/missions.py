from datetime import datetime

from galileo_sdk.business.objects.missions import (
    DirectoryListing,
    Mission,
    MissionType,
    HECRASMission,
    PythonMission,
    JuliaMission,
    RMission,
    STATAMission,
    OctaveMission,
    SWMM5Mission,
    AutoDockVinaMission,
    BioconductorMission,
    BlenderMission,
    QuantumEspressoMission,
    MatLabMission,
    FLO2DMission,
)
from galileo_sdk.business.objects import EJobStatus, Job, JobStatus, UpdateJobRequest
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
        self._add_project_type_params(body, create_project_request)
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
        self._delete("/projects/{project_id}".format(project_id=mission_id))
        return mission_id

    def update_mission(self, mission_id, update_project_request):
        response = self._put(
            "/projects/{project_id}".format(project_id=mission_id),
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

    def delete_mission_files(self, mission_id):
        self._delete("projects/{project_id}".format(project_project_id=mission_id))
        return mission_id

    def get_mission_types(self):
        response = self._get("/projecttypes/summaries")
        json = response.json()
        projecttypes = json["project_types"]
        return [
            projecttype_dict_to_projecttype(projecttype) for projecttype in projecttypes
        ]

    def _add_project_type_params(self, body, create_project_request):
        if isinstance(create_project_request, HECRASMission):
            body["plan"] = create_project_request.plan
            body["files_to_run"] = create_project_request.files_to_run
            body["nfs"] = create_project_request.nfs
            body["input_path"] = create_project_request.input_path
            body["output_path"] = create_project_request.output_path
        elif (
            isinstance(create_project_request, PythonMission)
            or isinstance(create_project_request, JuliaMission)
            or isinstance(create_project_request, STATAMission)
        ):
            body["filename"] = create_project_request.filename
            body["cpu"] = create_project_request.cpu_count
            body["arg"] = (create_project_request.arg,)
            body["dependencies"] = {
                dependency.name: dependency.version
                for dependency in create_project_request.dependencies
            }
            body["env"] = create_project_request.env
        elif isinstance(create_project_request, RMission):
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
            isinstance(create_project_request, SWMM5Mission)
            or isinstance(create_project_request, QuantumEspressoMission)
            or isinstance(create_project_request, MatLabMission)
            or isinstance(create_project_request, FLO2DMission)
        ):
            body["filename"] = create_project_request.filename
        elif isinstance(create_project_request, OctaveMission):
            body["filename"] = create_project_request.filename
            body["dependencies"] = {
                dependency.name: dependency.version
                for dependency in create_project_request.dependencies
            }
            body["arg"] = create_project_request.arg
        elif isinstance(create_project_request, AutoDockVinaMission):
            body["FILENAME"] = create_project_request.filename
        elif isinstance(create_project_request, BioconductorMission):
            pass
        elif isinstance(create_project_request, BlenderMission):
            body["copy_in_path"] = create_project_request.copy_in_path
            body["copy_container_path"] = create_project_request.copy_container_path


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
