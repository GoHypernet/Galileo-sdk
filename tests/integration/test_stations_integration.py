from galileo_sdk import GalileoSdk, ResourcePolicy, StationRole

# Must set env variables before running tests

CONFIG = "development"
STATION_ID = "86a32c0b-bad0-456b-b41a-cb2bef9cdafb"
LZ_ID = "Jaguar2121"
ROLE_ID = "b67bb82c-f939-4c22-a341-9904675b7c92"
galileo = GalileoSdk(config=CONFIG)
user = galileo.profiles.self()


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
    assert r_delete_station is True


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
    assert r_remove_volume is True
    assert r_delete_station is True


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
    assert deleted_host_path is True


def test_create_station_resource_policy():
    policy = galileo.stations.update_station_resource_policy(STATION_ID)

    assert isinstance(policy, ResourcePolicy)


def test_get_station_resource_policy():
    policy = galileo.stations.get_station_resource_policy(STATION_ID)

    assert isinstance(policy, ResourcePolicy)


def test_delete_station_resource_policy():
    response = galileo.stations.delete_station_resource_policy(STATION_ID)

    assert response is True


def test_self_resource_limits():
    policy, machine_id = galileo.stations.get_self_station_resource_limits(STATION_ID)
    assert isinstance(policy, ResourcePolicy)


def test_create_station_user_resource_policy():
    policy = galileo.stations.update_station_user_resource_policy(STATION_ID, user.userid, max_cpu_per_job=10000)
    assert isinstance(policy, ResourcePolicy)


def test_get_station_user_resource_policy():
    policy = galileo.stations.get_station_user_resource_policy(STATION_ID, user.userid)
    assert isinstance(policy, ResourcePolicy)


def test_delete_station_user_resource_policy():
    response = galileo.stations.delete_station_user_resource_policy(STATION_ID, user.userid)
    policy = galileo.stations.get_station_user_resource_policy(STATION_ID, user.userid)
    assert response is True
    assert policy is None


def test_update_station_role_resource_policy():
    resource_policy = galileo.stations.update_station_role_resource_policy(
        STATION_ID, ROLE_ID, max_cpu_per_job=1
    )
    assert resource_policy.max_cpu_per_job == 1


def test_get_station_role_resource_policy():
    resource_policy = galileo.stations.get_station_role_resource_policy(
        STATION_ID, ROLE_ID
    )

    assert isinstance(resource_policy, ResourcePolicy)


def test_crud_station_roles():
    create_station_role = galileo.stations.create_station_role(
        STATION_ID,
        "Subscriber",
        "Subscribes to activity in the station, should not be able to do anything in it",
    )

    get_station_role = galileo.stations.get_station_roles(STATION_ID, role_ids=[create_station_role.id])
    updated_station_role = galileo.stations.update_station_role(STATION_ID, create_station_role.id, "Follower")
    delete_response = galileo.stations.delete_station_role(STATION_ID, create_station_role.id)
    delete_station_role = galileo.stations.get_station_roles(STATION_ID, role_ids=[create_station_role.id])

    assert isinstance(create_station_role, StationRole)
    assert create_station_role.name == "Subscriber"
    assert isinstance(get_station_role[0], StationRole)
    assert get_station_role[0].name == "Subscriber"
    assert isinstance(updated_station_role, StationRole)
    assert updated_station_role.name == "Follower"
    assert delete_response is True
    assert len(delete_station_role) == 0


def test_delete_station_role_resource_policy():
    response = galileo.stations.delete_station_role_resource_policy(STATION_ID, ROLE_ID)
    resource_policy = galileo.stations.get_station_role_resource_policy(
        STATION_ID, ROLE_ID
    )
    assert response is True
    assert resource_policy is None


def test_update_station_machine_resource_policy():
    resource_policy = galileo.stations.update_station_machine_resource_policy(
        STATION_ID, LZ_ID, max_cpu_per_job=1
    )
    assert resource_policy.max_cpu_per_job == 1


def test_get_station_machine_resource_policy():
    resource_policy = galileo.stations.get_station_machine_resource_policy(
        STATION_ID, LZ_ID
    )
    resource_limits = galileo.stations.get_station_machine_resource_limits(
        STATION_ID, LZ_ID
    )

    assert isinstance(resource_policy, ResourcePolicy)
    assert isinstance(resource_limits, ResourcePolicy)


def test_delete_station_machine_resource_policy():
    response = galileo.stations.delete_station_machine_resource_policy(
        STATION_ID, LZ_ID
    )
    resource_policy = galileo.stations.get_station_machine_resource_policy(
        STATION_ID, LZ_ID
    )
    assert response is True
    assert resource_policy is None
