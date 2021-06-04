from galileo_sdk import GalileoSdk, ResourcePolicy, StationRole, EVolumeAccess

# Must set env variables before running tests

# Many of these are not used
CONFIG = "development"
STATION_ID = "86a32c0b-bad0-456b-b41a-cb2bef9cdafb"
LZ_ID = "Jaguar2121"
ROLE_ID = "b67bb82c-f939-4c22-a341-9904675b7c92"

galileo = GalileoSdk(config=CONFIG)
user = galileo.profiles.self()
MISSION_TYPE_ID = "stata_stata"


def test_list_stations():
    station_list = galileo.stations.list_stations()
    assert station_list is not None


def test_create_and_delete_station():
    station_details = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )

    r_delete_station = galileo.stations.delete_station(station_details.stationid)

    assert "sdk_station_integration_test" == station_details.name
    assert station_details.stationid is not ""
    assert r_delete_station['success'] is True


def test_add_and_remove_volumes_to_station():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )
    volumes = galileo.stations.add_volumes_to_station(
        station_id=station.stationid,
        name="volume",
        mount_point="mount_point",
        access=EVolumeAccess.READWRITE,
    )
    r_remove_volume = galileo.stations.remove_volume_from_station(
        station_id=station.stationid, volume_id=volumes.volumeid
    )

    r_delete_station = galileo.stations.delete_station(station.stationid)

    assert EVolumeAccess.READWRITE == volumes.access
    assert "mount_point" == volumes.mount_point
    assert r_remove_volume['success'] is True
    assert r_delete_station['success'] is True


def test_add_and_delete_host_path_to_volume():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )

    self = galileo.profiles.self()

    station_id = station.stationid

    volumes = galileo.stations.add_volumes_to_station(
        station_id=station_id,
        name="volume",
        mount_point="mount_point",
        access=EVolumeAccess.READWRITE,
    )

    volume_host_path = galileo.stations.add_host_path_to_volume(
        station_id=station_id,
        volume_id=volumes.volumeid,
        lz_id=self.lz_ids[0],
        host_path="host_path",
    )

    deleted_host_path = galileo.stations.delete_host_path_from_volume(
        station_id=station_id,
        volume_id=volumes.volumeid,
        host_path_id=volume_host_path.host_paths[0].volumehostpathid,
    )

    galileo.stations.delete_station(station_id)

    assert [] == volumes.host_paths
    assert "host_path" == volume_host_path.host_paths[0].host_path
    assert deleted_host_path['success'] is True


def test_create_station_resource_policy():

    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )
    station_id = station.stationid

    policy = galileo.stations.update_station_resource_policy(station_id)
    assert isinstance(policy, ResourcePolicy)

    galileo.stations.delete_station(station_id)


def test_get_station_resource_policy():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )
    station_id = station.stationid

    # Create resource policy
    galileo.stations.update_station_resource_policy(station_id)

    # Get Resource policy
    policy = galileo.stations.get_station_resource_policy(station_id)

    assert isinstance(policy, ResourcePolicy)
    galileo.stations.delete_station(station_id)


def test_delete_station_resource_policy():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )
    station_id = station.stationid

    # Create resource policy
    galileo.stations.update_station_resource_policy(station_id)

    # Delete resource policy
    response = galileo.stations.delete_station_resource_policy(station_id)
    assert response['success'] is True

    galileo.stations.delete_station(station_id)



def test_self_resource_limits():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )
    
    station_id = station.stationid
    user_id = galileo.profiles.self().userid
    lz_id = galileo.lz.list_lz(userids=[user_id])[0].lz_id

    galileo.stations.add_lz_to_station(station_id, [lz_id])
    
    # Create resource policy
    galileo.stations.update_station_resource_policy(station_id)
    
    policy, lz_id = galileo.stations.get_self_station_resource_limits(station_id)
    assert isinstance(policy, ResourcePolicy)

    galileo.stations.delete_station(station_id)

def test_create_station_user_resource_policy():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )

    station_id = station.stationid
    
    # Create resource policy
    policy = galileo.stations.update_station_user_resource_policy(station_id, user.userid, max_cpu_per_job=10000)
    
    assert isinstance(policy, ResourcePolicy)
    galileo.stations.delete_station(station_id)


def test_get_station_user_resource_policy():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )
    station_id = station.stationid

    # Create resource policy
    galileo.stations.update_station_user_resource_policy(station_id, user.userid, max_cpu_per_job=10000)
    policy = galileo.stations.get_station_user_resource_policy(station_id, user.userid)
    
    assert isinstance(policy, ResourcePolicy)
    galileo.stations.delete_station(station_id)


def test_delete_station_user_resource_policy():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )
    station_id = station.stationid
    # Create user resource policy 
    galileo.stations.update_station_user_resource_policy(station_id, user.userid, max_cpu_per_job=10000)
    # Delete user resource policy
    response = galileo.stations.delete_station_user_resource_policy(station_id, user.userid)
    policy = galileo.stations.get_station_user_resource_policy(station_id, user.userid)

    assert response["success"] is True
    assert policy is None

    galileo.stations.delete_station(station_id)

