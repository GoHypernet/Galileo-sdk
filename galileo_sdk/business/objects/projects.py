from ...business.objects.event import EventEmitter


class FileListing:
    def __init__(
        self, filename, modification_date, creation_date, file_size, nonce=None,
    ):
        self.filename = filename
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


class Project:
    def __init__(
        self,
        project_id,
        name,
        description,
        source_storage_id,
        source_path,  # default will be project_id
        destination_storage_id,
        destination_path,  # default will be project_id
        user_id,
        creation_timestamp,
    ):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.source_storage_id = source_storage_id
        self.source_path = source_path
        self.destination_storage_id = destination_storage_id
        self.destination_path = destination_path
        self.user_id = user_id
        self.creation_timestamp = creation_timestamp


class ProjectsEvents:
    def __init__(self):
        self._events = EventEmitter()
