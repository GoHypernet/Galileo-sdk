class FileListing:
    def __init__(
        self,
        filename,
        path,
        modification_date,
        creation_date,
        file_size,
        nonce=None,
    ):
        """
        Mission File Listing Object

        :param filename: Human readable name of the file object
        :param path: Path of the file object in the Mission storage
        :param modification_date: Timestamp when the file object was last touched
        :param creation_date: Timestamp when the file object was created
        :param file_size: Size in bytes of the file object
        :param nonce: Access nonce (Optional)
        """
        self.filename = filename
        self.path = path
        self.modification_date = modification_date
        self.modification_timestamp = modification_date
        self.creation_date = creation_date
        self.creation_timestamp = creation_date
        self.file_size = file_size
        self.nonce = nonce

    def __str__(self):
        return 'Filelisting: {path}/{filename}'.format(path=self.path,
                                                       filename=self.filename)

    def __repr__(self):
        return str(self)


class DirectoryListing:
    def __init__(
        self,
        storage_id,
        path,
        listings,
    ):
        self.storage_id = storage_id
        self.path = path
        self.listings = listings


class Mission:
    def __init__(
            self,
            mission_id,
            name,
            description,
            source_storage_id,
            source_path,  # default will be mission_id
            destination_storage_id,
            destination_path,  # default will be mission_id
            user_id,
            creation_timestamp,
            mission_type_id,
            updated_timestamp=None,
            organization_id=None,
            settings=None,
            mission_type_name=None,
            public=False):
        """
        Mission Object

        :param mission_id: UUID of the Mission
        :param name: Human readable name of the Mission
        :param description: Optional description of the Mission
        :param source_storage_id: UUID of the storage provider for input data
        :param source_path: base path in the source storage provider where data is stored
        :param destination_storage_id: UUID of the storage provider for output data
        :param destination_path: base path in the destination storage provider where data is stored
        :param user_id: UUID of the Mission owner
        :param creation_timestamp: Time the Mission was created
        :param mission_type_id: Mission framework type UUID
        :param updated_timestamp: Time the Mission was last updated
        :param organization_id: The organization UUID the Mission is associated with
        :param settings: Dictionary of Mission framework type settings
        :param mission_type_name: Human readable name of the Mission framework type
        :param public: Boolean indicating if the Mission is publicly searchable
        """
        self.mission_id = mission_id
        self.name = name
        self.description = description
        self.source_storage_id = source_storage_id
        self.source_path = source_path
        self.destination_storage_id = destination_storage_id
        self.destination_path = destination_path
        self.user_id = user_id
        self.creation_timestamp = creation_timestamp
        self.mission_type_id = mission_type_id
        self.updated_timestamp = updated_timestamp
        self.organization_id = organization_id
        self.settings = settings
        self.mission_type_name = mission_type_name
        self.public = public

    def __str__(self):
        return 'Mission: {name}'.format(name=self.name)

    def __repr__(self):
        return str(self)


class MissionType:
    def __init__(self,
                 id,
                 name,
                 description,
                 version,
                 active=None,
                 container_type=None,
                 wizard_spec=None,
                 enable_tunnels=None,
                 generate_credentials=None,
                 distributed=None,
                 min_cpu_count=None,
                 max_cpu_count=None,
                 default_cpu_count=None,
                 min_memory_amount=None,
                 max_memory_amount=None,
                 default_memory_amount=None,
                 min_gpu_count=None,
                 max_gpu_count=None,
                 default_gpu_count=None,
                 logo_url=None,
                 credits_per_hour=None):
        """
        Mission Framework Type Object

        :param id: UUID of the Mission Framework Type
        :param name: Human readable name of the Framework Type
        :param description: description of the Framework Type
        :param version: Specific version of the overall Framework Type
        :param active: Is the framework actively supported (False means depricated)
        :param container_type: Target container OS type (i.e. Windows, Linux, Singularity)
        :param wizard_spec: JSON specs for UI configuration wizard
        :param enable_tunnels: Enable tunnels
        :param generate_credentials: Generate Credentials for mission
        :param distributed: Distributed mission
        :param min_cpu_count: Minimum CPU count for jobs of this mission type.
        :param max_cpu_count: Maximum CPU count for jobs of this mission type.
        :param default_cpu_count: Default CPU count for jobs of this mission type.
        :param min_memory_amount: Minimum memory amount for jobs of this mission type.
        :param max_memory_amount: Maximum memory amount for jobs of this mission type.
        :param default_memory_amount: Default memory amount for jobs of this mission type.
        :param min_gpu_count: Minimum GPU count for jobs of this mission type.
        :param max_gpu_count: Maximum GPU count for jobs of this mission type.
        :param default_gpu_count: Default GPU count for jobs of this mission type.
        :param logo_url: URL for MissionType URL
        :param credits_per_hour: Credit amount per hour
        """
        self.id = id
        self.name = name
        self.description = description
        self.version = version
        self.active = active
        self.container_type = container_type
        self.wizard_spec = wizard_spec
        self.enable_tunnels = enable_tunnels
        self.generate_credentials = generate_credentials
        self.distributed = distributed
        self.min_cpu_count = min_cpu_count
        self.max_cpu_count = max_cpu_count
        self.default_cpu_count = default_cpu_count
        self.min_memory_amount = min_memory_amount
        self.max_memory_amount = max_memory_amount
        self.default_memory_amount = default_memory_amount
        self.min_gpu_count = min_gpu_count
        self.max_gpu_count = max_gpu_count
        self.default_gpu_count = default_gpu_count
        self.logo_url = logo_url
        self.credits_per_hour = credits_per_hour

    def __str__(self):
        return 'Mission Type: {name} Version: {version}'.format(
            name=self.name, version=self.version)

    def __repr__(self):
        return str(self)


