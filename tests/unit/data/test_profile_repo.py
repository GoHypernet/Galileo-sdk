from galileo_sdk.compat import mock
from galileo_sdk.business.utils.generate_query_str import generate_query_str
from galileo_sdk.data.repositories.profiles import ProfilesRepository
from galileo_sdk.mock_response import MockResponse

BACKEND = "http://BACKEND"
NAMESPACE = "/galileo/user_interface/v1"
UNIVERSE_ID = "universe_id"
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
settings_repo.get_settings().backend = BACKEND
settings_repo.get_settings().universe = UNIVERSE_ID
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
profile_repo = ProfilesRepository(settings_repo, auth_provider, NAMESPACE)

def mocked_requests_get(*args, **kwargs):
    if args[0] == "{backend}{namespace}/users".format(
        backend=BACKEND, namespace=NAMESPACE
    ):
        return MockResponse(
            {
                "users": [
                    {
                        "userid": "user{i}".format(i=i),
                        "username": "username{i}".format(i=i),
                        "stored_cards": [
                            {
                                "id": "x",
                                "user_id": "user{i}".format(i=i),
                                "stripe_payment_method_id": "stripe{i}".format(i=1),
                                "creation_timestamp": "timestamp{i}".format(i=i)
                            }
                        ],
                        "mids": ["{i}".format(i=i)],
                    }
                    for i in range(5)
                ]
            },
            200,
        )
    elif args[0] == "{backend}{namespace}/users/self".format(
        backend=BACKEND, namespace=NAMESPACE
    ):
        return MockResponse(
            {
                "userid": "userid",
                "username": "username",
                "stored_cards": [
                    {
                        "id": "0x",
                        "user_id": "userid",
                        "stripe_payment_method_id": "stripeid",
                        "creation_timestamp": "timestamp"
                    }
                ],
                "mids": ["mids"],
            },
            200,
        )
    elif args[0] == "{backend}{namespace}/users/invites".format(
        backend=BACKEND, namespace=NAMESPACE
    ):
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
                                "creation_timestamp": "date",
                                "updated_timestamp": "date",
                                "station_id": "station_id",
                                "role_id": "role_id",
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
                        "creation_timestamp": "creation_timestamp",
                        "updated_timestamp": "updated_timestamp",
                        "organization_id": "organization_id",
                        "status": "stable",
                    }
                ]
            },
            200,
        )

    return MockResponse(None, 404)


@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_list_users(mocked_requests):
    # Call
    r = profile_repo.list_users("")

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/users".format(backend=BACKEND, namespace=NAMESPACE),
          headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID,
            },
        json=None,
    )

    # Assert
    assert len(r) == 5
    assert len(r[0].lz_ids) == 1
    assert len(r[0].stored_cards) == 1
    for i in range(5):
        assert r[i].user_id == "user{i}".format(i=i)
        assert r[i].username == "username{i}".format(i=i)


@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_get_profile(mocked_requests):
    # Call
    r = profile_repo.self()

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/users/self".format(backend=BACKEND, namespace=NAMESPACE),
          headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID,
            },
        json=None,
    )

    # Assert
    assert r.user_id == "userid"
    assert r.username == "username"
    assert r.stored_cards[0].id == "0x"
    assert r.lz_ids == ["mids"]


@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_list_station_invites(mocked_requests):
    # Call
    r = profile_repo.list_station_invites()

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/users/invites".format(
            backend=BACKEND, namespace=NAMESPACE
        ),
          headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID,
            },
        json=None,
    )

    # Assert
    assert r[0].station_id == "stationid"
    assert r[0].lz_ids[0] == "1"
    assert r[0].name == "name"
    assert r[0].users[0].stationuser_id == "stationuserid"
