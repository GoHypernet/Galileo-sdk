from galileo_sdk import GalileoSdk
from galileo_sdk.business.objects.stations import EVolumeAccess

# Must set env variables before running tests

CONFIG = "development"

galileo = GalileoSdk(config=CONFIG)


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
        mid=self.mids[0],
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


galileo.disconnect()