class CreateMissionRequest(object):
    def __init__(
        self,
        name,
        description,
        source_storage_id=None,
        destination_storage_id=None,
        source_path=None,
        destination_path=None,
        mission_type_id=None,
        settings=None,
        public=False,
    ):
        """
        Mission Request Object

        :param name: Mission name
        :type name: str
        :param description: Description of the mission
        :type description: str
        :param source_storage_id: TODO: storage id for source storage, defaults to None
        :type source_storage_id: str, optional
        :param destination_storage_id: TODO: storage id for destination storage, defaults to None
        :type destination_storage_id: str, optional
        :param source_path: File path to source, defaults to None
        :type source_path: str, optional
        :param destination_path: Destination file path, defaults to None
        :type destination_path: str, optional
        :param mission_type_id: Mission type id, defaults to None
        :type mission_type_id: str, optional
        :param settings: Custom settings for mission, defaults to None
        :type settings: Dict, optional
        :param public: Create a public or private mission, defaults to False
        :type public: bool, optional
        """
        self.name = name
        self.description = description
        self.source_storage_id = source_storage_id
        self.destination_storage_id = destination_storage_id
        self.source_path = source_path
        self.destination_path = destination_path
        self.mission_type_id = mission_type_id
        self.settings = settings
        self.public = public

    def __str__(self):
        model_string = "Create Mission Request: "
        for key, value in self.__dict__.items():
            if "_" not in key and value is not None:
                model_string += "{key}={value}, ".format(key=key, value=value)

    def __repr__(self):
        return "Create Mission Request: {name}".format(name=self.name)


class UpdateMissionRequest(CreateMissionRequest):
    def __init__(
        self,
        mission_id,
        name=None,
        description=None,
        source_storage_id=None,
        destination_storage_id=None,
        source_path=None,
        destination_path=None,
        settings=None,
        public=None,
    ):
        """
        Update Mission Request Object

        :param mission_id: Mission ID of the mission to update
        :type mission_id: str
        :param name: Updated name, defaults to None
        :type name: str, optional
        :param description: Updated description, defaults to None
        :type description: str, optional
        :param source_storage_id: Updated source storage id, defaults to None
        :type source_storage_id: str, optional
        :param destination_storage_id: Updated destination storage id, defaults to None
        :type destination_storage_id: str, optional
        :param source_path: Updated source file path, defaults to None
        :type source_path: str, optional
        :param destination_path: Updated Destination file path, defaults to None
        :type destination_path: str, optional
        :param settings: Updated mission settings, defaults to None
        :type settings: Dict, optional
        :param public: Update mission access/visiblity, defaults to None
        :type public: bool, optional
        """
        self.mission_id = mission_id
        super(UpdateMissionRequest, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            source_path=source_path,
            destination_path=destination_path,
            settings=settings,
            public=public,
        )

    def __str__(self):
        model_string = "Update Mission Request: "
        for key, value in self.__dict__.items():
            if "_" not in key and value is not None:
                model_string += "{key}={value}, ".format(key=key, value=value)

    def __repr__(self):
        return "Update Mission Request: {name}".format(name=self.name)