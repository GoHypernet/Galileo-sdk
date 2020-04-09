import os

from .business.services.jobs import JobsService
from .business.services.log import LogService
from .business.services.machines import MachinesService
from .business.services.profiles import ProfilesService
from .business.services.projects import ProjectsService
from .business.services.stations import StationsService
from .data.events.connector import GalileoConnector
from .data.providers.auth import AuthProvider
from .data.repositories.jobs import JobsRepository
from .data.repositories.machines import MachinesRepository
from .data.repositories.profiles import ProfilesRepository
from .data.repositories.projects import ProjectsRepository
from .data.repositories.settings import SettingsRepository
from .data.repositories.stations import StationsRepository
from .sdk.jobs import JobsSdk
from .sdk.machines import MachinesSdk
from .sdk.profiles import ProfilesSdk
from .sdk.projects import ProjectsSdk
from .sdk.stations import StationsSdk

import sys

_ver = sys.version_info

is_py2 = (_ver[0] == 2)
is_py3 = (_ver[0] == 3)

NAMESPACE = "/galileo/user_interface/v1"


class GalileoSdk:
    def __init__(
        self,
        auth_token=None,
        refresh_token=None,
        username=None,
        password=None,
        config=None,
    ):
        """
        Galileo SDK object.

        :param auth_token: authentication token
        :param refresh_token: refresh token
        :param username: Galileo username
        :param password: Galileo password
        :param config: production or development
        """
        self.log = LogService()
        if "GALILEO_CONFIG" in os.environ:
            self._settings = SettingsRepository(str(os.environ["GALILEO_CONFIG"]))
        elif config:
            self._settings = SettingsRepository(config)
        else:
            self._settings = SettingsRepository("production")

        settings = self._settings.get_settings()
        self.backend = settings.backend

        if "GALILEO_TOKEN" in os.environ and "GALILEO_REFRESH_TOKEN" in os.environ:
            self._auth_provider = AuthProvider(
                settings_repository=self._settings,
                auth_token=str(os.environ["GALILEO_TOKEN"]),
                refresh_token=str(os.environ["GALILEO_REFRESH_TOKEN"]),
            )
        elif "GALILEO_USER" in os.environ and "GALILEO_PASSWORD" in os.environ:
            self._auth_provider = AuthProvider(
                settings_repository=self._settings,
                username=str(os.environ["GALILEO_USER"]),
                password=str(os.environ["GALILEO_PASSWORD"]),
            )
        elif auth_token and refresh_token:
            self._auth_provider = AuthProvider(
                settings_repository=self._settings,
                auth_token=auth_token,
                refresh_token=refresh_token,
            )
        elif username and password:
            self._auth_provider = AuthProvider(
                settings_repository=self._settings, username=username, password=password
            )
        else:
            raise ValueError(
                "Authentication token AND refresh token (OR) username AND password, must be provided"
            )

        self._jobs_repo = JobsRepository(self._settings, self._auth_provider, NAMESPACE)
        self._stations_repo = StationsRepository(
            self._settings, self._auth_provider, NAMESPACE
        )
        self._profiles_repo = ProfilesRepository(
            self._settings, self._auth_provider, NAMESPACE
        )
        self._machines_repo = MachinesRepository(
            self._settings, self._auth_provider, NAMESPACE
        )
        self._projects_repo = ProjectsRepository(
            self._settings, self._auth_provider, NAMESPACE
        )

        self._jobs_service = JobsService(self._jobs_repo)
        self._stations_service = StationsService(self._stations_repo)
        self._profiles_service = ProfilesService(self._profiles_repo)
        self._machines_service = MachinesService(self._machines_repo)
        self._projects_service = ProjectsService(self._projects_repo)

        self.profiles = ProfilesSdk(self._profiles_service)
        self.projects = ProjectsSdk(self._projects_service)

        if is_py3:
            self._events = GalileoConnector(self._settings, self._auth_provider, NAMESPACE)
            self.jobs = JobsSdk(self._jobs_service, self._events.jobs_events)
            self.stations = StationsSdk(
                self._stations_service, self._events.stations_events
            )
            self.machines = MachinesSdk(
                self._machines_service, self._events.machines_events
            )
        elif is_py2:
            self.jobs = JobsSdk(self._jobs_service)
            self.stations = StationsSdk(self._stations_service)
            self.machines = MachinesSdk(self._machines_service)

    def disconnect(self):
        """
        Call disconnect before your application or script ends.
        :return: None
        """
        if is_py3:
            self._events.disconnect()

    def update_auth_token(self, auth_token):
        """

        :param auth_token: str, new auth_token
        :return: None
        """
        self._auth_provider.set_access_token(auth_token)
