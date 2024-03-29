from galileo_sdk.compat import mock
from galileo_sdk.business.objects.stations import EVolumeAccess
from galileo_sdk.data.repositories.stations import StationsRepository
from galileo_sdk.mock_response import MockResponse

BACKEND = "http://BACKEND"
NAMESPACE = "/galileo/user_interface/v1"
STATION_ID = "STATION_ID"
USER_ID = "USER_ID"
VOLUMES_ID = "VOLUMES_ID"
HOST_PATH = "HOST_PATH"
UNIVERSE_ID = "universe_id"
HEADERS = {"Authorization": "Bearer ACCESS_TOKEN", "universe-id": UNIVERSE_ID}
NAME = "STATION_NAME"
USERNAMES = ["USERNAME1", "USERNAME2"]
DESCRIPTION = "description"
MIDS = ["mid1", "mid2"]
MOUNT_POINT = "MOUNT_POINT"
ACCESS = EVolumeAccess.READWRITE
ROLE_ID = "role_id"

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
settings_repo.get_settings().universe = UNIVERSE_ID
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
stations_repo = StationsRepository(settings_repo, auth_provider, NAMESPACE)


def mocked_requests_get(*args, **kwargs):
    if args[0] == "{backend}{namespace}/stations".format(backend=BACKEND,
                                                         namespace=NAMESPACE):
        return MockResponse(
            {
                "stations": [{
                    "name":
                    "name",
                    "stationid":
                    "stationid",
                    "description":
                    "description",
                    "users": [{
                        "stationuserid": "stationuserid",
                        "userid": "userid",
                        "status": "OWNER",
                        "creation_timestamp": "date",
                        "updated_timestamp": "date",
                        "station_id": "station_id",
                        "role_id": "role_id",
                    }],
                    "mids": ["mid"],
                    "volumes": [{
                        "stationid": "stationid",
                        "name": NAME,
                        "mount_point": "mount_point",
                        "access": "rw",
                        "host_paths": [],
                        "volumeid": "volumeid",
                    }],
                    "creation_timestamp":
                    "creation_timestamp",
                    "updated_timestamp":
                    "updated_timestamp",
                    "organization_id":
                    "organization_id",
                    "status":
                    "stable",
                } for _ in range(5)]
            },
            200,
        )
    elif args[0] == "{backend}{namespace}/stations/public".format(
            backend=BACKEND, namespace=NAMESPACE):
        return MockResponse(
            {
                "stations": [{
                    "allow_auto_join": False,
                    "allowed_mission_types": None,
                    "creation_timestamp": "creation",
                    "description": DESCRIPTION,
                    "jobs_in_queue_count": 0,
                    "member_count": 1,
                    "mid_count": 0,
                    "name": NAME,
                    "resource_policy": None,
                    "stationid": STATION_ID,
                    "updated_timestamp": "updated",
                    "user_count": 2,
                    "user_status": "OWNER",
                    "volume_count": 0
                } for _ in range(5)]
            },
            200,
        )
    elif args[0] == "{backend}{namespace}/stations/{station_id}/roles".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID):
        return MockResponse(
            {
                "roles": [{
                    "add_machine": False,
                    "allowed_mission_types": [],
                    "assign_protected_user_roles": False,
                    "assign_user_roles": False,
                    "control_all_jobs": False,
                    "control_jobs_on_own_machines": False,
                    "control_own_jobs": False,
                    "create_tunnels": True,
                    "creation_timestamp": "Mon, 24 May 2021 23:03:25 GMT",
                    "description":
                    "Base users that can launch jobs in the station",
                    "edit_job_resource_limits": False,
                    "edit_machine_policy": False,
                    "edit_metadata": False,
                    "edit_own_machine_policy": False,
                    "edit_station_policy": False,
                    "edit_station_roles": False,
                    "edit_user_policy": False,
                    "id": ROLE_ID,
                    "invite_users": False,
                    "launch_jobs": True,
                    "manage_volumes": False,
                    "name": "Launcher",
                    "protected_role": False,
                    "reject_user_requests": False,
                    "remove_all_users": False,
                    "remove_any_machine": False,
                    "remove_invited_users": False,
                    "role_type": "LAUNCHER",
                    "station_id": STATION_ID,
                    "updated_timestamp": "Mon, 24 May 2021 23:03:25 GMT",
                    "view_all_jobs": False,
                    "view_all_users": False,
                    "view_complete_activity": True,
                    "view_jobs_on_own_machines": False,
                    "view_own_jobs": False
                }],
                "total_items":
                1
            },
            200,
        )
    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    if args[0] == "{backend}{namespace}/station".format(backend=BACKEND,
                                                        namespace=NAMESPACE):
        return MockResponse(
            {
                "station": {
                    "name":
                    kwargs["json"]["name"],
                    "stationid":
                    "stationid",
                    "description":
                    kwargs["json"]["description"],
                    "users": [
                        {
                            "userid": kwargs["json"]["user_ids"][0],
                            "stationuserid": "stationuserid",
                            "status": "OWNER",
                            "creation_timestamp": "date",
                            "updated_timestamp": "date",
                            "station_id": "station_id",
                            "role_id": "role_id",
                        },
                        {
                            "userid": kwargs["json"]["user_ids"][1],
                            "stationuserid": "stationuserid",
                            "status": "OWNER",
                            "creation_timestamp": "date",
                            "updated_timestamp": "date",
                            "station_id": "station_id",
                            "role_id": "role_id",
                        },
                    ],
                    "mids": ["mid"],
                    "volumes": [{
                        "stationid": "stationid",
                        "name": NAME,
                        "mount_point": "mount_point",
                        "access": "rw",
                        "host_paths": [],
                        "volumeid": "volumeid",
                    }],
                    "creation_timestamp":
                    "creation_timestamp",
                    "updated_timestamp":
                    "updated_timestamp",
                    "organization_id":
                    "organization_id",
                    "status":
                    "stable",
                }
            },
            200,
        )
    elif args[
            0] == "{backend}{namespace}/station/{station_id}/users/invite".format(
                backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID):
        return MockResponse(True, 200)
    elif args[
            0] == "{backend}{namespace}/station/{station_id}/requests".format(
                backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID):
        return MockResponse(True, 200)
    elif args[
            0] == "{backend}{namespace}/station/{station_id}/machines".format(
                backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID):
        return MockResponse(True, 200)
    elif args[0] == "{backend}{namespace}/station/{station_id}/volumes".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID):
        return MockResponse(
            {
                "volumes": {
                    "stationid": "stationid",
                    "name": NAME,
                    "mount_point": "mount_point",
                    "access": "rw",
                    "host_paths": [],
                    "volumeid": "volumeid",
                }
            },
            200,
        )
    elif args[
            0] == "{backend}{namespace}/station/{station_id}/volumes/{volumes_id}/host_paths".format(
                backend=BACKEND,
                namespace=NAMESPACE,
                station_id=STATION_ID,
                volumes_id=VOLUMES_ID,
            ):
        return MockResponse(
            {
                "volume": {
                    "stationid": "stationid",
                    "name": NAME,
                    "mount_point": "mount_point",
                    "access": "rw",
                    "host_paths": [],
                    "volumeid": "volumeid",
                }
            },
            200,
        )

    return MockResponse(None, 404)


