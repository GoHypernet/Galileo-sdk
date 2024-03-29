from galileo_sdk.compat import mock
from galileo_sdk.business.objects.profiles import Profile, ProfileCard
from galileo_sdk.business.objects.stations import EStationUserRole, Station, StationUser
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
        Profile(user_id="userid",
                username="username",
                lz_ids=["mids"],
                stored_cards=[
                    ProfileCard(id="0x",
                                user_id="x",
                                stripe_payment_method_id="x",
                                creation_timestamp="x")
                ]),
        Profile(user_id="userid2",
                username="username2",
                lz_ids=["mids2"],
                stored_cards=[
                    ProfileCard(id="0x2",
                                user_id="x",
                                stripe_payment_method_id="x",
                                creation_timestamp="x")
                ]),
    ]

    # Call
    r = profile_service.list_users()

    # Assert
    assert len(r) == 2
    assert r[0].user_id == "userid"
    assert r[1].username == "username2"
    assert r[1].lz_ids[0] == "mids2"
    assert r[1].stored_cards[0].id == "0x2"


def test_get_profile():
    profile_repo.self.return_value = Profile(
        user_id="userid",
        username="username",
        lz_ids=["mids"],
        stored_cards=[
            ProfileCard(id="0x",
                        user_id="x",
                        stripe_payment_method_id="x",
                        creation_timestamp="x")
        ])

    # Call
    r = profile_service.self()

    # Assert
    assert r.user_id == "userid"
    assert r.username == "username"
    assert r.stored_cards[0].id == "0x"
    assert r.lz_ids[0] == "mids"


def test_list_station_invites():
    profile_repo.list_station_invites.return_value = [
        Station(
            station_id="stationid",
            description="description",
            name="name",
            users=[
                StationUser(
                    "stationuserid",
                    "userid",
                    EStationUserRole.ADMIN,
                    "station_id",
                    "username",
                    "role_id",
                    "creation_timestamp",
                    "updated_timestamp",
                )
            ],
        )
    ]

    # Call
    r = profile_service.list_station_invites()

    # Assert
    assert len(r) == 1
    assert r[0].station_id == "stationid"
    assert r[0].description == "description"
    assert r[0].name == "name"
