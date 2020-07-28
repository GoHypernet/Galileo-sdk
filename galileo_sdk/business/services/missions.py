import os

from ..utils.generate_query_str import generate_query_str
from ..objects import UpdateMissionRequest, CreateMissionRequest


class MissionsService:
    def __init__(self, missions_repo):
        self._missions_repo = missions_repo

    def list_missions(
        self, ids=None, names=None, user_ids=None, page=1, items=25,
    ):
        query = generate_query_str(
            {
                "ids": ids,
                "names": names,
                "user_ids": user_ids,
                "page": page,
                "items": items,
            }
        )

        return self._missions_repo.list_missions(query)

    def create_mission(
        self,
        name,
        description="",
        source_storage_id=None,
        destination_storage_id=None,
        mission_type_name=None,
        source_path=None,
        destination_path=None,
        mission_type_id=None,
    ):

        # if not project_type_id:
        #     project_types = self.get_project_types()
        #     for project_type in project_types:
        #         if project_type.version == create_project_request.version and \
        #                 project_type.name == create_project_request.project_type_name:
        #             create_project_request.project_type_id = project_type.id
        #
        #     if not create_project_request.project_type_id:
        #         raise Exception("Version of this project type is not found")

        return self._missions_repo.create_mission(
            CreateMissionRequest(
                name,
                description,
                source_storage_id,
                destination_storage_id,
                mission_type_name,
                source_path,
                destination_path,
                mission_type_id,
            )
        )

    def upload(self, mission_id, dir):
        name = os.path.basename(dir)
        for root, dirs, files in os.walk(dir):
            for file in files:
                basename = os.path.basename(root)
                if basename == name:
                    filename = file
                else:
                    filename = os.path.join(os.path.basename(root), file)

                filename = filename.replace(" ", "_")

                filepath = os.path.join(os.path.abspath(root), file)
                f = open(filepath, "rb").read()
                self._missions_repo.upload_single_file(mission_id, f, filename)
        return True

    def run_job_on_station(self, mission_id, station_id):
        return self._missions_repo.run_job_on_station(mission_id, station_id)

    def run_job_on_lz(self, mission_id, station_id, lz_id):
        return self._missions_repo.run_job_on_lz(mission_id, station_id, lz_id)

    def get_mission_files(self, mission_id):
        return self._missions_repo.get_mission_files(mission_id)

    def delete_mission(self, mission_id):
        return self._missions_repo.delete_mission(mission_id)

    def update_mission(self, mission_id, update_mission_request):
        return self._missions_repo.update_mission(mission_id, update_mission_request)

    def update_mission_args(self, mission_id, args):
        update_mission_request = UpdateMissionRequest(
            None, None, None, None, None, args
        )
        return self._missions_repo.update_mission(mission_id, update_mission_request)

    def delete_mission_files(self, mission_id):
        return self._missions_repo.delete_mission_files(mission_id)

    def get_mission_types(self):
        return self._missions_repo.get_mission_types()
