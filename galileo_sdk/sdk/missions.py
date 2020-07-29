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
    ):
        """
        Get list of missions

        :param ids: Optional[List[str]]: Filter by mission id
        :param names: Optional[List[str]]: Filter by mission name
        :param user_ids: Optional[List[str]]: Filter by user ids
        :param page: Optional[int]: Page #
        :param items: Optional[int]: # of items per page
        :param mission_type_ids: Optional[List[str]]: Filter by mission_type_ids
        :return: List[mission]
        """
        return self._missions_service.list_missions(
            ids=ids,
            names=names,
            user_ids=user_ids,
            page=page,
            items=items,
            mission_type_ids=mission_type_ids,
        )

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

        :param name: str: Name of mission
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
        return self._missions_service.create_mission(
            name,
            description,
            source_storage_id,
            destination_storage_id,
            source_path,
            destination_path,
            mission_type_id,
            settings,
        )

    def upload(self, mission_id, directory):
        """
        Upload a directory

        :param mission_id: str: Mission you want to upload the file to
        :param directory: str: Path to folder that you want to upload
        :return: bool
        """
        return self._missions_service.upload(mission_id, directory)

    def run_job_on_station(self, mission_id, station_id):
        """
        Run a job on a station

        :param mission_id: str: Mission you want to upload the file to
        :param station_id: str: Station you want to run the job on
        :return: Job
        """
        return self._missions_service.run_job_on_station(mission_id, station_id)

    def run_job_on_lz(self, mission_id, station_id, lz_id):
        """
        Run a job on a landing zone

        :param mission_id: str: Mission you want to upload the file to
        :param station_id: str: Station you want to run the job on
        :param lz_id: str: Landing zone you want to run the job on
        :return: Job
        """
        return self._missions_service.run_job_on_lz(mission_id, station_id, lz_id)

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
        mission = self._missions_service.create_mission(
            name,
            description,
            source_storage_id,
            destination_storage_id,
            source_path,
            destination_path,
            mission_type_id,
            settings,
        )
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
        return self._missions_service.create_mission_and_run_job(
            name=name,
            directory=directory,
            station_id=station_id,
            lz_id=lz_id,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            source_path=source_path,
            destination_path=destination_path,
            mission_type_id=mission_type_id,
            settings=settings,
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

        :param mission_id: Mission id of mission you want to delete files from
        :param file_path: Path to the mission file you want to delete starting from
        the mission root
        :return:
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
        return self._missions_service.update_mission(
            mission_id,
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            source_path=source_path,
            destination_path=destination_path,
            settings=settings,
        )

    def update_mission_args(self, mission_id, args):
        """
        Update the arguments to a mission.

        :param mission_id:
        :param args:
        :return:
        """
        return self._missions_service.update_mission(mission_id, args)

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
