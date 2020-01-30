from unittest import mock

from src.business.services.profiles import ProfilesService

BACKEND = "http://BACKEND"

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = f"{BACKEND}"
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
profile_repo = mock.Mock()
profile_service = ProfilesService(profile_repo)


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def test_list_users():
    profile_repo.list_users.return_value = MockResponse(
        {"users": [{"profile": i} for i in range(27)]}, 200
    )

    # Call
    r = profile_service.list_users()

    # Assert
    assert r["users"] == [{"profile": i} for i in range(27)]
    assert r["users"][0] == {"profile": 0}
    assert len(r["users"]) == 27


def test_get_profile():
    profile_repo.self.return_value = MockResponse(
        {
            "userid": "userid",
            "username": "username",
            "wallets": ["0x"],
            "mids": "mids",
        },
        200,
    )

    # Call
    r = profile_service.self()

    # Assert
    assert r["userid"] == "userid"
    assert r["username"] == "username"
    assert r["wallets"] == ["0x"]
    assert r["mids"] == "mids"


def test_list_station_invites():
    profile_repo.list_station_invites.return_value = MockResponse(
        {"stations": [{"invite": i} for i in range(10)]}, 200
    )

    # Call
    r = profile_service.list_station_invites()

    # Assert
    assert r["stations"] == [{"invite": i} for i in range(10)]
    assert r["stations"][3] == {"invite": 3}
    assert len(r["stations"]) == 10
