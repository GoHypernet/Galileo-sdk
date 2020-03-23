import mock
from galileo_sdk.business.objects.profiles import Profile, ProfileWallet
from galileo_sdk.business.objects.stations import (EStationUserRole, Station,
                                                   StationUser)
from galileo_sdk.business.services.profiles import ProfilesService

BACKEND = "http://BACKEND"

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
profile_repo = mock.Mock()
profile_service = ProfilesService(profile_repo)


def test_list_users():
    profile_repo.list_users.return_value = [
        Profile("userid", "username", ["mids"], [ProfileWallet("0x", "x", "x")]),
        Profile("userid2", "username2", ["mids2"], [ProfileWallet("0x2", "x2", "x2")]),
    ]

    # Call
    r = profile_service.list_users()

    # Assert
    assert len(r) == 2
    assert r[0].userid == "userid"
    assert r[1].username == "username2"
    assert r[1].mids[0] == "mids2"
    assert r[1].wallets[0].wallet == "0x2"


def test_get_profile():
    profile_repo.self.return_value = Profile(
        "userid", "username", ["mids"], [ProfileWallet("0x", "x", "x")]
    )

    # Call
    r = profile_service.self()

    # Assert
    assert r.userid == "userid"
    assert r.username == "username"
    assert r.wallets[0].wallet == "0x"
    assert r.mids[0] == "mids"


def test_list_station_invites():
    profile_repo.list_station_invites.return_value = [
        Station(
            stationid="stationid",
            description="description",
            name="name",
            users=[StationUser("stationuserid", "userid", EStationUserRole.ADMIN)],
        )
    ]

    # Call
    r = profile_service.list_station_invites()

    # Assert
    assert len(r) == 1
    assert r[0].stationid == "stationid"
    assert r[0].description == "description"
    assert r[0].name == "name"
