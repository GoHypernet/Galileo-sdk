from unittest import mock

from src.business.utils.generate_query_str import generate_query_str
from src.data.repositories.profiles import ProfilesRepository
from src.mock_response import MockResponse

BACKEND = "http://BACKEND"
NAMESPACE = "/galileo/user_interface/v1"
QUERY = "?userids=userids&usernames=usernames&partial_usernames=partial_usernames&wallets=wallets&public_keys=public_keys&page=1&items=25"

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = f"{BACKEND}"
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
profile_repo = ProfilesRepository(settings_repo, auth_provider)


def mocked_requests_get(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/users{QUERY}":
        return MockResponse({"users": [{"profile": i} for i in range(27)]}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/users/self":
        return MockResponse(
            {
                "userid": "userid",
                "username": "username",
                "wallets": ["0x"],
                "mids": "mids",
            },
            200,
        )
    elif args[0] == f"{BACKEND}{NAMESPACE}/users/invites":
        return MockResponse({"stations": [{"invite": i} for i in range(10)]}, 200)

    return MockResponse(None, 404)


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_list_users(mocked_requests):
    # Call

    print(
        generate_query_str(
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
    )
    r = profile_repo.list_users(
        generate_query_str(
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
    )

    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/users{QUERY}",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
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
        f"{BACKEND}{NAMESPACE}/users/self",
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
        f"{BACKEND}{NAMESPACE}/users/invites",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r["stations"] == [{"invite": i} for i in range(10)]
    assert r["stations"][3] == {"invite": 3}
    assert len(r["stations"]) == 10