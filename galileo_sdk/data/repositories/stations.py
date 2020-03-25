from galileo_sdk.compat import urlunparse, requests

from galileo_sdk.business.objects.stations import (EStationUserRole,
                                                   EVolumeAccess, Station,
                                                   StationUser,
                                                   Volume, VolumeHostPath)


class StationsRepository:
    def __init__(
        self, settings_repository, auth_provider, namespace,
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider
        self._namespace = namespace

    def _make_url(self, endpoint, params="", query="", fragment=""):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse(
            (
                schema,
                "{addr}{namespace}".format(addr=addr, namespace=self._namespace),
                endpoint,
                params,
                query,
                fragment,
            )
        )

    def _request(self, request, endpoint, data=None, params="", query="", fragment=""):
        url = self._make_url(endpoint, params, query, fragment)
        access_token = self._auth_provider.get_access_token()
        headers = {
            "Authorization": "Bearer {access_token}".format(access_token=access_token)
        }
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

    def list_stations(self, query):
        response = self._get("/stations", query=query)
        json = response.json()
        stations = json["stations"]
        return [station_dict_to_station(station) for station in stations]

    def create_station(self, name, description, userids=None):
        response = self._post(
            "/station",
            {"name": name, "usernames": userids, "description": description},
        )
        json = response.json()
        station = json["station"]
        return station_dict_to_station(station)

    def invite_to_station(self, station_id, userids):
        response = self._post(
            "/station/{station_id}/users/invite".format(station_id=station_id),
            {"userids": userids},
        )
        return response.json()

    def accept_station_invite(self, station_id):
        response = self._put(
            "/station/{station_id}/users/accept".format(station_id=station_id)
        )
        return response.json()

    def reject_station_invite(self, station_id):
        response = self._put(
            "/station/{station_id}/users/reject".format(station_id=station_id)
        )
        return response.json()

    def request_to_join(self, station_id):
        response = self._post(
            "/station/{station_id}/users".format(station_id=station_id)
        )
        return response.json()

    def approve_request_to_join(self, station_id, userids):
        response = self._put(
            "/station/{station_id}/users/approve".format(station_id=station_id),
            {"userids": userids},
        )
        return response.json()

    def reject_request_to_join(self, station_id, userids):
        response = self._put(
            "/station/{station_id}/users/reject".format(station_id=station_id),
            {"userids": userids},
        )
        return response.json()

    def leave_station(self, station_id):
        response = self._put(
            "/station/{station_id}/user/withdraw".format(station_id=station_id)
        )
        return response.json()

    def remove_member_from_station(self, station_id, userid):
        response = self._delete(
            "/station/{station_id}/user/{userid}/delete".format(
                station_id=station_id, userid=userid
            )
        )
        return response.json()

    def delete_station(self, station_id):
        response = self._delete("/station/{station_id}".format(station_id=station_id))
        return response.json()

    def add_machines_to_station(self, station_id, mids):
        response = self._post(
            "/station/{station_id}/machines".format(station_id=station_id),
            {"mids": mids},
        )
        return response.json()

    def remove_machines_from_station(self, station_id, mids):
        response = self._delete(
            "/station/{station_id}/machines".format(station_id=station_id),
            {"mids": mids},
        )
        return response.json()

    def add_volumes_to_station(self, station_id, name, mount_point, access):
        response = self._post(
            "/station/{station_id}/volumes".format(station_id=station_id),
            {"name": name, "mount_point": mount_point, "access": access.value},
        )
        json = response.json()
        volume = json["volumes"]
        return volume_dict_to_volume(volume)

    def add_host_path_to_volume(self, station_id, volume_id, mid, host_path):
        response = self._post(
            "/station/{station_id}/volumes/{volume_id}/host_paths".format(
                station_id=station_id, volume_id=volume_id
            ),
            {"mid": mid, "host_path": host_path},
        )
        json = response.json()
        volume = json["volume"]
        return volume_dict_to_volume(volume)

    def delete_host_path_from_volume(self, station_id, volume_id, host_path_id):
        response = self._delete(
            "/station/{station_id}/volumes/{volume_id}/host_paths/{host_path_id}".format(
                station_id=station_id, volume_id=volume_id, host_path_id=host_path_id
            )
        )
        return response.json()

    def remove_volume_from_station(self, station_id, volume_id):
        response = self._delete(
            "/station/{station_id}/volumes/{volume_id}".format(
                station_id=station_id, volume_id=volume_id
            )
        )
        return response.json()

    def update_station(self, request):
        response = self._put(
            "/station/{station_id}".format(station_id=request.station_id),
            {"name": request.name, "description": request.description},
        )
        json = response.json()
        station = json["station"]
        return station_dict_to_station(station)


def host_path_dict_to_host_path(hostpath):
    return VolumeHostPath(
        volumehostpathid=hostpath["volumehostpathid"],
        mid=hostpath["mid"],
        host_path=hostpath["host_path"],
    )


def volume_dict_to_volume(volume):
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


def station_dict_to_station(station):
    return Station(
        stationid=station["stationid"],
        name=station["name"],
        description=station["description"],
        users=[user_dict_to_station_user(user) for user in station["users"]],
        machine_ids=station["mids"],
        volumes=[volume_dict_to_volume(volume) for volume in station["volumes"]],
    )


def user_dict_to_station_user(user):
    return StationUser(
        stationuserid=user["stationuserid"],
        userid=user["userid"],
        status=EStationUserRole[user["status"]],
    )
