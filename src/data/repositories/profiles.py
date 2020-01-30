from typing import Any, Callable, List, Optional
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
        return urlunparse((schema, addr, endpoint, params, query, fragment))

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
        try:
            r = request(url, json=data, headers=headers)
            return r
        except requests.exceptions.RequestException as e:
            print(e)

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request(requests.post, *args, **kwargs)

    def self(self):
        """
        Get your Galileo profile

        :return: Response with information about yourself
        """
        return self._get("/users/self")

    def list_users(
        self,
        userids: Optional[List[str]] = None,
        usernames: Optional[List[str]] = None,
        partial_usernames: Optional[List[str]] = None,
        wallets: Optional[List[str]] = None,
        public_keys: Optional[List[str]] = None,
        page: Optional[int] = None,
        items: Optional[int] = None,
    ):
        """
        Get all Galileo users and their profiles

        :param userids:
        :param usernames:
        :param partial_usernames:
        :param wallets:
        :param public_keys: optional, filter by public key
        :param page: optional, page #
        :param items: optional, items per page
        :return: Response with a list of Galileo users' profiles
        """
        return self._get(
            "/users",
            {
                "page": page,
                "items": items,
                "userids": userids,
                "usernames": usernames,
                "partial_usernames": partial_usernames,
                "wallets": wallets,
                "public_keys": public_keys,
            },
        )

    def list_station_invites(self):
        """
        Get all your station invites

        :return: Response with a list of station invites
        """
        return self._get("/users/invites")
