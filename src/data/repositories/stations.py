from urllib.parse import urlunparse

import requests


class StationsRepository:
    def __init__(self, settings_repository, access_token):
        self._settings_repository = settings_repository
        self._access_token = access_token
        self._headers = {"Authorization": f"Bearer {self._access_token}"}

    def _make_url(self, endpoint, params="", query="", fragment=""):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse((schema, backend, endpoint, params, query, fragment))

    def _request(self, request, endpoint, data=None, params="", query="", fragment=""):
        url = self._make_url(endpoint, params, query, fragment)
        return request(url, json=data, headers=self._headers)

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request(requests.post, *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request(requests.put, *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._request(requests.delete, *args, **kwargs)

    def list_stations(
        self,
        page=1,
        items=25,
        stationids=None,
        names=None,
        mids=None,
        user_roles=None,
        volumeids=None,
        descriptions=None,
    ):
        """
        List Galileo stations

        :param page: optional, page #
        :param items: optional, items per page
        :param stationids: optional, filter based on stationids
        :param names: optional, filter based on names
        :param mids: optional, filter based on mids
        :param user_roles: optional, filter based on user roles
        :param volumeids: optional, filter based on volumeids
        :param descriptions: optional, filter based on descriptions
        :return:
        """
        self._get(
            "/stations",
            {
                page,
                items,
                stationids,
                names,
                mids,
                user_roles,
                volumeids,
                descriptions,
            },
        )

    def create_station(self, name, usernames, description=""):
        """
        Create a new station

        :param name:
        :param usernames:
        :param description:
        :return: Response with object of the station created
        """
        return self._post("/station", {name, usernames, description})

    def invite_to_station(self, station_id, userids):
        """
        Invite user(s) to a station

        :param userids: list of user's ids
        :param station_id: station's id
        :return: boolean for success
        """
        return self._post(f"/station/{station_id}/users/invite", {userids})

    def accept_station_invite(self, station_id):
        """
        Accept an invitation to join a station

        :param station_id: station's id
        :return: boolean, True for success
        """
        return self._put(f"/station/{station_id}/users/accept")

    def reject_station_invite(self, station_id):
        """
        Reject an invitation to join a station

        :param station_id: station's id
        :return: boolean, True for success
        """
        return self._put(f"/station/{station_id}/users/reject")

    def request_to_join(self, station_id):
        """
        Request to join a station

        :param station_id: station's id
        :return: boolean, True for success
        """
        return self._post(f"/station/{station_id}/users")

    def approve_to_join(self, station_id, userids):
        """
        Admins and owners can approve members to join a station

        :param station_id: station's id
        :param userids: list of user ids that will be approved
        :return: boolean, True for success
        """
        return self._put(f"/station/{station_id}/users", {userids})

    def reject_to_join(self, station_id, userids):
        """
        Admins and owners can reject members that want to join a station

        :param station_id: station's id
        :param userids: list of user ids that will be rejected
        :return: boolean, True for success
        """
        return self._put(f"/station/{station_id}/users", {userids})

    def leave_station(self, station_id):
        """
        Leave a station as a member

        :param station_id: station's id
        :return: boolean, True for success
        """
        return self._put(f"/station/{station_id}/user/withdraw")

    def remove_member_from_station(self, station_id, userid):
        """
        Remove a member from a station

        :param station_id: station's id
        :param userid: the id of the user you want to remove
        :return: boolean, True for success
        """
        return self._delete(f"/station/{station_id}/user/{userid}/delete")

    def delete_station(self, station_id):
        """
        Permanently delete a station

        :param station_id: station's id
        :return: boolean, True for success
        """
        return self._delete(f"/station/{station_id}")

    def add_machines_to_station(self, station_id, mids):
        """
        Add machines to a station

        :param station_id: station's id
        :param mids: list of machine ids that will be added
        :return: boolean, True for success
        """
        return self._post(f"/station/{station_id}/machines", {mids})

    def remove_machines_from_station(self, station_id, mids):
        """
        Remove machines from a station

        :param station_id: station's id
        :param mids: list of machine ids that will be added
        :return: boolean, True for success
        """
        return self._delete(f"/station/{station_id}/machines", {mids})

    def add_volumes_to_station(self, station_id, name, mount_point, access):
        """
        Add volumes to a station

        :param station_id: station's id
        :param name: volume name
        :param mount_point: directory path from inside the container
        :param access: read/write access: either 'r' or 'rw'
        :return: {"volumes": Volume}
        """
        return self._post(f"/station/{station_id}/volumes", {name, mount_point, access})

    def add_host_path_to_volume(self, station_id, volume_id, mid, host_path):
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
            f"/station/{station_id}/volumes/{volume_id}/host_paths", {mid, host_path},
        )

    def remove_host_path_from_volume(self, station_id, volume_id, host_path_id):
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
