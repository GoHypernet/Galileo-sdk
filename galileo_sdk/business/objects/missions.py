class FileListing:
    def __init__(
        self, filename, path, modification_date, creation_date, file_size, nonce=None,
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


class DirectoryListing:
    def __init__(
        self, storage_id, path, listings,
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
        source_path,  # default will be project_id
        destination_storage_id,
        destination_path,  # default will be project_id
        user_id,
        creation_timestamp,
        mission_type_id,
        updated_timestamp=None,
        organization_id=None,
        settings=None,
        mission_type_name=None,
        public=False
    ):
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


class MissionType:
    def __init__(
        self,
        id,
        name,
        description,
        version,
        active=None,
        container_type=None,
        wizard_spec=None,
    ):
        """
        Mission Framework Type Object

        :param id: UUID of the Mission Framework Type
        :param name: Human readable name of the Framework Type
        :param description: Optional description of the Framework Type
        :param version: Specific version of the overall Framework Type
        :param active: Is the framework actively supported (False means depricated)
        :param container_type: Target container OS type (i.e. Windows, Linux, Singularity)
        :param wizard_spec: JSON specs for UI configuration wizard
        """
        self.id = id
        self.name = name
        self.description = description
        self.version = version
        self.active = active
        self.container_type = container_type
        self.wizard_spec = wizard_spec


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
        self.name = name
        self.description = description
        self.source_storage_id = source_storage_id
        self.destination_storage_id = destination_storage_id
        self.source_path = source_path
        self.destination_path = destination_path
        self.project_type_id = mission_type_id
        self.settings = settings
        self.public = public


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
