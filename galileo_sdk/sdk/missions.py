from ..business.objects.missions import UpdateMissionRequest, CreateMissionRequest


class MissionsSdk:
    def __init__(self, missions_service):
        self._missions_service = missions_service

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
        """
        Get list of Missions associated with your account

        :param ids: Optional[List[str]]: Filter by Mission UUID
        :param names: Optional[List[str]]: Filter by Mission name
        :param user_ids: Optional[List[str]]: Filter by user UUID
        :param page: Optional[int]: Return a particular page number
        :param items: Optional[int]: Number of Missions to return per page
        :param mission_type_ids: Optional[List[str]]: Filter by mission_type_ids
        :param archived: Optional[bool]: Filter for archived projects
        :return: List[Mission]
        
        Example:
            >>> missions = galileo.missions.list_missions(items=10)
            >>> for mission in missions:
            >>>    print(mission.name)
        """
        return self._missions_service.list_missions(
            ids=ids,
            names=names,
            user_ids=user_ids,
            page=page,
            items=items,
            mission_type_ids=mission_type_ids,
            archived=archived
        )

    def get_mission_by_id(self, mission_id):
        """
        Get a specific Mission's details by providing its UUID
        
        :param mission_id: str: Mission UUID
        :return: Mission
        
        Example:
            >>> UUID = '3f571a99-783e-49d9-a218-c32ffcb81899'
            >>> mission = galileo.missions.get_mission_by_id(mission_id=UUID)
            >>> print(mission.name)
        """
        return self._missions_service.get_mission_by_id(mission_id)

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
        """
        Create a mission

        :param name: str: Human readable name of the Mission you are creating
        :param description: Optional[str]: Optional description of the Mission you are creating
        :param mission_type_id: Optional[str]: UUID of the Mission framework type you are creating
        :param destination_path: Optional[str]: Root directory of the Mission in the specified source Cargo Bay (not needed if using default storage)
        :param source_path: Optional[str]: Root directory of the Mission in the specified destinatino Cargo Bay (not needed if using default storage)
        :param destination_storage_id: Optional[str]: UUID of the Cargo Bay to use as the Mission data destination
        :param source_storage_id: Optional[str]: UUID of the Cargo Bay to use as the Mission data source
        :param settings: Optional[Dict[str, str]]: Mission framework type settings (get this info from get_mission_type_settings_info)
         missions.get_mission_type_settings_info()
        :return: Mission
        
        Example:
            >>> new_mission = galileo.missions.create_mission(name='My Mission',description='This creates and empty Mission with no framework type')
        """
        request = CreateMissionRequest(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            source_path=source_path,
            destination_path=destination_path,
            mission_type_id=mission_type_id,
            settings=settings,
        )
        return self._missions_service.create_mission(request)

    def upload(self, mission_id, directory):
        """
        Uplood a

        :param mission_id: str: Mission you want to upload the file to
        :param directory: str: Path to folder that you want to upload
        :return: bool
        """
        return self._missions_service.upload(mission_id, directory)

    def run_job_on_station(self, mission_id, station_id, cpu_count=None, memory_amount=None, gpu_count=None):
        """
        Run a job on a station

        Example::

            galileo.missions.run_job_on_station(mission.mission_id,station.stationid,cpu_count=1,memory_amount=1048)

        :param mission_id: str: Reference ID of Mission to launch job from
        :param station_id: str: Reference ID of the Station to deploy job to
        :param cpu_count: int: Number of cpus for this job to request
        :param memory_amount: int: Memory in MB for this job to request
        :param gpu_count: int: Number of gpus for this job to request
        :return: Job
        """
        return self._missions_service.run_job_on_station(mission_id, station_id, cpu_count=cpu_count, memory_amount=memory_amount, gpu_count=gpu_count)

    def run_job_on_lz(self, mission_id, station_id, lz_id, cpu_count=None, memory_amount=None, gpu_count=None):
        """
        Run a job on a landing zone

        Example::

            galileo.missions.run_job_on_lz(mission.mission_id,station.stationid,lzid,cpu_count=1,memory_amount=1048)

        :param mission_id: str: Reference ID of Mission to launch job from
        :param station_id: str: Reference ID of the Station to deploy job to
        :param lz_id: str: Reference ID of specific LZ to deploy to
        :param cpu_count: int: Number of cpus for this job to request
        :param memory_amount: int: Memory in MB for this job to request
        :param gpu_count: int: Number of gpus for this job to request
        :return: Job
        """
        return self._missions_service.run_job_on_lz(mission_id, station_id, lz_id, cpu_count=cpu_count, memory_amount=memory_amount, gpu_count=gpu_count)

    def create_and_upload_mission(
        self,
        name,
        directory,
        description="",
        source_storage_id=None,
        destination_storage_id=None,
        source_path=None,
        destination_path=None,
        mission_type_id=None,
        settings=None,
    ):
        """
        Create and upload mission

        :param name: str: Name of mission
        :param directory: str: filepath to the folder you want to upload
        :param description: Optional[str]: description of mission
        :param mission_type_id: Optional[str]: specify mission type
        :param destination_path: Optional[str]
        :param source_path: Optional[str]
        :param destination_storage_id: Optional[str]
        :param source_storage_id: Optional[str]
        :param settings: Optional[Dict[str, str]]: Get required settings via
         missions.get_mission_type_settings_info()
        :return: Mission
        """
        request = CreateMissionRequest(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            source_path=source_path,
            destination_path=destination_path,
            mission_type_id=mission_type_id,
            settings=settings,
        )
        mission = self._missions_service.create_mission(request)
        self._missions_service.upload(mission.mission_id, directory)
        return mission

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
        """
        Create mission and run a job

        :param name: str: Name of mission
        :param directory: str: filepath to the folder you want to upload
        :param station_id: str: station id the mission will be ran in
        :param lz_id: Optional[str] if you want to run on a specific landing zone
        :param description: Optional[str]: description of mission
        :param mission_type_id: Optional[str]: specify mission type
        :param destination_path: Optional[str]
        :param source_path: Optional[str]
        :param destination_storage_id: Optional[str]
        :param source_storage_id: Optional[str]
        :param settings: Optional[Dict[str, str]]: Get required settings via
         missions.get_mission_type_settings_info()
        :return: Job
        """
        request = CreateMissionRequest(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            source_path=source_path,
            destination_path=destination_path,
            mission_type_id=mission_type_id,
            settings=settings,
        )
        return self._missions_service.create_mission_and_run_job(
            request=request, directory=directory, station_id=station_id, lz_id=lz_id,
        )

    def get_mission_files(self, mission_id):
        """
        Provides the metadata of all files in a mission

        :param mission_id: mission you want to inspect
        :return: DirectoryListing
        """

        return self._missions_service.get_mission_files(mission_id)

    def delete_file(self, mission_id, file_path):
        """
        Delete file in mission

        :param mission_id: Mission id of mission you want to delete files from
        :param file_path: Path to the mission file you want to delete excluding the mission root
        e.g. if the file to delete is "mission_name/files/file1.py", please enter "files/file1.py"
        :return: boolean
        """
        return self._missions_service.delete_file(mission_id, file_path)

    def update_mission(
        self,
        mission_id,
        name=None,
        description=None,
        source_storage_id=None,
        destination_storage_id=None,
        source_path=None,
        destination_path=None,
        settings=None,
    ):
        """

        :param mission_id: str: Mission type id
        :param name: str: Name of mission
        :param destination_path: Optional[str]
        :param source_path: Optional[str]
        :param destination_storage_id: Optional[str]
        :param source_storage_id: Optional[str]
        :param description: Optional[str]
        :param settings: Optional[Dict[str, str]]: Get required settings via
         missions.get_mission_type_settings_info()
        :return:
        """
        request = UpdateMissionRequest(
            mission_id,
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            source_path=source_path,
            destination_path=destination_path,
            settings=settings,
        )
        return self._missions_service.update_mission(request)

    def update_mission_args(self, mission_id, arg):
        """
        Update the arguments to a mission.

        :param mission_id: str: Mission's id
        :param arg: List[str]: Please supply them as a list of str ["arg1", "arg2"]
        :return:
        """
        return self._missions_service.update_mission_args(mission_id, arg)

    def list_mission_types(self):
        """
        Gets a list of summaries of mission types

        :return: List[MissionType]
        """
        return self._missions_service.list_mission_types()

    def get_mission_type(self, mission_type_id):
        """
        Get a mission type further info

        :param mission_type_id: str: Mission type id
        :return: MissionType
        """
        return self._missions_service.get_mission_type(mission_type_id)

    def get_mission_type_settings_info(self, mission_type_id):
        """
        Gets the mission type's settings info. This settings info is necessary
        when providing a mission type id during creating a project.

        :param mission_type_id: str: Mission type id
        :return: Dict[str, str]: a dictionary that you can update the values of
        """
        return self._missions_service.get_mission_type_settings_info(mission_type_id)
