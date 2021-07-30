from galileo_sdk.compat import requests


class AuthProvider:
    def __init__(
        self,
        settings_repository,
        auth_token=None,
        refresh_token=None,
        username=None,
        password=None,
    ):
        """
        Authenticates a user with a username and password or access token.

        :param settings_repository: Settings repository
        :type settings_repository: SettingsRepository
        :param auth_token: Access token, default None
        :type auth_token: str, optional
        :param refresh_token: Refresh token, default None
        :type refresh_token: str, optional
        :param username: Username, default None
        :type username: str, optional
        :param password: Password, default None
        :type password: str, optional

        """
        self._settings_repository = settings_repository
        settings = self._settings_repository.get_settings()

        if auth_token and refresh_token:
            self._access_token = auth_token
            self._refresh_token = refresh_token
        elif username and password:
            r = requests.post(
                "{backend}/galileo/landing_zone/v1/oauth/token".format(
                    backend=settings.backend),
                json={
                    "username": username,
                    "password": password,
                    "grant_type": "password",
                },
            )
            if r.status_code != 200:
                raise ValueError(
                    "Could not get Auth0 authentication tokens for this username and password combination"
                )
            r = r.json()
            self._access_token = r["access_token"]
            self._refresh_token = r["refresh_token"]

    def get_access_token(self):
        """
        Get the access token.

        :return: A valid access token
        :rtype: str
        """
        return self._access_token

    def get_refresh_token(self):
        """
        Get the refresh token.

        :return: Refresh token
        :rtype: str
        """
        return self._refresh_token

    def set_access_token(self, auth_token):
        """
        Set the access token.

        :param auth_token: A valid access token
        :type auth_token: str
        """
        self._access_token = auth_token
