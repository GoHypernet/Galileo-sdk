import sys

if sys.version_info[0] == 3:
    from .events import GalileoConnector

from .repositories import (
    JobsRepository,
    LzRepository,
    ProfilesRepository,
    ProjectsRepository,
    RequestsRespository,
    StationsRepository,
    SettingsRepository,
)
from .providers import AuthProvider
