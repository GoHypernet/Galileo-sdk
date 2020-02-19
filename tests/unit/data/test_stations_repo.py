from unittest import mock

from src.data.repositories.stations import StationsRepository
from src.mock_response import MockResponse

BACKEND = "http://BACKEND"
NAMESPACE = "/galileo/user_interface/v1"
STATION_ID = "STATION_ID"
USER_ID = "USER_ID"
VOLUMES_ID = "VOLUMES_ID"
HOST_PATH = "HOST_PATH"
HEADERS = {"Authorization": f"Bearer ACCESS_TOKEN"}
NAME = "STATION_NAME"
USERNAMES = ["USERNAME1", "USERNAME2"]
DESCRIPTION = "description"
MIDS = ["mid1", "mid2"]
MOUNT_POINT = "MOUNT_POINT"
ACCESS = "rw"

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = f"{BACKEND}"
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
stations_repo = StationsRepository(settings_repo, auth_provider)


def mocked_requests_get(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/stations":
        return MockResponse({"stations": [{"stations": i} for i in range(10)]}, 200)

    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/station":
        return MockResponse(
            {
                "station": {
                    "name": kwargs["json"]["name"],
                    "stationid": "stationid",
                    "description": kwargs["json"]["description"],
                    "users": kwargs["json"]["usernames"],
                    "mids": ["mid"],
                    "volumes": [],
                }
            },
            200,
        )
    elif args[0] == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/users/invite":
        return MockResponse(True, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/users":
        return MockResponse(True, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/machines":
        return MockResponse(True, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/volumes":
        return MockResponse({"volumes": "volume"}, 200)
    elif (
        args[0]
        == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/volumes/{VOLUMES_ID}/host_paths"
    ):
        return MockResponse({"volume": "volume"}, 200)

    return MockResponse(None, 404)


def mocked_requests_put(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/users/accept":
        return MockResponse(True, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/users/reject":
        return MockResponse(True, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/users/approve":
        return MockResponse(True, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/users/reject":
        return MockResponse(True, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/user/withdraw":
        return MockResponse(True, 200)

    return MockResponse(None, 404)


def mocked_requests_delete(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/user/{USER_ID}/delete":
        return MockResponse(True, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}":
        return MockResponse(True, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/machines":
        return MockResponse(True, 200)
    elif (
        args[0]
        == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/volumes/{VOLUMES_ID}/host_paths/{HOST_PATH}"
    ):
        return MockResponse(True, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/volumes/{VOLUMES_ID}":
        return MockResponse(True, 200)

    return MockResponse(None, 404)


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_list_stations(mocked_requests):
    # Call
    r = stations_repo.list_stations("")
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/stations", headers=HEADERS, json=None,
    )

    # Assert
    assert r["stations"] == [{"stations": i} for i in range(10)]
    assert r["stations"][0] == {"stations": 0}
    assert len(r["stations"]) == 10


@mock.patch("requests.post", side_effect=mocked_requests_post)
def test_create_station(mocked_requests):
    # Call
    r = stations_repo.create_station(NAME, DESCRIPTION, USERNAMES)
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station",
        headers=HEADERS,
        json={"name": NAME, "usernames": USERNAMES, "description": DESCRIPTION,},
    )

    # Assert
    assert r["station"]["name"] == NAME
    assert r["station"]["description"] == DESCRIPTION
    assert r["station"]["users"] == USERNAMES


@mock.patch("requests.post", side_effect=mocked_requests_post)
def test_invite_to_station(mocked_requests):
    # Call
    r = stations_repo.invite_to_station(STATION_ID, USERNAMES)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/users/invite",
        headers=HEADERS,
        json={"userids": USERNAMES},
    )

    # Assert
    assert r.status_code == 200
    assert r.json() == True


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_accept_station_invite(mocked_requests):
    # Call
    r = stations_repo.accept_station_invite(STATION_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/users/accept",
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r.status_code == 200
    assert r.json() == True


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_reject_station_invite(mocked_requests):
    # Call
    r = stations_repo.reject_station_invite(STATION_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/users/reject",
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r.status_code == 200
    assert r.json() == True


@mock.patch("requests.post", side_effect=mocked_requests_post)
def test_request_to_join(mocked_requests):
    # Call
    r = stations_repo.request_to_join(STATION_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/users", headers=HEADERS, json=None
    )

    # Assert
    assert r.status_code == 200
    assert r.json() == True


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_approve_request_to_join(mocked_requests):
    # Call
    r = stations_repo.approve_request_to_join(STATION_ID, USERNAMES)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/users/approve",
        headers=HEADERS,
        json={"userids": USERNAMES},
    )

    # Assert
    assert r.status_code == 200
    assert r.json() == True


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_reject_request_to_join(mocked_requests):
    # Call
    r = stations_repo.reject_request_to_join(STATION_ID, USERNAMES)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/users/reject",
        headers=HEADERS,
        json={"userids": USERNAMES},
    )

    # Assert
    assert r.status_code == 200
    assert r.json() == True


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_leave_station(mocked_requests):
    # Call
    r = stations_repo.leave_station(STATION_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/user/withdraw",
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r.status_code == 200
    assert r.json() == True


@mock.patch("requests.delete", side_effect=mocked_requests_delete)
def test_remove_member_from_station(mocked_requests):
    # Call
    r = stations_repo.remove_member_from_station(STATION_ID, USER_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/user/{USER_ID}/delete",
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r.status_code == 200
    assert r.json() == True


@mock.patch("requests.delete", side_effect=mocked_requests_delete)
def test_delete_station(mocked_requests):
    # Call
    r = stations_repo.delete_station(STATION_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}", headers=HEADERS, json=None
    )

    # Assert
    assert r.status_code == 200
    assert r.json() == True


@mock.patch("requests.post", side_effect=mocked_requests_post)
def test_add_machines_to_station(mocked_requests):
    # Call
    r = stations_repo.add_machines_to_station(STATION_ID, MIDS)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/machines",
        headers=HEADERS,
        json={"mids": MIDS},
    )

    # Assert
    assert r.status_code == 200
    assert r.json() == True


@mock.patch("requests.delete", side_effect=mocked_requests_delete)
def test_remove_machines_from_station(mocked_requests):
    # Call
    r = stations_repo.remove_machines_from_station(STATION_ID, MIDS)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/machines",
        headers=HEADERS,
        json={"mids": MIDS},
    )

    # Assert
    assert r.status_code == 200
    assert r.json() == True


@mock.patch("requests.post", side_effect=mocked_requests_post)
def test_add_volumes_to_station(mocked_requests):
    # Call
    r = stations_repo.add_volumes_to_station(STATION_ID, NAME, MOUNT_POINT, ACCESS)
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/volumes",
        headers=HEADERS,
        json={"name": NAME, "mount_point": MOUNT_POINT, "access": ACCESS},
    )

    # Assert
    assert r["volumes"] == "volume"


@mock.patch("requests.post", side_effect=mocked_requests_post)
def test_add_host_path_to_station(mocked_requests):
    # Call
    r = stations_repo.add_host_path_to_volume(
        STATION_ID, VOLUMES_ID, MIDS[0], HOST_PATH
    )
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/volumes/{VOLUMES_ID}/host_paths",
        headers=HEADERS,
        json={"mid": MIDS[0], "host_path": HOST_PATH},
    )

    # Assert
    assert r["volume"] == "volume"


@mock.patch("requests.delete", side_effect=mocked_requests_delete)
def test_delete_host_path_from_station(mocked_requests):
    # Call
    r = stations_repo.delete_host_path_from_volume(STATION_ID, VOLUMES_ID, HOST_PATH)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/volumes/{VOLUMES_ID}/host_paths/{HOST_PATH}",
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r.status_code == 200
    assert r.json() == True


@mock.patch("requests.delete", side_effect=mocked_requests_delete)
def test_remove_volume_from_station(mocked_requests):
    # Call
    r = stations_repo.remove_volume_from_station(STATION_ID, VOLUMES_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/station/{STATION_ID}/volumes/{VOLUMES_ID}",
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r.status_code == 200
    assert r.json() == True
