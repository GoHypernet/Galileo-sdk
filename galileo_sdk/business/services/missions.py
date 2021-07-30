import os

from ..utils.generate_query_str import generate_query_str
from ..objects import UpdateMissionRequest
from galileo_sdk.compat import quote


#TODO Replace some bool return types with Success objects
class MissionsService:
    def __init__(self, missions_repo):
        """
        Mission Service

        :param missions_repo: Mission repository
        :type missions_repo: MissionsRepository
        """
        self._missions_repo = missions_repo

    def list_missions(self,
                      mission_ids=None,
                      names=None,
                      user_ids=None,
                      page=1,
                      items=25,
                      mission_type_ids=None,
                      archived=None):
        """
        List filtered missions

        :param mission_ids: Filter by mission ids, defaults to None
        :type mission_ids: List[str], optional
        :param names: Filter by mission names, defaults to None
        :type names: List[str], optional
        :param user_ids: Filter by users, defaults to None
        :type user_ids: List[str], optional
        :param page: Current page of results, defaults to 1
        :type page: int, optional
        :param items: Number of items per page, defaults to 25
        :type items: int, optional
        :param mission_type_ids: Filter by mission type, defaults to None
        :type mission_type_ids: List[str], optional
        :param archived: Filter by archived missions, defaults to None
        :type archived: bool, optional
        :return: Filtered missions
        :rtype: List[Mission]
        """
        query = generate_query_str({
            "ids": mission_ids,
            "names": names,
            "user_ids": user_ids,
            "page": page,
            "items": items,
            "mission_type_ids": mission_type_ids,
            "archived": archived
        })

        return self._missions_repo.list_missions(query)

    def get_mission_by_id(self, mission_id):
        """
        Get mission by id

        :param mission_id: Mission id of the mission to get
        :type mission_id: str
        :return: Selected mission object
        :rtype: Mission
        """
        query = generate_query_str({"ids": mission_id})

        return self._missions_repo.list_missions(query)[0]

    def create_mission(self, request):
        """
        Create a new mission

        :param request: Create mission request
        :type request: CreateMissionRequest
        :return: New mission
        :rtype: Mission
        """
        return self._missions_repo.create_mission(request)

    def create_mission_and_run_job(self,
                                   request,
                                   directory,
                                   station_id,
                                   lz_id=None,
                                   cpu_count=None,
                                   memory_amount=None,
                                   gpu_count=None):
        """
        Create a new mission and run a job on a station 

        :param request: Create mission request
        :type request: CreateMissionRequest
        :param directory: Job folder to run
        :type directory: str
        :param station_id: Station id to run the job on
        :type station_id: str 
        :param lz_id: Specific LZ to run the job on, defaults to None
        :type lz_id: str, optional
        :param cpu_count: Cpu count to run the job with, defaults to None
        :type cpu_count: number, optional
        :param memory_amount: Memory amount to run the job with, defaults to None
        :type memory_amount: number, optional
        :param gpu_count: GPU count to run the job with, defaults to None
        :type gpu_count: number, optional
        :return: Job that was run
        :rtype: Job
        """
        mission = self.create_mission(request)
        self.upload(mission.mission_id, directory)
        if lz_id:
            job = self.run_job_on_lz(mission.mission_id, station_id, lz_id,
                                     cpu_count, memory_amount, gpu_count)
        else:
            job = self.run_job_on_station(mission.mission_id,
                                          station_id,
                                          cpu_count=cpu_count,
                                          memory_amount=memory_amount,
                                          gpu_count=gpu_count)

        return job

    def upload(self, mission_id, payload, rename=None, verbose=False):
        """
        Upload a folder to a mission

        :param mission_id: Mission id of the mission to upload to
        :type mission_id: str
        :param payload: Path to the folder to upload
        :type payload: str
        :param rename: Renamed folder, defaults to None
        :type rename: str, optional
        :param verbose: Verbose output, defaults to False
        :type verbose: bool, optional
        :return: Succesfully uploaded files
        :rtype: bool
        """
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
                        self._missions_repo.upload_single_file(
                            mission_id, f, filename)
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

    def run_job_on_station(self,
                           mission_id,
                           station_id,
                           cpu_count=None,
                           memory_amount=None,
                           gpu_count=None):
        """
        Run a job on a station
        
        :param mission_id: Mission id of the mission to run the job on
        :type mission_id: str
        :param station_id: Station id of the station to run the job on
        :type station_id: str
        :param cpu_count: Cpu count to run the job with, defaults to None
        :type cpu_count: number, optional
        :param memory_amount: Memory amount to run the job with, defaults to None
        :type memory_amount: number, optional
        :param gpu_count: GPU count to run the job with, defaults to None
        :type gpu_count: number, optional
        :return: Job that was run
        :rtype: Job 
        """
        return self._missions_repo.run_job_on_station(mission_id, station_id,
                                                      cpu_count, memory_amount,
                                                      gpu_count)

    def run_job_on_lz(self,
                      mission_id,
                      station_id,
                      lz_id,
                      cpu_count=None,
                      memory_amount=None,
                      gpu_count=None):
        """
        Run a job on a specific LZ

        :param mission_id: Mission id of the mission to run the job on
        :type mission_id: str
        :param station_id: Station id of the station to run the job on
        :type station_id: str
        :param lz_id: Specific LZ to run the job on
        :type lz_id: str
        :param cpu_count: Cpu count to run the job with, defaults to None
        :type cpu_count: number, optional
        :param memory_amount: Memory amount to run the job with, defaults to None
        :type memory_amount: number, optional
        :param gpu_count: GPU count to run the job with, defaults to None
        :type gpu_count: number, optional
        :return: Job that was run
        :rtype: Job 
        """
        return self._missions_repo.run_job_on_lz(mission_id, station_id, lz_id,
                                                 cpu_count, memory_amount,
                                                 gpu_count)

    def get_mission_files(self, mission_id):
        """
        Get files for/from a mission

        :param mission_id: Mission id of the mission to get files for/from
        :type mission_id: str
        :return: Files for/from the mission
        :rtype: List[FileListing]

        """
        return self._missions_repo.get_mission_files(mission_id)

    def delete_mission(self, mission_id):
        """
        Delete a mission

        :param mission_id: Mission id of the mission to delete
        :type mission_id: str
        :return: True if mission was deleted, False otherwise
        :rtype: bool
        """
        return self._missions_repo.delete_mission(mission_id)

    # TODO: Is this desired return type?
    def update_mission(self, update_mission_request):
        """
        Update a mission

        :param update_mission_request: Update mission request
        :type update_mission_request: UpdateMissionRequest
        :return: Successful update
        :rtype: bool
        """
        try:
            response = self._missions_repo.update_mission(
                update_mission_request)
            return True
        except Exception as e:
            print("Error: ", e)
            return False

    def update_mission_args(self, mission_id, arg):
        """
        Update mission args

        :param mission_id: Mission id of the mission to update
        :type mission_id: str
        :param arg: Argument to update
        :type arg: List[str]
        :return: True if mission args were updated, False otherwise
        :rtype: bool

        """
        missions = self.list_missions(mission_ids=[mission_id])
        mission = missions[0]
        mission.settings["arg"] = arg
        if not isinstance(arg, list):
            raise Exception(
                "args must be in the form of a List[str] e.g. ['arg1', 'arg2', 'arg3']"
            )
        update_mission_request = UpdateMissionRequest(
            mission_id=mission_id, settings=mission.settings)
        return self._missions_repo.update_mission(update_mission_request)

    def delete_file(self, mission_id, filename):
        """
        Delete a file from a mission

        :param mission_id: Mission id of the mission to delete the file from
        :type mission_id: str
        :param filename: Filename to delete
        :type filename: str
        :return: True if file was deleted, False otherwise
        :rtype: bool

        """
        try:
            query = generate_query_str({"filename": quote(filename, safe="")})
            response = self._missions_repo.delete_file(mission_id, query)

            return True
        except Exception as e:
            print("Error: ", e)
            return False

    def list_mission_types(self):
        """
        List mission types

        :return: All mission types
        :rtype: List[MissionType]
        """
        return self._missions_repo.list_mission_types()

    # extend this function when new widget types are added to the docker wizard
    def _parse_wizard_spec(self, wizard_spec, settings):
        """
        parse the wizard spec if into dependencies and settings

        :param wizard_spec: Mission wizard spec
        :type wizard_spec: Dict
        :param settings: Mission settings
        :type settings: Dict

        #TODO: Recurively parse the settings and dependencies?
        """
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
        """
        Get the settings for the mission

        :param wizard_spec_pages: Wizard spec pages
        :type wizard_spec_pages: Dict? #TODO Double Check
        :return: Settings for the mission
        :rtype: Dict
        """
        settings = {}
        for page in wizard_spec_pages:
            self._parse_wizard_spec(page, settings)

        return settings

    def get_mission_type(self, mission_type_id):
        """
        Gets a mission type

        :param mission_type_id: Mission type ID of the mission
        :type mission_type_id: str
        :return: Get a mission type
        :rtype: MissionType
        """
        if not mission_type_id:
            raise Exception("Mission type ID must be provided")
        query = generate_query_str({"ids": [mission_type_id]})
        return self._missions_repo.get_mission_type(query)

    def get_mission_type_settings_info(self, mission_type_id):
        """
        Gets mission type settings

        :param mission_type_id: Mission ID to get settings from
        :type mission_type_id: str
        :return: Dict of mission type settings
        :rtype: Dict
        """
        mission_type = self.get_mission_type(mission_type_id)
        return self._get_settings(mission_type.wizard_spec)
