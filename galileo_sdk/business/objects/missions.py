class FileListing:
    def __init__(
        self, filename, path, modification_date, creation_date, file_size, nonce=None,
    ):
        self.filename = filename
        self.path = path
        self.modification_date = modification_date
        self.creation_date = creation_date
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
    ):
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
    ):
        self.name = name
        self.description = description
        self.source_storage_id = source_storage_id
        self.destination_storage_id = destination_storage_id
        self.source_path = source_path
        self.destination_path = destination_path
        self.project_type_id = mission_type_id
        self.settings = settings


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
        )
