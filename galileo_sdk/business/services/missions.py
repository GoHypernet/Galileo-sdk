import os

from ..utils.generate_query_str import generate_query_str
from ..objects import UpdateMissionRequest
from galileo_sdk.compat import quote


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
        archived=None
    ):
        query = generate_query_str(
            {
                "ids": ids,
                "names": names,
                "user_ids": user_ids,
                "page": page,
                "items": items,
                "mission_type_ids": mission_type_ids,
                "archived": archived
            }
        )

        return self._missions_repo.list_missions(query)

    def get_mission_by_id(self, mission_id):
        query = generate_query_str({"ids": mission_id})

        return self._missions_repo.list_missions(query)[0]

    def create_mission(self, request):
        return self._missions_repo.create_mission(request)

    def create_mission_and_run_job(
        self, request, directory, station_id, lz_id=None, cpu_count=None, memory_amount=None, gpu_count=None
    ):
        mission = self.create_mission(request)
        self.upload(mission.mission_id, directory)
        if lz_id:
            job = self.run_job_on_lz(mission.mission_id, station_id, lz_id, cpu_count, memory_amount, gpu_count)
        else:
            job = self.run_job_on_station(mission.mission_id, station_id, cpu_count=cpu_count, memory_amount=memory_amount, gpu_count=gpu_count)

        return job

    def upload(self, mission_id, payload, rename=None, verbose=False):
        try:
            if not os.path.exists(payload):
                if verbose:
                    print("Payload is not a directory or file")
                return False
            
            name = os.path.basename(payload)
            if os.path.isdir(payload):
                for root, dirs, files in os.walk(payload):
                    for file in files:
                        basename = os.path.basename(root)
                        filepath = os.path.join(os.path.abspath(root), file)
                        if basename == name:
                            filename = file
                        else:
                            filename = os.path.relpath(filepath, payload)
 
                        f = open(filepath, "rb").read()
                        self._missions_repo.upload_single_file(mission_id, f, filename)
                        if verbose:
                            print(" Upload complete: ", filename)
            else:
                f = open(payload, "rb").read()
                if rename:
                    name = rename
                self._missions_repo.upload_single_file(mission_id, f, name)
                if verbose:
                    print("Upload complete: ", name)
            return True
        except Exception as e:
            print("Error: ", e)
            return False

    def run_job_on_station(self, mission_id, station_id, cpu_count=None, memory_amount=None, gpu_count=None):
        return self._missions_repo.run_job_on_station(mission_id, station_id, cpu_count, memory_amount, gpu_count)

    def run_job_on_lz(self, mission_id, station_id, lz_id, cpu_count=None, memory_amount=None, gpu_count=None):
        return self._missions_repo.run_job_on_lz(mission_id, station_id, lz_id, cpu_count, memory_amount, gpu_count)

    def get_mission_files(self, mission_id):
        return self._missions_repo.get_mission_files(mission_id)

    def delete_mission(self, mission_id):
        return self._missions_repo.delete_mission(mission_id)

    def update_mission(self, update_mission_request):
        try:
            response = self._missions_repo.update_mission(update_mission_request)
            return True
        except Exception as e:
            print("Error: ", e)
            return False

    def update_mission_args(self, mission_id, arg):
        missions = self.list_missions(ids=[mission_id])
        mission = missions[0]
        mission.settings["arg"] = arg
        if not isinstance(arg, list):
            raise Exception(
                "args must be in the form of a List[str] e.g. ['arg1', 'arg2', 'arg3']"
            )
        update_mission_request = UpdateMissionRequest(
            mission_id=mission_id, settings=mission.settings
        )
        return self._missions_repo.update_mission(update_mission_request)

    def delete_file(self, mission_id, filename):
        try:
            query = generate_query_str({"filename": quote(filename, safe="")})
            response = self._missions_repo.delete_file(mission_id, query)
            
            return True
        except Exception as e:
            print("Error: ", e)
            return False

    def list_mission_types(self):
        return self._missions_repo.list_mission_types()

    # extend this function when new widget types are added to the docker wizard
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
            elif dict_type == "single-select":
                dict_type = []
                for option in wizard_spec.get('options', None):
                    dict_type.append(option.get('value', None))

            if dict_key == "dependencies":
                dict_type = "Dict[str, str], e.g. {'dependency1': 'version1', 'dependency2': 'version2'}"

            settings[dict_key] = dict_type

        for key, value in wizard_spec.items():
            if type(value) == type(list()):
                for v in value:
                    self._parse_wizard_spec(v, settings)

    def _get_settings(self, wizard_spec_pages):
        settings = {}
        for page in wizard_spec_pages:
            self._parse_wizard_spec(page, settings)

        return settings

    def get_mission_type(self, mission_type_id):
        query = generate_query_str({"ids": mission_type_id})
        return self._missions_repo.get_mission_type(query)

    def get_mission_type_settings_info(self, mission_type_id):
        mission_type = self.get_mission_type(mission_type_id)
        return self._get_settings(mission_type.wizard_spec)