def mocked_requests_put(*args, **kwargs):
    if args[0] == "{backend}{namespace}/station/{station_id}/users/accept".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID):
        return MockResponse(True, 200)
    elif args[
            0] == "{backend}{namespace}/station/{station_id}/users/reject".format(
                backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID):
        return MockResponse(True, 200)
    elif args[
            0] == "{backend}{namespace}/station/{station_id}/requests/approve".format(
                backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID):
        return MockResponse(True, 200)
    elif args[
            0] == "{backend}{namespace}/station/{station_id}/requests/reject".format(
                backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID):
        return MockResponse(True, 200)
    elif args[
            0] == "{backend}{namespace}/station/{station_id}/user/withdraw".format(
                backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID):
        return MockResponse(True, 200)

    return MockResponse(None, 404)


def mocked_requests_delete(*args, **kwargs):
    if args[0] == "{backend}{namespace}/station/{station_id}/user/{user_id}/delete".format(
            backend=BACKEND,
            namespace=NAMESPACE,
            station_id=STATION_ID,
            user_id=USER_ID):
        return MockResponse(True, 200)
    elif args[0] == "{backend}{namespace}/station/{station_id}".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID):
        return MockResponse(True, 200)
    elif args[
            0] == "{backend}{namespace}/station/{station_id}/machines".format(
                backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID):
        return MockResponse(True, 200)
    elif args[
            0] == "{backend}{namespace}/station/{station_id}/volumes/{volumes_id}/host_paths/{host_path}".format(
                backend=BACKEND,
                namespace=NAMESPACE,
                station_id=STATION_ID,
                volumes_id=VOLUMES_ID,
                host_path=HOST_PATH,
            ):
        return MockResponse(True, 200)
    elif args[
            0] == "{backend}{namespace}/station/{station_id}/volumes/{volumes_id}".format(
                backend=BACKEND,
                namespace=NAMESPACE,
                station_id=STATION_ID,
                volumes_id=VOLUMES_ID,
            ):
        return MockResponse(True, 200)

    return MockResponse(None, 404)


