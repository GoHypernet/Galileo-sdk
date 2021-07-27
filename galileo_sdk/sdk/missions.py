from ..business.objects.missions import UpdateMissionRequest, CreateMissionRequest


class MissionsSdk:
    def __init__(self, missions_service):
        self._missions_service = missions_service

    def list_missions(self,
                      mission_ids=None,
                      names=None,
                      user_ids=None,
                      page=1,
                      items=25,
                      mission_type_ids=None,
                      archived=None):
        """
        Get list of Missions associated with your account

        :param mission_ids: Optional[List[str]]: Filter by Mission UUID
        :param names: Optional[List[str]]: Filter by Mission name
        :param user_ids: Optional[List[str]]: Filter by user UUID
        :param page: Optional[int]: Return a particular page number
        :param items: Optional[int]: Number of Missions to return per page
        :param mission_type_ids: Optional[List[str]]: Filter by mission_type_ids
        :param archived: Optional[bool]: Filter for archived missions
        :return: List[Mission]
        
        Example:
            >>> missions = galileo.missions.list_missions(items=10)
            >>> for mission in missions:
            >>>    print(mission.name)
        """
        return self._missions_service.list_missions(
            mission_ids=mission_ids,
            names=names,
            user_ids=user_ids,
            page=page,
            items=items,
            mission_type_ids=mission_type_ids,
            archived=archived)

    def get_mission_by_id(self, mission_id):
        """
        Get a specific Mission's details by providing its UUID
        
        :param mission_id: str: Mission UUID
        :return: Mission
        
        Example:
            >>> my_missions = galileo.missions.list_missions()
            >>> mission = galileo.missions.get_mission_by_id(mission_id=my_missions[0].mission_id)
            >>> print(mission.name)
        """
        return self._missions_service.get_mission_by_id(mission_id)

    def create_mission(self,
                       name,
                       description="",
                       source_storage_id=None,
                       destination_storage_id=None,
                       source_path=None,
                       destination_path=None,
                       mission_type_id=None,
                       settings=None,
                       public=False):
        """
        Create a new Mission in your Galileo account.

        :param name: str: Human readable name of the Mission you are creating
        :param description: Optional[str]: Optional description of the Mission you are creating
        :param mission_type_id: Optional[str]: UUID of the Mission framework type you are creating
        :param destination_path: Optional[str]: Root directory of the Mission in the specified source Cargo Bay (not needed if using default storage)
        :param source_path: Optional[str]: Root directory of the Mission in the specified destinatino Cargo Bay (not needed if using default storage)
        :param destination_storage_id: Optional[str]: UUID of the Cargo Bay to use as the Mission data destination
        :param source_storage_id: Optional[str]: UUID of the Cargo Bay to use as the Mission data source
        :param settings: Optional[Dict[str, str]]: Mission framework type settings (get this info from get_mission_type_settings_info)
        :param public: Optional[bool]: Boolean indicating whether to list the Mission as public (True) or private (False - default)
         missions.get_mission_type_settings_info()
        :return: Mission
        
        Example:
            >>> swmm_mission = galileo.missions.create_mission(name="SWMM Test2",description="testing",mission_type_id='f1934063-034a-4eba-adaa-e28bd95f138a',settings={"cpu_count":"1","memory_count":"3000","filename":"river","swmmversion":"5.1.007"})
            >>> print(swmm_mission.mission_id)
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
            public=public,
        )
        return self._missions_service.create_mission(request)

    def delete_mission_by_id(self, mission_id):
        """
        Deletes a mission

        :param mission_id: str: Target Mission UUID

        Example:
            >>> galileo.missions.delete_mission_by_id(mission_id="mission-id")
        """

        return self._missions_service.delete_mission(mission_id)

    def upload(self, mission_id, payload, rename=None, verbose=False):
        """
        Upload a file or directory to the specified Mission. If the payload is a file, this function 
        will place the file in the top level of the Mission file tree. If the payload is a directory, 
        files in the first level of the payload directory will appear in the top level of the Mission 
        file tree and subfolders of the payload will appear as subfolders in the Mission file tree. 

        :param mission_id: str: Target Mission UUID
        :param payload: str: Path to folder or file to upload to targeted Mission
        :param rename: str: Used when uploading a single file to specify the desired path within the Mission context (i.e. rename='/data/mydata.csv').
        :param verbose: bool: Verbosity flag, default is False
        :return: bool
        
        Example:
            >>> my_missions = galileo.missions.list_missions() # get the UUID of the mission you want
            >>> UUID = my_missions[0].mission_id
            >>> payload = 'C:\\Users\\Galileo\\Hypernet Labs, Inc. Dropbox\\Julia Example' # a Windows path, put your path here
            >>> success = galileo.missions.upload(UUID, payload) # upload a whole directory
            >>> if success:
            >>>     print("It worked")
            >>> else:
            >>>     print("I don't think this Mission exists")
        """
        return self._missions_service.upload(mission_id, payload, rename,
                                             verbose)

    def run_job_on_station(self,
                           mission_id,
                           station_id,
                           cpu_count=None,
                           memory_amount=None,
                           gpu_count=None):
        """
        Run a job on a station

        :param mission_id: str: Reference ID of Mission to launch job from
        :param station_id: str: Reference ID of the Station to deploy job to
        :param cpu_count: int: Number of cpus for this job to request
        :param memory_amount: int: Memory in MB for this job to request
        :param gpu_count: int: Number of gpus for this job to request
        :return: Job

        Example:
            >>> galileo.missions.run_job_on_station(mission.mission_id,station.stationid,cpu_count=1,memory_amount=1048)

        """
        return self._missions_service.run_job_on_station(
            mission_id,
            station_id,
            cpu_count=cpu_count,
            memory_amount=memory_amount,
            gpu_count=gpu_count)

    def run_job_on_lz(self,
                      mission_id,
                      station_id,
                      lz_id,
                      cpu_count=None,
                      memory_amount=None,
                      gpu_count=None):
        """
        Run a job on a landing zone

        :param mission_id: str: Reference ID of Mission to launch job from
        :param station_id: str: Reference ID of the Station to deploy job to
        :param lz_id: str: Reference ID of specific LZ to deploy to
        :param cpu_count: int: Number of cpus for this job to request
        :param memory_amount: int: Memory in MB for this job to request
        :param gpu_count: int: Number of gpus for this job to request
        :return: Job

        Example:
            >>> galileo.missions.run_job_on_lz(mission.mission_id,station.stationid,lzid,cpu_count=1,memory_amount=1048)
        """
        return self._missions_service.run_job_on_lz(
            mission_id,
            station_id,
            lz_id,
            cpu_count=cpu_count,
            memory_amount=memory_amount,
            gpu_count=gpu_count)

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
        public=False,
    ):
        """
        Create a new Mission in your Galileo account and upload input files from the specified directory in the same call. 

        :param name: str: Human readable name of the Mission that will be displayed in the UI
        :param directory: str: filepath to the folder you want to upload as input files to the Mission
        :param description: Optional[str]: Textual description of the Mission 
        :param mission_type_id: Optional[str]: Mission Framework Type UUID
        :param destination_path: Optional[str]: Storage directory in the destination Cargo Bay
        :param source_path: Optional[str]: Source directory in the source Cargo Bay
        :param destination_storage_id: Optional[str]: UUID of the Cargo Bay where results will be stored
        :param source_storage_id: Optional[str]: UUID of the Cargo Bay where source files are to be stored
        :param settings: Optional[Dict[str, str]]: Mission Framework Type settings (can be retrieved via the get_mission_type_settings_info function)
         missions.get_mission_type_settings_info()
        :param public: Optional[bool]: Boolean indicating if the resulting Mission should be listed as public (True) or private (False - default)
        :return: Mission
        
        Example:
            >>> project_folder = 'C:\\Users\\Galileo\\SWMM_Project' # put your path here
            >>> swmm_mission = galileo.missions.create_and_upload_mission(name="SWMM Test2",directory=project_folder,description="testing",mission_type_id='f1934063-034a-4eba-adaa-e28bd95f138a',settings={"cpu_count":"1","memory_count":"3000","filename":"river","swmmversion":"5.1.007"})
            >>> print(swmm_mission.mission_id)
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
            public=public,
        )
        mission = self._missions_service.create_mission(request)
        self._missions_service.upload(mission.mission_id, directory, True)
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
        public=False,
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
        :param public: Optional[bool]: Boolean indicating if the resulting Mission should be listed as public (True) or private (False - default)
        :return: Job

        Example:
            >>> project_folder = 'C:\\Users\\Galileo\\SWMM_Project' # put your path here
            >>> swmm_mission = galileo.missions.create_and_run_job("SWMM Test2",project_folder,"my-station-id")
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
            public=public,
        )
        return self._missions_service.create_mission_and_run_job(
            request=request,
            directory=directory,
            station_id=station_id,
            lz_id=lz_id,
        )

    def get_mission_files(self, mission_id):
        """
        Provides the metadata of all files in a Mission context

        :param mission_id: UUID of the Mission to inspect
        :return: List[FileListing]
        
        Example:
            >>> my_missions = galileo.missions.list_missions() # get the UUID of the mission you want
            >>> UUID = my_missions[0].mission_id
            >>> mission_files = galileo.missions.get_mission_files(UUID)
            >>> for file in mission_files:
            >>>     print(file.filename, file.path, file.file_size)
        
        """

        return self._missions_service.get_mission_files(mission_id)

    def delete_file(self, mission_id, file_path):
        """
        Delete a single file in a Mission

        :param mission_id: UUID of the targeted Mission
        :param file_path: Path to the mission file you want to delete excluding the mission root
        :return: Bool
        
        Example:
        
            >>> # Delete all files in a Mission, including the results
            >>> my_missions = galileo.missions.list_missions() # get the UUID of the mission you want
            >>> UUID = my_missions[0].mission_id
            >>> mission_files = galileo.missions.get_mission_files(UUID)
            >>> for mission_file in mission_files:
            >>>     success = galileo.missions.delete_file(UUID,os.path.join(mission_file.path,mission_file.name))
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
        Update the settings and metadata associated with a Mission context. 

        :param mission_id: str: UUID of the Mission you are updating 
        :param name: str: Mission name after update
        :param destination_path: Optional[str]: Storage destination Cargo Bay root path after update
        :param source_path: Optional[str]: Storage source Cargo Bay root path after update
        :param destination_storage_id: Optional[str]: Storage destination Cargo Bay UUID after update
        :param source_storage_id: Optional[str]: Storage source Cargo Bay UUID after update
        :param description: Optional[str]: Mission description after update
        :param public: Optional[bool]: Boolean flag determining if the Mission is publicly viewable. 
        :param settings: Optional[Dict[str, str]]: Mission framework setting to be applied after update
        :return: Bool: Success flag
        
        Example:
        
            >>> my_missions = galileo.missions.list_missions()
            >>> print("Old Mission Name: ", my_missions[0].name)
            >>> success = galileo.missions.update_mission(my_missions[0].mission_id, "New Name")        
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
        TODO: Add return type
        :return:

        Example:
            >>> my_missions = galileo.missions.list_missions()
            >>> print("Old Mission Name: ", my_missions[0].name)
            >>> galileo.missions.update_mission_args(my_missions[0].mission_id, ["arg1", "arg2"])
        """
        return self._missions_service.update_mission_args(mission_id, arg)

    def list_mission_types(self):
        """
        Gets a list of summaries of Mission Framework Types. 
        
        :return: List[MissionType]
        
        Example:
        
        >>> mission_types = galileo.missions.list_mission_types()
        >>> for mission_type in mission_types:
        >>>     if mission_type.name == "SWMM5" and mission_type.version == 'Batch Mode':
        >>>         print(mission_type.id)
        """
        return self._missions_service.list_mission_types()

    def get_mission_type(self, mission_type_id):
        """
        Retrieve more detailed information about a Mission Framework Type

        :param mission_type_id: str: Mission Framework Type UUID
        :return: MissionType
        
        Example:
        
        >>> mission_types = galileo.missions.list_mission_types()
        >>> mission_type_id = mission_types[0].id
        >>> my_mission_type = galileo.missions.get_mission_type(mission_type_id)
        >>> print("Mission Type Name: ", my_mission_type.name)
        """
        return self._missions_service.get_mission_type(mission_type_id)

    def get_mission_type_settings_info(self, mission_type_id):
        """
        Gets the settings of a particular Mission Framework Type. Use the settings that are returned 
        when creating or updating a Mission with Framework Type mission_type_id. 

        :param mission_type_id: str: Mission Framework Type UUID
        :return: Dict[str, str]: a dictionary where the keys are the names of the settings you can provide and 
        the value is the type or options that are expected for that setting. 
        
        Example:
        
        >>> mission_types = galileo.missions.list_mission_types()
        >>> mission_type_id = mission_types[0].id
        >>> my_mission_type = galileo.missions.get_mission_type(mission_type_id)
       
        >>> my_mission_type_settings = galileo.missions.get_mission_type_settings_info(my_mission_type.id)
        >>> for parameter in my_missin_type_settings:
        >>>     print(parameter, my_mission_type_settings[parameter])
        """
        return self._missions_service.get_mission_type_settings_info(
            mission_type_id)
