import os

from ..utils.generate_query_str import generate_query_str
from ..objects import UpdateMissionRequest, CreateMissionRequest


class MissionsService:
    def __init__(self, missions_repo):
        self._missions_repo = missions_repo

    def list_missions(
        self,
        ids=None,
        names=None,
        user_ids=None,
        page=1,
        items=25,
        mission_type_ids=None,
    ):
        query = generate_query_str(
            {
                "ids": ids,
                "names": names,
                "user_ids": user_ids,
                "page": page,
                "items": items,
                "project_type_id": mission_type_ids,
            }
        )

        return self._missions_repo.list_missions(query)

    def create_mission(
        self,
        name,
        description="",
        source_storage_id=None,
        destination_storage_id=None,
        source_path=None,
        destination_path=None,
        mission_type_id=None,
        settings=None,
    ):
        return self._missions_repo.create_mission(
            CreateMissionRequest(
                name=name,
                description=description,
                source_storage_id=source_storage_id,
                destination_storage_id=destination_storage_id,
                source_path=source_path,
                destination_path=destination_path,
                mission_type_id=mission_type_id,
                settings=settings,
            )
        )

    def create_mission_and_run_job(
        self,
        name,
        directory,
        station_id,
        lz_id=None,
        description="",
        source_storage_id=None,
        destination_storage_id=None,
        source_path=None,
        destination_path=None,
        mission_type_id=None,
        settings=None,
    ):
        mission = self.create_mission(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            source_path=source_path,
            destination_path=destination_path,
            mission_type_id=mission_type_id,
            settings=settings,
        )
        self.upload(mission.mission_id, directory)
        if lz_id:
            job = self.run_job_on_lz(mission.mission_id, station_id, lz_id)
        else:
            job = self.run_job_on_station(mission.mission_id, station_id)

        return job

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

    def delete_file(self, mission_id, file):
        return self._missions_repo.delete_file(mission_id, file)

    def list_mission_types(self):
        return self._missions_repo.list_mission_types()

    def _parse_wizard_spec(self, wizard_spec, settings):
        dict_key = wizard_spec.get("key", None)
        dict_type = wizard_spec.get("type", None)
        if dict_key and dict_type and dict_key != "dependency":
            # Rename types to standard Python types
            if dict_type == "checkbox":
                dict_type = "bool"
            elif dict_type == "text":
                dict_type = "str"
            elif dict_type == "number":
                dict_type = "int"

            if dict_key == "dependencies":
                dict_type = "Dict[str, str], e.g. {'dependency1': 'version1', 'dependency2': 'version2'}"

            settings[dict_key] = dict_type

        for key, value in wizard_spec.items():
            if type(value) == type(list()):
                for v in value:
                    self._parse_wizard_spec(v, settings)

    def _get_settings(self, wizard_spec_pages):
        settings = []
        for page in wizard_spec_pages:
            self._parse_wizard_spec(page, settings)

        return settings

    def get_mission_type(self, mission_type_id):
        return self._missions_repo.get_mission_type(mission_type_id)

    def get_mission_type_settings_info(self, mission_type_id):
        mission_type = self.get_mission_type(mission_type_id)
        return self._get_settings(mission_type["wizard_spec"])
