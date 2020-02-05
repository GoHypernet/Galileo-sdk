from typing import Optional

import requests

from ..repositories.settings import SettingsRepository


class AuthProvider:
    def __init__(
        self,
        settings_repository: SettingsRepository,
        auth_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self._settings_repository = settings_repository
        settings = self._settings_repository.get_settings()

        if auth_token and refresh_token:
            self._access_token = auth_token
            self._refresh_token = refresh_token
        elif username and password:
            r = requests.post(
                f"{settings.backend}/galileo/landing_zone/v1/oauth/token",
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
        return self._access_token

    def get_refresh_token(self):
        return self._refresh_token
