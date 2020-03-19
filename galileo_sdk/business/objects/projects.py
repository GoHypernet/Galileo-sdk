from datetime import datetime
from typing import List, Optional, Union

from ...business.objects.event import EventEmitter


class FileListing:
    def __init__(
        self,
        filename: str,
        modification_date: datetime,
        creation_date: datetime,
        file_size: int,
        nonce: Optional[str] = None,
    ):
        self.filename = filename
        self.modification_date = modification_date
        self.creation_date = creation_date
        self.file_size = file_size
        self.nonce = nonce

    def __str__(self):
        return f"{self.filename}"


class DirectoryListing:
    def __init__(
        self,
        storage_id: str,
        path: str,
        listings: List[Union["FileListing", "DirectoryListing"]],
    ):
        self.storage_id = storage_id
        self.path = path
        self.listings = listings

    def __str__(self) -> str:
        listing_str = ", ".join(map(str, self.listings))
        s = f"path: '{self.path}', listings: [{listing_str}]"
        return s


class Project:
    def __init__(
        self,
        project_id: str,
        name: str,
        description: str,
        source_storage_id: str,
        source_path: str,  # default will be project_id
        destination_storage_id: str,
        destination_path: str,  # default will be project_id
        user_id: str,
        creation_timestamp: datetime,
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
    _events: EventEmitter

    def __init__(self):
        self._events = EventEmitter()
