import os

from galileo_sdk import GalileoSdk

# Must set env variables before running tests
CONFIG = "development"

galileo = GalileoSdk(config=CONFIG)


def test_list_users():
    users = galileo.profiles.list_users()
    assert not users == None
    assert "users" in users
    assert "userid" in users["users"][0]
    assert "username" in users["users"][0]
    assert "wallets" in users["users"][0]


def test_get_profile():
    self = galileo.profiles.self()
    print(self)
    assert not self == None
    assert "mids" in self
    assert "wallets" in self


def test_list_station_invites():
    station_invites = galileo.profiles.list_station_invites()
    assert not station_invites == None
    assert "stations" in station_invites


galileo.disconnect()
