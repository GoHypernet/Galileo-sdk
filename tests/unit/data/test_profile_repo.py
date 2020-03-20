from unittest import mock

from galileo_sdk.business.utils.generate_query_str import generate_query_str
from galileo_sdk.data.repositories.profiles import ProfilesRepository
from galileo_sdk.mock_response import MockResponse

BACKEND = "http://BACKEND"
NAMESPACE = "/galileo/user_interface/v1"
QUERY = generate_query_str(
    {
        "userids": ["userids"],
        "usernames": ["usernames"],
        "partial_usernames": ["partial_usernames"],
        "wallets": ["wallets"],
        "public_keys": ["public_keys"],
        "page": 1,
        "items": 25,
    }
)

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = f"{BACKEND}"
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
profile_repo = ProfilesRepository(settings_repo, auth_provider, NAMESPACE)


def mocked_requests_get(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/users":
        return MockResponse(
            {
                "users": [
                    {
                        "userid": f"user{i}",
                        "username": f"username{i}",
                        "wallets": [
                            {
                                "wallet": f"{i}",
                                "public_key": "x",
                                "profilewalletid": "x",
                            }
                        ],
                        "mids": [f"{i}"],
                    }
                    for i in range(5)
                ]
            },
            200,
        )
    elif args[0] == f"{BACKEND}{NAMESPACE}/users/self":
        return MockResponse(
            {
                "userid": "userid",
                "username": "username",
                "wallets": [
                    {"wallet": "0x", "public_key": "x", "profilewalletid": "x"}
                ],
                "mids": ["mids"],
            },
            200,
        )
    elif args[0] == f"{BACKEND}{NAMESPACE}/users/invites":
        return MockResponse(
            {
                "stations": [
                    {
                        "stationid": "stationid",
                        "name": "name",
                        "description": "description",
                        "users": [
                            {
                                "stationuserid": "stationuserid",
                                "userid": "userid",
                                "status": "ADMIN",
                            }
                        ],
                        "mids": ["1", "2"],
                        "volumes": [
                            {
                                "volumeid": "id",
                                "name": "name",
                                "mount_point": "mount_point",
                                "stationid": "stationid",
                                "access": "rw",
                                "host_paths": [
                                    {
                                        "volumehostpathid": "volumehostpathid",
                                        "mid": "mid",
                                        "host_path": "hostpath",
                                    }
                                ],
                            }
                        ],
                    }
                ]
            },
            200,
        )

    return MockResponse(None, 404)


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_list_users(mocked_requests):
    # Call
    r = profile_repo.list_users("")

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/users",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert len(r) == 5
    assert len(r[0].mids) == 1
    assert len(r[0].wallets) == 1
    for i in range(5):
        assert r[i].userid == f"user{i}"
        assert r[i].username == f"username{i}"


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_get_profile(mocked_requests):
    # Call
    r = profile_repo.self()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/users/self",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r.userid == "userid"
    assert r.username == "username"
    assert r.wallets[0].wallet == "0x"
    assert r.mids == ["mids"]


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_list_station_invites(mocked_requests):
    # Call
    r = profile_repo.list_station_invites()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/users/invites",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r[0].stationid == "stationid"
    assert r[0].mids[0] == "1"
    assert r[0].name == "name"
    assert r[0].users[0].stationuserid == "stationuserid"
