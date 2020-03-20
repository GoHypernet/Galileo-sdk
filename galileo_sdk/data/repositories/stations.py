import json
from typing import List, Optional
from urllib.parse import urlencode, urlunparse

import requests

from galileo_sdk.business.objects.stations import (EStationUserRole,
                                                   EVolumeAccess, Station,
                                                   StationUser,
                                                   UpdateStationRequest,
                                                   Volume, VolumeHostPath)

from ..providers.auth import AuthProvider
from .settings import SettingsRepository


class StationsRepository:
    def __init__(
        self,
        settings_repository: SettingsRepository,
        auth_provider: AuthProvider,
        namespace: str,
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider
        self._namespace = namespace

    def _make_url(self, endpoint, params="", query="", fragment=""):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse(
            (schema, f"{addr}{self._namespace}", endpoint, params, query, fragment,)
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

    def list_stations(self, query: str) -> List[Station]:
        response = self._get("/stations", query=query)
        json: dict = response.json()
        stations: List[dict] = json["stations"]
        return [station_dict_to_station(station) for station in stations]

    def create_station(
        self, name: str, description: str, userids: Optional[List[str]] = None
    ) -> Station:
        response = self._post(
            "/station",
            {"name": name, "usernames": userids, "description": description},
        )
        json: dict = response.json()
        station: dict = json["station"]
        return station_dict_to_station(station)

    def invite_to_station(self, station_id: str, userids: List[str]) -> bool:
        response = self._post(
            f"/station/{station_id}/users/invite", {"userids": userids}
        )
        return response.json()

    def accept_station_invite(self, station_id: str) -> bool:
        response = self._put(f"/station/{station_id}/users/accept")
        return response.json()

    def reject_station_invite(self, station_id: str) -> bool:
        response = self._put(f"/station/{station_id}/users/reject")
        return response.json()

    def request_to_join(self, station_id: str) -> bool:
        response = self._post(f"/station/{station_id}/users")
        return response.json()

    def approve_request_to_join(self, station_id: str, userids: List[str]) -> bool:
        response = self._put(
            f"/station/{station_id}/users/approve", {"userids": userids}
        )
        return response.json()

    def reject_request_to_join(self, station_id: str, userids: List[str]) -> bool:
        response = self._put(
            f"/station/{station_id}/users/reject", {"userids": userids}
        )
        return response.json()

    def leave_station(self, station_id: str) -> bool:
        response = self._put(f"/station/{station_id}/user/withdraw")
        return response.json()

    def remove_member_from_station(self, station_id: str, userid: str) -> bool:
        response = self._delete(f"/station/{station_id}/user/{userid}/delete")
        return response.json()

    def delete_station(self, station_id: str) -> bool:
        response = self._delete(f"/station/{station_id}")
        return response.json()

    def add_machines_to_station(self, station_id: str, mids: List[str]) -> bool:
        response = self._post(f"/station/{station_id}/machines", {"mids": mids})
        return response.json()

    def remove_machines_from_station(self, station_id: str, mids: List[str]) -> bool:
        response = self._delete(f"/station/{station_id}/machines", {"mids": mids})
        return response.json()

    def add_volumes_to_station(
        self, station_id: str, name: str, mount_point: str, access: EVolumeAccess
    ) -> Volume:
        response = self._post(
            f"/station/{station_id}/volumes",
            {"name": name, "mount_point": mount_point, "access": access.value},
        )
        json: dict = response.json()
        volume: dict = json["volumes"]
        return volume_dict_to_volume(volume)

    def add_host_path_to_volume(
        self, station_id: str, volume_id: str, mid: str, host_path: str
    ) -> Volume:
        response = self._post(
            f"/station/{station_id}/volumes/{volume_id}/host_paths",
            {"mid": mid, "host_path": host_path},
        )
        json: dict = response.json()
        volume: dict = json["volume"]
        return volume_dict_to_volume(volume)

    def delete_host_path_from_volume(
        self, station_id: str, volume_id: str, host_path_id: str
    ) -> bool:
        response = self._delete(
            f"/station/{station_id}/volumes/{volume_id}/host_paths/{host_path_id}"
        )
        return response.json()

    def remove_volume_from_station(self, station_id: str, volume_id: str) -> bool:
        response = self._delete(f"/station/{station_id}/volumes/{volume_id}")
        return response.json()

    def update_station(self, request: UpdateStationRequest) -> Station:
        response = self._put(
            f"/station/{request.station_id}",
            {"name": request.name, "description": request.description},
        )
        json: dict = response.json()
        station: dict = json["station"]
        return station_dict_to_station(station)


def host_path_dict_to_host_path(hostpath: dict):
    return VolumeHostPath(
        volumehostpathid=hostpath["volumehostpathid"],
        mid=hostpath["mid"],
        host_path=hostpath["host_path"],
    )


def volume_dict_to_volume(volume: dict):
    return Volume(
        volumeid=volume["volumeid"],
        name=volume["name"],
        mount_point=volume["mount_point"],
        stationid=volume["stationid"],
        access=EVolumeAccess(volume["access"]),
        host_paths=[
            host_path_dict_to_host_path(host_path) for host_path in volume["host_paths"]
        ],
    )


def station_dict_to_station(station: dict):
    return Station(
        stationid=station["stationid"],
        name=station["name"],
        description=station["description"],
        users=[user_dict_to_station_user(user) for user in station["users"]],
        machine_ids=station["mids"],
        volumes=[volume_dict_to_volume(volume) for volume in station["volumes"]],
    )


def user_dict_to_station_user(user: dict):
    return StationUser(
        stationuserid=user["stationuserid"],
        userid=user["userid"],
        status=EStationUserRole[user["status"]],
    )
