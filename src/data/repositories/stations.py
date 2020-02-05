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
        try:
            r = request(url, json=data, headers=headers)
            return r
        except requests.exceptions.RequestException as e:
            print(e)

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

    def create_station(self, name: str, userids: List[str], description: str):
        """
        Create a new station

        :param name: name of station
        :param userids: list of members's user ids to invite
        :param description: description of station
        :return: Response with object of the station created
        """
        return self._post(
            "/station",
            {"name": name, "usernames": userids, "description": description},
        )

    def invite_to_station(self, station_id: str, userids: List[str]):
        """
        Invite user(s) to a station

        :param userids: list of user's ids
        :param station_id: station's id
        :return: boolean for success
        """
        return self._post(f"/station/{station_id}/users/invite", {"userids": userids})

    def accept_station_invite(self, station_id: str):
        """
        Accept an invitation to join a station

        :param station_id: station's id
        :return: boolean, True for success
        """
        return self._put(f"/station/{station_id}/users/accept")

    def reject_station_invite(self, station_id: str):
        """
        Reject an invitation to join a station

        :param station_id: station's id
        :return: boolean, True for success
        """
        return self._put(f"/station/{station_id}/users/reject")

    def request_to_join(self, station_id: str):
        """
        Request to join a station

        :param station_id: station's id
        :return: boolean, True for success
        """
        return self._post(f"/station/{station_id}/users")

    def approve_request_to_join(self, station_id: str, userids: List[str]):
        """
        Admins and owners can approve members to join a station

        :param station_id: station's id
        :param userids: list of user ids that will be approved
        :return: boolean, True for success
        """
        return self._put(f"/station/{station_id}/users/approve", {"userids": userids})

    def reject_request_to_join(self, station_id: str, userids: List[str]):
        """
        Admins and owners can reject members that want to join a station

        :param station_id: station's id
        :param userids: list of user ids that will be rejected
        :return: boolean, True for success
        """
        return self._put(f"/station/{station_id}/users/reject", {"userids": userids})

    def leave_station(self, station_id: str):
        """
        Leave a station as a member

        :param station_id: station's id
        :return: boolean, True for success
        """
        return self._put(f"/station/{station_id}/user/withdraw")

    def remove_member_from_station(self, station_id: str, userid: str):
        """
        Remove a member from a station

        :param station_id: station's id
        :param userid: the id of the user you want to remove
        :return: boolean, True for success
        """
        return self._delete(f"/station/{station_id}/user/{userid}/delete")

    def delete_station(self, station_id: str):
        """
        Permanently delete a station

        :param station_id: station's id
        :return: boolean, True for success
        """
        return self._delete(f"/station/{station_id}")

    def add_machines_to_station(self, station_id: str, mids: List[str]):
        """
        Add machines to a station

        :param station_id: station's id
        :param mids: list of machine ids that will be added
        :return: boolean, True for success
        """
        return self._post(f"/station/{station_id}/machines", {"mids": mids})

    def remove_machines_from_station(self, station_id: str, mids: List[str]):
        """
        Remove machines from a station

        :param station_id: station's id
        :param mids: list of machine ids that will be added
        :return: boolean, True for success
        """
        return self._delete(f"/station/{station_id}/machines", {"mids": mids})

    def add_volumes_to_station(
        self, station_id: str, name: str, mount_point: str, access: str
    ):
        """
        Add volumes to a station

        :param station_id: station's id
        :param name: volume name
        :param mount_point: directory path from inside the container
        :param access: read/write access: either 'r' or 'rw'
        :return: {"volumes": Volume}
        """
        return self._post(
            f"/station/{station_id}/volumes",
            {"name": name, "mount_point": mount_point, "access": access},
        )

    def add_host_path_to_volume(
        self, station_id: str, volume_id: str, mid: str, host_path: str
    ):
        """
        Add host path to volume before running a job
        Host path is where the landing zone will store the results of a job

        :param station_id: station's id
        :param volume_id: volume's id
        :param mid: machine id
        :param host_path: directory path for landing zone
        :return: {"volume": Volume}
        """
        return self._post(
            f"/station/{station_id}/volumes/{volume_id}/host_paths",
            {"mid": mid, "host_path": host_path},
        )

    def delete_host_path_from_volume(
        self, station_id: str, volume_id: str, host_path_id: str
    ):
        """
        Remove a host path
        Host path is where the landing zone will store the results of a job

        :param station_id: station's id
        :param volume_id: volume's id
        :param host_path_id: host path id
        :return: boolean, True for success
        """

        return self._delete(
            f"/station/{station_id}/volumes/{volume_id}/host_paths/{host_path_id}"
        )

    def remove_volume_from_station(self, station_id: str, volume_id: str):
        """
        Remove a volume from station
        :param station_id: station's id
        :param volume_id: volume's id
        :return: boolean, True for success
        """
        return self._delete(f"/station/{station_id}/volumes/{volume_id}")
