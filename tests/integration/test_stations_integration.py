from src import GalileoSdk
import os

# Must set env variables before running tests
USERNAME = os.getenv("GALILEO_USER")
PASSWORD = os.getenv("GALILEO_PASSWORD")
CONFIG = "local"

galileo = GalileoSdk(username=USERNAME, password=PASSWORD, config=CONFIG,)


def test_list_stations():
    station_list = galileo.stations.list_stations()
    assert station_list != None


def test_create_and_delete_station():
    station_details = galileo.stations.create_station(
        name="sdk_station", userids=[], description="for testing",
    )

    station_list = galileo.stations.list_stations()
    sdk_station_id = ""
    for station in station_list["stations"]:
        if station["name"] == "sdk_station":
            sdk_station_id = station["stationid"]

    r_delete_station = galileo.stations.delete_station(sdk_station_id)

    assert "sdk_station" == station_details["station"]["name"]
    assert not sdk_station_id == ""
    assert r_delete_station == True


def test_add_and_remove_volumes_to_station():
    galileo.stations.create_station(
        name="sdk_station", userids=[], description="for testing",
    )

    station_list = galileo.stations.list_stations()
    station_id = ""
    for station in station_list["stations"]:
        if station["name"] == "sdk_station":
            station_id = station["stationid"]

    volumes = galileo.stations.add_volumes_to_station(
        station_id=station_id, name="volume", mount_point="mount_point", access="rw"
    )
    r_remove_volume = galileo.stations.remove_volume_from_station(
        station_id=station_id, volume_id=volumes["volumes"]["volumeid"]
    )

    galileo.stations.delete_station(station_id)

    print(volumes)
    assert "rw" == volumes["volumes"]["access"]
    assert "mount_point" == volumes["volumes"]["mount_point"]
    assert r_remove_volume == True


def test_add_and_delete_host_path_to_volume():
    galileo.stations.create_station(
        name="sdk_station", userids=[], description="for testing",
    )

    self = galileo.profiles.self()

    station_list = galileo.stations.list_stations()
    station_id = ""
    for station in station_list["stations"]:
        if station["name"] == "sdk_station":
            station_id = station["stationid"]

    volumes = galileo.stations.add_volumes_to_station(
        station_id=station_id, name="volume", mount_point="mount_point", access="rw"
    )

    host_path = galileo.stations.add_host_path_to_volume(
        station_id=station_id,
        volume_id=volumes["volumes"]["volumeid"],
        mid="mid-1",
        host_path="host_path",
    )
    print(host_path)

    deleted_host_path = galileo.stations.delete_host_path_from_volume(
        station_id=station_id,
        volume_id=volumes["volumes"]["volumeid"],
        host_path_id=host_path["volume"]["host_paths"][0]["volumehostpathid"],
    )

    galileo.stations.delete_station(station_id)

    print(deleted_host_path)

    assert [] == volumes["volumes"]["host_paths"]
    assert "host_path" == host_path["volume"]["host_paths"][0]["host_path"]
    assert deleted_host_path == True
