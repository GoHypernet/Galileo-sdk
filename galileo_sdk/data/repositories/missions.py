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
        missions = json["projects"]
        return [mission_dict_to_mission(mission) for mission in missions]

    def create_mission(self, create_mission_request):
        body = {
            "name": create_mission_request.name,
            "description": create_mission_request.description,
            "source_storage_id": create_mission_request.source_storage_id,
            "destination_storage_id": create_mission_request.destination_storage_id,
            "source_path": create_mission_request.source_path,
            "destination_path": create_mission_request.destination_path,
            "mission_type_id": create_mission_request.mission_type_id,
            "public": create_mission_request.public,
        }
        if create_mission_request.settings is not None:
            body.update(create_mission_request.settings)
        response = self._post("/projects", data=body)
        json = response.json()
        mission = json["project"]
        return mission_dict_to_mission(mission)

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
            "destination_storage_id": update_project_request.destination_storage_id,
            "source_path": update_project_request.source_path,
            "destination_path": update_project_request.destination_path,
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
        missiontypes = json["project_types"]
        return [
            missiontype_dict_to_missiontype(missiontype) for missiontype in missiontypes
        ]

    def get_mission_type(self, query):
        response = self._get("/projecttypes", query=query)
        json = response.json()
        missiontypes = json["projecttypes"]
        return missiontype_dict_to_missiontype(missiontypes[0])


def missiontype_dict_to_missiontype(missiontype):
    return MissionType(
        missiontype["id"],
        missiontype["name"],
        missiontype["description"],
        missiontype["version"],
        missiontype.get("active", None),
        missiontype.get("container_type", None),
        missiontype.get("wizard_spec", None),
        missiontype.get("enable_tunnels", None),
        missiontype.get("generate_credentials", None),
        missiontype.get("distributed", None),
        missiontype.get("min_cpu_count", None),
        missiontype.get("max_cpu_count", None),
        missiontype.get("default_cpu_count", None),
        missiontype.get("min_memory_amount", None),
        missiontype.get("max_memory_amount", None),
        missiontype.get("default_memory_amount", None),
        missiontype.get("min_gpu_count", None),
        missiontype.get("max_gpu_count", None),
        missiontype.get("default_gpu_count", None),
        missiontype.get("logo_url", None),
        missiontype.get("credits_per_hour", None),
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


def mission_dict_to_mission(mission):
    return Mission(
        mission["id"],
        mission["name"],
        mission["description"],
        mission["source_storage_id"],
        mission["source_path"],
        mission["destination_storage_id"],
        mission["destination_path"],
        mission["user_id"],
        mission["creation_timestamp"],
        mission["mission_type_id"],
        mission.get("updated_timestamp", None),
        mission.get("organization_id", None),
        mission.get("settings", None),
        mission.get("mission_type_name"),
        mission.get("public", None)
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
        mission_id=job["mission_id"],
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