def test_update_station_role_resource_policy():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )
    station_id = station.stationid

    resource_policy = galileo.stations.update_station_role_resource_policy(
        station_id, ROLE_ID, max_cpu_per_job=1
    )
    assert resource_policy.max_cpu_per_job == 1

    galileo.stations.delete_station(station_id)

def test_get_station_role_resource_policy():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )
    station_id = station.stationid
    # Create role resource policy
    galileo.stations.update_station_role_resource_policy(
            station_id, ROLE_ID, max_cpu_per_job=1
        )

    resource_policy = galileo.stations.get_station_role_resource_policy(
        station_id, ROLE_ID
    )

    assert isinstance(resource_policy, ResourcePolicy)

    galileo.stations.delete_station(station_id)

def test_crud_station_roles():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )
    station_id = station.stationid
    
    # Create role resource policy
    galileo.stations.update_station_role_resource_policy(
            station_id, ROLE_ID, max_cpu_per_job=1
        )


    create_station_role = galileo.stations.create_station_role(
        station_id,
        "Subscriber",
        "Subscribes to activity in the station, should not be able to do anything in it",
    )

    get_station_role = galileo.stations.get_station_roles(station_id, role_ids=[create_station_role.id])
    updated_station_role = galileo.stations.update_station_role(station_id, create_station_role.id, "Follower")
    delete_response = galileo.stations.delete_station_role(station_id, create_station_role.id)
    delete_station_role = galileo.stations.get_station_roles(station_id, role_ids=[create_station_role.id])

    assert isinstance(create_station_role, StationRole)
    assert create_station_role.name == "Subscriber"
    assert isinstance(get_station_role[0], StationRole)
    assert get_station_role[0].name == "Subscriber"
    assert isinstance(updated_station_role, StationRole)
    assert updated_station_role.name == "Follower"
    assert delete_response['success'] is True
    assert len(delete_station_role) == 0

    galileo.stations.delete_station(station_id)

def test_delete_station_role_resource_policy():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )

    station_id = station.stationid
    # Create role resource policy
    galileo.stations.update_station_role_resource_policy(
            station_id, ROLE_ID, max_cpu_per_job=1
        )


    response = galileo.stations.delete_station_role_resource_policy(station_id, ROLE_ID)
    resource_policy = galileo.stations.get_station_role_resource_policy(
        station_id, ROLE_ID
    )
    assert response["success"] is True
    assert resource_policy is None

    galileo.stations.delete_station(station_id)


def test_update_station_lz_resource_policy():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )

    station_id = station.stationid
    # Create role resource policy
    galileo.stations.update_station_role_resource_policy(
            station_id, ROLE_ID, max_cpu_per_job=1
        )

    user_id = galileo.profiles.self().userid
    lz_id = galileo.lz.list_lz(userids=[user_id])[0].lz_id

    galileo.stations.add_lz_to_station(station_id, [lz_id])


    resource_policy = galileo.stations.update_station_lz_resource_policy(
        station_id, lz_id, max_cpu_per_job=1
    )
    assert resource_policy.max_cpu_per_job == 1
    galileo.stations.delete_station(station_id)


def test_get_station_lz_resource_policy():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )
    station_id = station.stationid
    # Create role resource policy
    user_id = galileo.profiles.self().userid
    lz_id = galileo.lz.list_lz(userids=[user_id])[0].lz_id

    galileo.stations.add_lz_to_station(station_id, [lz_id])

    galileo.stations.update_station_lz_resource_policy(
        station_id, lz_id, max_cpu_per_job=1
    )

    resource_policy = galileo.stations.get_station_lz_resource_policy(
        station_id, lz_id
    )
    resource_limits = galileo.stations.get_station_lz_resource_limits(
        station_id, lz_id
    )

    assert isinstance(resource_policy, ResourcePolicy)
    assert isinstance(resource_limits, ResourcePolicy)
    galileo.stations.delete_station(station_id)



def test_delete_station_lz_resource_policy():
    station = galileo.stations.create_station(
        name="sdk_station_integration_test", userids=[], description="for testing",
    )
    station_id = station.stationid
    user_id = galileo.profiles.self().userid
    lz_id = galileo.lz.list_lz(userids=[user_id])[0].lz_id
    # Create role resource policy

    galileo.stations.add_lz_to_station(station_id, [lz_id])

    galileo.stations.update_station_lz_resource_policy(
        station_id, lz_id, max_cpu_per_job=1
    )

    response = galileo.stations.delete_station_lz_resource_policy(
        station_id, lz_id
    )
    resource_policy = galileo.stations.get_station_lz_resource_policy(
        station_id, lz_id
    )
    assert response["success"] is True
    assert resource_policy is None
    galileo.stations.delete_station(station_id)

