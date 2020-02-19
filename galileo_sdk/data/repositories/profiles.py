from typing import Any, Callable, Optional
from urllib.parse import urlunparse

import requests

from ..providers.auth import AuthProvider
from .settings import SettingsRepository


class ProfilesRepository:
    def __init__(
        self, settings_repository: SettingsRepository, auth_provider: AuthProvider,
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider

    def _make_url(
        self,
        endpoint: str,
        params: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
    ):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse(
            (
                schema,
                f"{addr}/galileo/user_interface/v1",
                endpoint,
                params,
                query,
                fragment,
            )
        )

    def _request(
        self,
        request: Callable,
        endpoint: str,
        data: Optional[Any] = None,
        params: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
    ):
        url = self._make_url(endpoint, params, query, fragment)
        access_token = self._auth_provider.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        r = request(url, json=data, headers=headers)
        r.raise_for_status()
        return r

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request(requests.post, *args, **kwargs)

    def self(self):
        return self._get("/users/self")

    def list_users(self, query: str):
        return self._get("/users", query=query)

    def list_station_invites(self):
        return self._get("/users/invites")
