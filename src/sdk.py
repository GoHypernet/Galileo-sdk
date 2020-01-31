from typing import Optional

from .business.services import jobs, log, machines, profiles, stations
from .data.events.connector import GalileoConnector
from .data.providers import auth
from .data.repositories import jobs, machines, profiles, settings, stations
from .sdk.jobs import JobsSdk
from .sdk.machines import MachinesSdk
from .sdk.profiles import ProfilesSdk
from .sdk.stations import StationsSdk


class GalileoSdk:
    jobs: JobsSdk
    stations: StationsSdk
    profiles: ProfilesSdk
    machines: MachinesSdk

    def __init__(
        self,
        auth_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        config=None,
    ):
        self.log = log.LogService()

        if config is None:
            self._settings = settings.SettingsRepository("production")
        else:
            self._settings = settings.SettingsRepository(config)

        if auth_token and refresh_token:
            self._auth_provider = auth.AuthProvider(
                settings_repository=self._settings,
                auth_token=auth_token,
                refresh_token=refresh_token,
            )
        elif username and password:
            self._auth_provider = auth.AuthProvider(
                settings_repository=self._settings, username=username, password=password
            )
        else:
            raise ValueError(
                "Authentication token AND refresh token (OR) username AND password, must be provided"
            )

        self._events = GalileoConnector(self._settings, self._auth_provider)

        self._jobs_repo = jobs.JobsRepository(self._settings, self._auth_provider)
        self._jobs_service = jobs.JobsService(self._jobs_repo)
        self.jobs = JobsSdk(self._jobs_service, self._events.jobs_events)

        self._stations_repo = stations.StationsRepository(
            self._settings, self._auth_provider
        )
        self._stations_service = stations.StationsService(self._stations_repo)
        self.stations = StationsSdk(self._stations_service, self._events.station_events)

        self._profiles_repo = profiles.ProfilesRepository(
            self._settings, self._auth_provider
        )
        self._profiles_service = profiles.ProfilesService(self._profiles_repo)
        self.profiles = ProfilesSdk(self._profiles_service)

        self._machines_repo = machines.MachinesRepository(
            self._settings, self._auth_provider
        )
        self._machines_service = machines.MachinesService(self._machines_repo)
        self.machines = MachinesSdk(
            self._machines_service, self._events.machines_events
        )
