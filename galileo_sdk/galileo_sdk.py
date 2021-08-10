import os
import socket

from .business import (
    UniversesService,
    CargoBaysService,
    JobsService,
    LogService,
    LzService,
    ProfilesService,
    MissionsService,
    StationsService,
)
from .data import (
    AuthProvider,
    UniversesRepository,
    CargoBaysRepository,
    JobsRepository,
    LzRepository,
    ProfilesRepository,
    MissionsRepository,
    SettingsRepository,
    StationsRepository,
)
from .sdk import (
    UniversesSdk,
    CargoBaysSdk,
    JobsSdk,
    LzSdk,
    ProfilesSdk,
    MissionsSdk,
    StationsSdk,
)

import sys

_ver = sys.version_info

is_py2 = _ver[0] == 2
is_py3 = _ver[0] == 3

if is_py3:
    from .data import GalileoConnector

NAMESPACE = "/galileo/user_interface/v1"


def notify():
    if len(sys.argv) > 1:
        GalileoSdk.send_notification(GalileoSdk, sys.argv[1])
    else:
        print("No message given for notification.")


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
            self._settings = SettingsRepository(
                str(os.environ["GALILEO_CONFIG"]))
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
        elif username and password:
            self._auth_provider = AuthProvider(
                settings_repository=self._settings,
                username=username,
                password=password)
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
        else:
            raise ValueError(
                "Authentication token AND refresh token (OR) username AND password, must be provided"
            )

        # Set up feature repositories
        self._universes_repo = UniversesRepository(self._settings,
                                                   self._auth_provider,
                                                   NAMESPACE)
        self._cargo_bays_repo = CargoBaysRepository(self._settings,
                                                    self._auth_provider,
                                                    NAMESPACE)
        self._jobs_repo = JobsRepository(self._settings, self._auth_provider,
                                         NAMESPACE)
        self._stations_repo = StationsRepository(self._settings,
                                                 self._auth_provider,
                                                 NAMESPACE)
        self._profiles_repo = ProfilesRepository(self._settings,
                                                 self._auth_provider,
                                                 NAMESPACE)
        self._lz_repo = LzRepository(self._settings, self._auth_provider,
                                     NAMESPACE)
        self._missions_repo = MissionsRepository(self._settings,
                                                 self._auth_provider,
                                                 NAMESPACE)

        # set up feature services
        self._universes_service = UniversesService(self._universes_repo)
        self._cargobays_service = CargoBaysService(self._cargo_bays_repo)
        self._jobs_service = JobsService(self._jobs_repo, self._profiles_repo)
        self._stations_service = StationsService(self._stations_repo)
        self._profiles_service = ProfilesService(self._profiles_repo)
        self._lz_service = LzService(self._lz_repo)
        self._missions_service = MissionsService(self._missions_repo)

        # set up feature SDKs
        self.universes = UniversesSdk(self._universes_service)
        self.cargobays = CargoBaysSdk(self._cargobays_service)
        self.profiles = ProfilesSdk(self._profiles_service)
        self.missions = MissionsSdk(self._missions_service)

        connector = None
        if is_py3:
            connector = GalileoConnector(self._settings, self._auth_provider,
                                         NAMESPACE)

        self.jobs = JobsSdk(self._jobs_service, connector)
        self.stations = StationsSdk(self._stations_service, connector)
        self.lz = LzSdk(self._lz_service, connector)

    def disconnect(self):
        """
        Call disconnect before your application or script ends.
        :return: None
        """
        if is_py3:
            self.jobs.disconnect()
            self.stations.disconnect()
            self.lz.disconnect()

    def update_auth_token(self, auth_token):
        """

        :param auth_token: str, new auth_token
        :return: None
        """
        self._auth_provider.set_access_token(auth_token)

    def set_universe(self, universe_id):
        """
        Call this function to set your Galileo Universe context. The Hypernet Labs Universe is the
        default operating Universe if nothing is set. 
        
        :param universe_id: str, the uuid of the universe you want to operate in (default is Hypernet Labs)
        :return: None
        """
        self._settings.get_settings().universe = universe_id

    def send_notification(self, message, verbose=False):
        """
        Call this function to send a custom notification from Galileo. You must be running in an active Galileo
        job container for this function to return successful. 
        
        :param message: str, the string to be pushed to the user as the notification (max size is 4kb). 
        :param verbose: boolean, print debug messages to stdout.
        :return success: boolean, whether the message was sent successfully or not. 

        Example:
            >>> success = galileo.send_notification("This is a test notification", verbose=True)
        """

        GALILEO_LZ_IPV4 = os.environ.get('GALILEO_LZ_IPV4')
        GALILEO_LZ_PORT = os.environ.get('GALILEO_LZ_PORT')

        if not (GALILEO_LZ_IPV4 and GALILEO_LZ_PORT):
            if verbose:
                print(
                    "Could not retrieve port and IPV4 address for notification service."
                )
                print(
                    "Are you sure you are running in an active job container?")
            return False

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((GALILEO_LZ_IPV4, int(GALILEO_LZ_PORT)))
            s.sendall("{message}".format(message=message).encode())
            print("Message send successfully.")

        return True