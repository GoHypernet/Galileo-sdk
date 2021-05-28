from galileo_sdk import GalileoSdk

# Must set env variables before running tests
CONFIG = "development"

# TODO Give Galileo authentication
galileo = GalileoSdk(config=CONFIG)


def test_list_users():
    users = galileo.profiles.list_users()
    assert users is not None
    assert users[0].userid is not None
    assert users[0].username is not None
    assert users[0].lz_ids is not None
    assert users[0].wallets is not None


def test_get_profile():
    self = galileo.profiles.self()
    assert self is not None
    assert self.lz_ids is not None
    assert self.wallets is not None


def test_list_station_invites():
    station_invites = galileo.profiles.list_station_invites()
    assert station_invites is not None
    assert station_invites[0].lz_ids is not None
    assert station_invites[0].description is not None
    assert station_invites[0].users is not None
    assert station_invites[0].volumes is not None


galileo.disconnect()
