import json
from typing import List, Optional
from urllib.parse import urlencode, urlunparse

import requests

from ..providers.auth import AuthProvider
from .settings import SettingsRepository


class StationsRepository:
    def __init__(
        self, settings_repository: SettingsRepository, auth_provider: AuthProvider
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider

    def _make_url(self, endpoint, params="", query="", fragment=""):
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

    def _request(self, request, endpoint, data=None, params="", query="", fragment=""):
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

    def _put(self, *args, **kwargs):
        return self._request(requests.put, *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._request(requests.delete, *args, **kwargs)

    def list_stations(self, query: str):
        return self._get("/stations", query=query)

    def create_station(
        self, name: str, description: str, userids: Optional[List[str]] = None
    ):
        return self._post(
            "/station",
            {"name": name, "usernames": userids, "description": description},
        )

    def invite_to_station(self, station_id: str, userids: List[str]):
        return self._post(f"/station/{station_id}/users/invite", {"userids": userids})

    def accept_station_invite(self, station_id: str):
        return self._put(f"/station/{station_id}/users/accept")

    def reject_station_invite(self, station_id: str):
        return self._put(f"/station/{station_id}/users/reject")

    def request_to_join(self, station_id: str):
        return self._post(f"/station/{station_id}/users")

    def approve_request_to_join(self, station_id: str, userids: List[str]):
        return self._put(f"/station/{station_id}/users/approve", {"userids": userids})

    def reject_request_to_join(self, station_id: str, userids: List[str]):
        return self._put(f"/station/{station_id}/users/reject", {"userids": userids})

    def leave_station(self, station_id: str):
        return self._put(f"/station/{station_id}/user/withdraw")

    def remove_member_from_station(self, station_id: str, userid: str):
        return self._delete(f"/station/{station_id}/user/{userid}/delete")

    def delete_station(self, station_id: str):
        return self._delete(f"/station/{station_id}")

    def add_machines_to_station(self, station_id: str, mids: List[str]):
        return self._post(f"/station/{station_id}/machines", {"mids": mids})

    def remove_machines_from_station(self, station_id: str, mids: List[str]):
        return self._delete(f"/station/{station_id}/machines", {"mids": mids})

    def add_volumes_to_station(
        self, station_id: str, name: str, mount_point: str, access: str
    ):
        return self._post(
            f"/station/{station_id}/volumes",
            {"name": name, "mount_point": mount_point, "access": access},
        )

    def add_host_path_to_volume(
        self, station_id: str, volume_id: str, mid: str, host_path: str
    ):
        return self._post(
            f"/station/{station_id}/volumes/{volume_id}/host_paths",
            {"mid": mid, "host_path": host_path},
        )

    def delete_host_path_from_volume(
        self, station_id: str, volume_id: str, host_path_id: str
    ):
        return self._delete(
            f"/station/{station_id}/volumes/{volume_id}/host_paths/{host_path_id}"
        )

    def remove_volume_from_station(self, station_id: str, volume_id: str):
        return self._delete(f"/station/{station_id}/volumes/{volume_id}")