@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_list_stations(mocked_requests):
    # Call
    r = stations_repo.list_stations("")

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/stations".format(backend=BACKEND,
                                               namespace=NAMESPACE),
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert len(r) == 5
    assert len(r[0].volumes) == 1
    assert r[0].volumes[0].name == NAME


@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_get_public_stations(mocked_requests):
    # Call
    r = stations_repo.get_public_stations("")

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/stations/public".format(backend=BACKEND,
                                                      namespace=NAMESPACE),
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert len(r) == 5


@mock.patch("galileo_sdk.compat.requests.post",
            side_effect=mocked_requests_post)
def test_create_station(mocked_requests):
    # Call
    r = stations_repo.create_station(NAME, DESCRIPTION, USERNAMES)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station".format(backend=BACKEND,
                                              namespace=NAMESPACE),
        headers=HEADERS,
        json={
            "name": NAME,
            "user_ids": USERNAMES,
            "description": DESCRIPTION
        },
    )

    # Assert
    assert r.name == NAME
    assert r.description == DESCRIPTION
    assert r.users[0].user_id == USERNAMES[0]
    assert r.users[1].user_id == USERNAMES[1]


@mock.patch("galileo_sdk.compat.requests.post",
            side_effect=mocked_requests_post)
def test_invite_to_station(mocked_requests):
    # Call
    r = stations_repo.invite_to_station(STATION_ID, USERNAMES, ROLE_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/users/invite".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID),
        headers=HEADERS,
        json={
            "userids": USERNAMES,
            "role_id": "role_id"
        },
    )

    # Assert
    assert r is True


