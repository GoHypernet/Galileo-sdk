from .data import jobs, machines, profiles, stations
from .business import jobs, log, machines, profiles, stations


class GalileoSdk:
    def __init__(self, auth_token, refresh_token):
        self.auth_token = auth_token
        self.refresh_token = refresh_token

        self.log = log.LogService()

        self._jobs_repo = jobs.JobsRepository()
        self._jobs_service = jobs.JobsService(self._jobs_repo)
        self.jobs = JobsSdk(self._jobs_service)

        self._stations_repo = stations.StationsRepository()
        self._stations_service = stations.StationsService(self._jobs_repo)
        self.stations = StationsSdk(self._jobs_repo)

        self._profiles_repo = profiles.ProfilesRepository()
        self._profiles_service = profiles.ProfilesService(self._profiles_repo)
        self.profiles = ProfilesSdk(self._profiles_service)

        self._machines_repo = machines.MachinesRepository()
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
