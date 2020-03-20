from typing import Any, Callable, List, Optional
from urllib.parse import urlunparse

import requests

from galileo_sdk.business.objects.profiles import Profile, ProfileWallet
from galileo_sdk.business.objects.stations import Station
from galileo_sdk.data.repositories.stations import station_dict_to_station

from ..providers.auth import AuthProvider
from .settings import SettingsRepository


class ProfilesRepository:
    def __init__(
        self,
        settings_repository: SettingsRepository,
        auth_provider: AuthProvider,
        namespace: str,
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider
        self._namespace = namespace

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
            (schema, f"{addr}{self._namespace}", endpoint, params, query, fragment,)
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

    def self(self) -> Profile:
        response = self._get("/users/self")
        json: dict = response.json()
        return user_dict_to_profile(json)

    def list_users(self, query: str) -> List[Profile]:
        response = self._get("/users", query=query)
        json: dict = response.json()
        users: List[dict] = json["users"]
        return [user_dict_to_profile(user) for user in users]

    def list_station_invites(self) -> List[Station]:
        response = self._get("/users/invites")
        json: dict = response.json()
        stations: List[dict] = json["stations"]
        return [station_dict_to_station(station) for station in stations]


def wallet_dict_to_wallet(wallet: dict):
    return ProfileWallet(
        wallet=wallet["wallet"],
        public_key=wallet["public_key"],
        profilewalletid=wallet["profilewalletid"],
    )


def user_dict_to_profile(profile: dict):
    return Profile(
        userid=profile["userid"],
        username=profile["username"],
        mids=profile["mids"],
        wallets=[wallet_dict_to_wallet(wallet) for wallet in profile["wallets"]],
    )