@mock.patch("galileo_sdk.compat.requests.put", side_effect=mocked_requests_put)
def test_accept_station_invite(mocked_requests):
    # Call
    r = stations_repo.accept_station_invite(STATION_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/users/accept".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID),
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r is True


@mock.patch("galileo_sdk.compat.requests.put", side_effect=mocked_requests_put)
def test_reject_station_invite(mocked_requests):
    # Call
    r = stations_repo.reject_station_invite(STATION_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/users/reject".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID),
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r is True


@mock.patch("galileo_sdk.compat.requests.post",
            side_effect=mocked_requests_post)
def test_request_to_join(mocked_requests):
    # Call
    r = stations_repo.request_to_join(STATION_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/requests".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID),
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r is True


@mock.patch("galileo_sdk.compat.requests.put", side_effect=mocked_requests_put)
def test_approve_request_to_join(mocked_requests):
    # Call
    r = stations_repo.approve_request_to_join(STATION_ID, USERNAMES)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/requests/approve".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID),
        headers=HEADERS,
        json={"userids": USERNAMES},
    )

    # Assert
    assert r is True


@mock.patch("galileo_sdk.compat.requests.put", side_effect=mocked_requests_put)
def test_reject_request_to_join(mocked_requests):
    # Call
    r = stations_repo.reject_request_to_join(STATION_ID, USERNAMES)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/requests/reject".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID),
        headers=HEADERS,
        json={"userids": USERNAMES},
    )

    # Assert
    assert r is True


@mock.patch("galileo_sdk.compat.requests.put", side_effect=mocked_requests_put)
def test_leave_station(mocked_requests):
    # Call
    r = stations_repo.leave_station(STATION_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/user/withdraw".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID),
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r is True


@mock.patch("galileo_sdk.compat.requests.delete",
            side_effect=mocked_requests_delete)
def test_remove_member_from_station(mocked_requests):
    # Call
    r = stations_repo.remove_member_from_station(STATION_ID, USER_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/user/{user_id}/delete".
        format(backend=BACKEND,
               namespace=NAMESPACE,
               station_id=STATION_ID,
               user_id=USER_ID),
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r is True


@mock.patch("galileo_sdk.compat.requests.delete",
            side_effect=mocked_requests_delete)
def test_delete_station(mocked_requests):
    # Call
    r = stations_repo.delete_station(STATION_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID),
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r is True


@mock.patch("galileo_sdk.compat.requests.post",
            side_effect=mocked_requests_post)
def test_add_lzs_to_station(mocked_requests):
    # Call
    r = stations_repo.add_lzs_to_station(STATION_ID, MIDS)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/machines".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID),
        headers=HEADERS,
        json={"mids": MIDS},
    )

    # Assert
    assert r is True


@mock.patch("galileo_sdk.compat.requests.delete",
            side_effect=mocked_requests_delete)
def test_remove_lzs_from_station(mocked_requests):
    # Call
    r = stations_repo.remove_lzs_from_station(STATION_ID, MIDS)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/machines".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID),
        headers=HEADERS,
        json={"mids": MIDS},
    )

    # Assert
    assert r is True


@mock.patch("galileo_sdk.compat.requests.post",
            side_effect=mocked_requests_post)
def test_add_volumes_to_station(mocked_requests):
    # Call
    r = stations_repo.add_volume_to_station(STATION_ID, NAME, MOUNT_POINT,
                                            ACCESS)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/volumes".format(
            backend=BACKEND, namespace=NAMESPACE, station_id=STATION_ID),
        headers=HEADERS,
        json={
            "name": NAME,
            "mount_point": MOUNT_POINT,
            "access": ACCESS.value
        },
    )

    # Assert
    assert r.name == NAME


@mock.patch("galileo_sdk.compat.requests.post",
            side_effect=mocked_requests_post)
def test_add_host_path_to_station(mocked_requests):
    # Call
    r = stations_repo.add_host_path_to_volume(STATION_ID, VOLUMES_ID, MIDS[0],
                                              HOST_PATH)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/volumes/{volumes_id}/host_paths"
        .format(
            backend=BACKEND,
            namespace=NAMESPACE,
            station_id=STATION_ID,
            volumes_id=VOLUMES_ID,
        ),
        headers=HEADERS,
        json={
            "mid": MIDS[0],
            "host_path": HOST_PATH
        },
    )

    # Assert
    assert r.name == NAME


@mock.patch("galileo_sdk.compat.requests.delete",
            side_effect=mocked_requests_delete)
def test_delete_host_path_from_station(mocked_requests):
    # Call
    r = stations_repo.delete_host_path_from_volume(STATION_ID, VOLUMES_ID,
                                                   HOST_PATH)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/volumes/{volumes_id}/host_paths/{host_path}"
        .format(
            backend=BACKEND,
            namespace=NAMESPACE,
            station_id=STATION_ID,
            volumes_id=VOLUMES_ID,
            host_path=HOST_PATH,
        ),
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r is True


@mock.patch("galileo_sdk.compat.requests.delete",
            side_effect=mocked_requests_delete)
def test_remove_volume_from_station(mocked_requests):
    # Call
    r = stations_repo.remove_volume_from_station(STATION_ID, VOLUMES_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/station/{station_id}/volumes/{volumes_id}".
        format(
            backend=BACKEND,
            namespace=NAMESPACE,
            station_id=STATION_ID,
            volumes_id=VOLUMES_ID,
        ),
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r is True
