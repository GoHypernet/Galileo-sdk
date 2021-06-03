from galileo_sdk import GalileoSdk

# Must set env variables before running tests
CONFIG = "development"

# TODO Give Galileo authentication
galileo = GalileoSdk(config=CONFIG)

# TODO Changed wallets to stored_cards

def test_list_users():
    users = galileo.profiles.list_users()
    assert users is not None
    assert users[0].userid is not None
    assert users[0].username is not None
    assert users[0].lz_ids is not None
    assert users[0].stored_cards is not None


def test_get_profile():
    self = galileo.profiles.self()
    assert self is not None
    assert self.lz_ids is not None
    assert self.stored_cards is not None

# TODO Station invites list is empty
def test_list_station_invites():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )
    station_id = station.stationid
    # Create role resource policy
    role_id = station.users[0].role_id
    galileo.stations.invite_to_station(station_id, [user_id], role_id)
    
    

    station_invites = galileo.profiles.list_station_invites()
    assert station_invites is not None
    assert station_invites[0].lz_ids is not None
    assert station_invites[0].description is not None
    assert station_invites[0].users is not None
    assert station_invites[0].volumes is not None

    galileo.stations.delete_station(station_id)


galileo.disconnect()
