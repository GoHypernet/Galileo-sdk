from unittest import mock

from src.data.repositories.profiles import ProfilesRepository

BACKEND = "http://BACKEND"

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = f"{BACKEND}"
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
profile_repo = ProfilesRepository(settings_repo, auth_provider)


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == f"{BACKEND}/users":
        return MockResponse({"users": [{"profile": i} for i in range(27)]}, 200)
    elif args[0] == f"{BACKEND}/users/self":
        return MockResponse(
            {
                "userid": "userid",
                "username": "username",
                "wallets": ["0x"],
                "mids": "mids",
            },
            200,
        )
    elif args[0] == f"{BACKEND}/users/invites":
        return MockResponse({"stations": [{"invite": i} for i in range(10)]}, 200)

    return MockResponse(None, 404)


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_list_users(mocked_requests):
    # Call
    r = profile_repo.list_users(
        ["userids"],
        ["usernames"],
        ["partial_usernames"],
        ["wallets"],
        ["public_keys"],
        1,
        25,
    )

    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}/users",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json={
            "userids": ["userids"],
            "usernames": ["usernames"],
            "partial_usernames": ["partial_usernames"],
            "wallets": ["wallets"],
            "public_keys": ["public_keys"],
            "page": 1,
            "items": 25,
        },
    )

    # Assert
    assert r["users"] == [{"profile": i} for i in range(27)]
    assert r["users"][0] == {"profile": 0}
    assert len(r["users"]) == 27


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_get_profile(mocked_requests):
    # Call
    r = profile_repo.self()
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}/users/self",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r["userid"] == "userid"
    assert r["username"] == "username"
    assert r["wallets"] == ["0x"]
    assert r["mids"] == "mids"


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_list_station_invites(mocked_requests):
    # Call
    r = profile_repo.list_station_invites()
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}/users/invites",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r["stations"] == [{"invite": i} for i in range(10)]
    assert r["stations"][3] == {"invite": 3}
    assert len(r["stations"]) == 10
