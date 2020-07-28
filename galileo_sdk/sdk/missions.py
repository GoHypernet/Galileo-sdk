class MissionsSdk:
    def __init__(self, missions_service):
        self._missions_service = missions_service

    def list_missions(
        self, ids=None, names=None, user_ids=None, page=1, items=25,
    ):
        """
        Get list of missions

        :param ids: Optional[List[str]]: Filter by mission id
        :param names: Optional[List[str]]: Filter by mission name
        :param user_ids: Optional[List[str]]: Filter by user ids
        :param page: Optional[int]: Page #
        :param items: Optional[int]: # of items per page
        :return: List[mission]
        """
        return self._missions_service.list_missions(
            ids=ids, names=names, user_ids=user_ids, page=page, items=items
        )

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
        """
        Create a mission
        :param: CreatemissionRequest
        :return: mission
        """
        return self._missions_service.create_mission(
            name,
            description,
            source_storage_id,
            destination_storage_id,
            mission_type_name,
            source_path,
            destination_path,
            mission_type_id,
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

        :param mission_id: str
        :param station_id: str
        :return: Job
        """
        return self._missions_service.run_job_on_station(mission_id, station_id)

    def run_job_on_lz(self, mission_id, station_id, lz_id):
        """
        Run a job on a machine

        :param mission_id: str
        :param station_id: str
        :param lz_id: str
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
        mission_type_name=None,
        source_path=None,
        destination_path=None,
        mission_type_id=None,
    ):
        mission = self._missions_service.create_mission(
            name,
            description,
            source_storage_id,
            destination_storage_id,
            mission_type_name,
            source_path,
            destination_path,
            mission_type_id,
        )
        self._missions_service.upload(mission.mission_id, directory)
        return mission

    def create_mission_and_run_job(
        self,
        name,
        directory,
        station_id,
        machine_id=None,
        description="",
        source_storage_id=None,
        destination_storage_id=None,
        mission_type_name=None,
        source_path=None,
        destination_path=None,
        mission_type_id=None,
    ):
        """
        :param name:
        :param directory: str: filepath to the folder you want to upload
        :param station_id: str: station id the mission will be ran in
        :param machine_id: Optional[str] if you want to run on a specific machine
        :param mission_type_id: str
        :param destination_path: str
        :param source_path: str
        :param mission_type_name: str
        :param destination_storage_id: str
        :param source_storage_id: str
        :param description: str
        :return: Job
        """
        mission = self._missions_service.create_mission(
            name,
            description,
            source_storage_id,
            destination_storage_id,
            mission_type_name,
            source_path,
            destination_path,
            mission_type_id,
        )
        self._missions_service.upload(mission.mission_id, directory)
        if machine_id:
            job = self._missions_service.run_job_on_lz(
                mission.mission_id, station_id, machine_id
            )
        else:
            job = self._missions_service.run_job_on_station(
                mission.mission_id, station_id
            )

        return job

    def get_mission_files(self, mission_id):
        """
        Provides the metadata of all files in a mission
        :param mission_id: mission you want to inspect
        :return: DirectoryListing
        """

        return self._missions_service.get_mission_files(mission_id)

    def delete_file(self, mission_id, file_path):
        """

        :param mission_id:
        :param file_path:
        :return:
        """
        return self._missions_service.delete_file(mission_id, file_path)

    def update_mission(self, mission_id, update_mission_request):
        """

        :param mission_id:
        :param update_mission_request:
        :return:
        """
        return self._missions_service.update_mission(mission_id, update_mission_request)

    def update_mission_args(self, mission_id, args):
        """

        :param mission_id:
        :param args:
        :return:
        """
        return self._missions_service.update_mission(mission_id, args)

    def delete_mission_files(self, mission_id):
        """

        :param mission_id:
        :return:
        """
        return self._missions_service.delete_mission_files(mission_id)

    def get_mission_types(self):
        """

        :return:
        """
        return self._missions_service.get_mission_types()
