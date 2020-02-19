from typing import List, Optional
import requests

from ...data.repositories.stations import StationsRepository
from ..utils.generate_query_str import generate_query_str


class StationsService:
    def __init__(self, stations_repo: StationsRepository):
        self._stations_repo = stations_repo

    def list_stations(
        self,
        stationids: Optional[List[str]] = None,
        names: Optional[List[str]] = None,
        mids: Optional[List[str]] = None,
        user_roles: Optional[List[str]] = None,
        volumeids: Optional[List[str]] = None,
        descriptions: Optional[List[str]] = None,
        page: Optional[int] = 1,
        items: Optional[int] = 25,
    ):
        query: str = generate_query_str(
            {
                "page": page,
                "items": items,
                "stationids": stationids,
                "names": names,
                "mids": mids,
                "user_roles": user_roles,
                "volumeids": volumeids,
                "descriptions": descriptions,
            }
        )

        r = self._stations_repo.list_stations(query)
        return r.json()

    def create_station(
        self, name: str, description: str, userids: Optional[List[str]] = None
    ):
        r = self._stations_repo.create_station(name, description, userids)
        return r.json()

    def invite_to_station(self, station_id: str, userids: List[str]):
        r = self._stations_repo.invite_to_station(station_id, userids)
        return r.json()

    def accept_station_invite(self, station_id: str):
        r = self._stations_repo.accept_station_invite(station_id)
        return r.json()

    def reject_station_invite(self, station_id: str):
        r = self._stations_repo.reject_station_invite(station_id)
        return r.json()

    def request_to_join(self, station_id: str):
        r = self._stations_repo.request_to_join(station_id)
        return r.json()

    def approve_request_to_join(self, station_id: str, userids: List[str]):
        r = self._stations_repo.approve_request_to_join(station_id, userids)
        return r.json()

    def reject_request_to_join(self, station_id: str, userids: List[str]):
        r = self._stations_repo.reject_request_to_join(station_id, userids)
        return r.json()

    def leave_station(self, station_id: str):
        r = self._stations_repo.leave_station(station_id)
        return r.json()

    def remove_member_from_station(self, station_id: str, userid: str):
        r = self._stations_repo.remove_member_from_station(station_id, userid)
        return r.json()

    def delete_station(self, station_id: str):
        r = self._stations_repo.delete_station(station_id)
        return r.json()

    def add_machines_to_station(self, station_id: str, mids: List[str]):
        r = self._stations_repo.add_machines_to_station(station_id, mids)
        return r.json()

    def remove_machines_from_station(self, station_id: str, mids: List[str]):
        r = self._stations_repo.remove_machines_from_station(station_id, mids)
        return r.json()

    def add_volumes_to_station(
        self, station_id: str, name: str, mount_point: str, access: str
    ):
        r = self._stations_repo.add_volumes_to_station(
            station_id, name, mount_point, access
        )
        return r.json()

    def add_host_path_to_volume(
        self, station_id: str, volume_id: str, mid: str, host_path: str
    ):
        r = self._stations_repo.add_host_path_to_volume(
            station_id, volume_id, mid, host_path
        )
        return r.json()

    def delete_host_path_from_volume(
        self, station_id: str, volume_id: str, host_path_id: str
    ):
        r = self._stations_repo.delete_host_path_from_volume(
            station_id, volume_id, host_path_id
        )
        return r.json()

    def remove_volume_from_station(self, station_id: str, volume_id):
        r = self._stations_repo.remove_volume_from_station(station_id, volume_id)
        return r.json()
