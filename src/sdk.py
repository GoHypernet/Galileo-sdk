from typing import Optional

from .business.services import jobs, log, machines, profiles, stations
from .data.providers import auth
from .data.repositories import jobs, machines, profiles, settings, stations


class GalileoSdk:
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
                auth_token=auth_token, refresh_token=refresh_token
            )
        elif username and password:
            self._auth_provider = auth.AuthProvider(
                username=username, password=password
            )
        else:
            raise ValueError(
                "Authentication token AND refresh token (OR) username AND password, must be provided"
            )

        self._jobs_repo = jobs.JobsRepository(self._settings, self._auth_provider)
        self._jobs_service = jobs.JobsService(self._jobs_repo)
        self.jobs = JobsSdk(self._jobs_service)

        self._stations_repo = stations.StationsRepository(
            self._settings, self._auth_provider
        )
        self._stations_service = stations.StationsService(self._jobs_repo)
        self.stations = StationsSdk(self._jobs_repo)

        self._profiles_repo = profiles.ProfilesRepository(
            self._settings, self._auth_provider
        )
        self._profiles_service = profiles.ProfilesService(self._profiles_repo)
        self.profiles = ProfilesSdk(self._profiles_service)

        self._machines_repo = machines.MachinesRepository(
            self._settings, self._auth_provider
        )
        self._machines_service = machines.MachinesService(self._machines_repo)
        self.machines = MachinesSdk(self._machines_service)


class JobsSdk:
    def __init__(self, jobs_service):
        self._jobs_service = jobs_service

    def list_jobs(self):
        pass


class MachinesSdk:
    def __init__(self, machines_service):
        self._machines_service = machines_service


class ProfilesSdk:
    def __init__(self, profiles_service):
        self._profile_service = profiles_service

    def list_users(self, page, items):
        self._profile_service.list_users(page, items)
        pass


class StationsSdk:
    def __init__(self, stations_service):
        self._stations_service = stations_service
