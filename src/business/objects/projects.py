from datetime import datetime
from typing import Optional

from ...business.objects.event import EventEmitter


class Project:
    def __init__(
        self,
        id_: Optional[str],
        name: str,
        description: str,
        source_storage_id: str,
        source_path: str,  # default will be project_id
        destination_storage_id: str,
        destination_path: str,  # default will be project_id
        user_id: str,
        creation_timestamp: datetime,
    ):
        self.id = id_
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
