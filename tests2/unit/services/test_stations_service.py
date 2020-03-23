import mock
from galileo_sdk.business.objects.stations import (EStationUserRole,
                                                   EVolumeAccess, Station,
                                                   StationUser, Volume)
from galileo_sdk.business.services.stations import StationsService

BACKEND = "http://BACKEND"
STATION_ID = "STATION_ID"
USER_ID = "USER_ID"
VOLUMES_ID = "VOLUMES_ID"
HOST_PATH = "HOST_PATH"
HEADERS = {"Authorization": "Bearer ACCESS_TOKEN"}
NAME = "STATION_NAME"
USERNAMES = ["USERNAME1", "USERNAME2"]
DESCRIPTION = "description"
MIDS = ["mid1", "mid2"]
MOUNT_POINT = "MOUNT_POINT"
ACCESS = "rw"

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
stations_repo = mock.Mock()
stations_service = StationsService(stations_repo)


def test_list_stations():
    stations_repo.list_stations.return_value = [
        Station(
            "stationid",
            "name",
            "description",
            [StationUser("stationuserid", "userid", EStationUserRole.ADMIN)],
            ["machine_ids"],
            ["volume_ids"],
        )
        for _ in range(5)
    ]

    # Call
    r = stations_service.list_stations()

    # Assert
    assert len(r) == 5
    assert r[0].stationid == "stationid"
    assert r[0].users[0].status == EStationUserRole.ADMIN


def test_create_station():
    stations_repo.create_station.return_value = Station(
        "stationid",
        "name",
        "description",
        [StationUser("stationuserid", "userid", EStationUserRole.ADMIN)],
        ["machine_ids"],
        ["volume_ids"],
    )

    # Call
    r = stations_service.create_station(NAME, DESCRIPTION, USERNAMES)

    # Assert
    assert r.stationid == "stationid"
    assert r.users[0].status == EStationUserRole.ADMIN


def test_invite_to_station():
    stations_repo.invite_to_station.return_value = True

    # Call
    r = stations_service.invite_to_station(STATION_ID, USERNAMES)

    # Assert
    print(r)
    assert r is True


def test_accept_station_invite():
    stations_repo.accept_station_invite.return_value = True

    # Call
    r = stations_service.accept_station_invite(STATION_ID)

    # Assert
    assert r is True


def test_reject_station_invite():
    stations_repo.reject_station_invite.return_value = True

    # Call
    r = stations_service.reject_station_invite(STATION_ID)

    # Assert
    assert r is True


def test_request_to_join():
    stations_repo.request_to_join.return_value = True

    # Call
    r = stations_service.request_to_join(STATION_ID)

    # Assert
    assert r is True


def test_approve_request_to_join():
    stations_repo.approve_request_to_join.return_value = True

    # Call
    r = stations_service.approve_request_to_join(STATION_ID, USERNAMES)

    # Assert
    assert r is True


def test_reject_request_to_join():
    stations_repo.reject_request_to_join.return_value = True

    # Call
    r = stations_service.reject_request_to_join(STATION_ID, USERNAMES)

    # Assert
    assert r is True


def test_leave_station():
    stations_repo.leave_station.return_value = True

    # Call
    r = stations_service.leave_station(STATION_ID)

    # Assert
    assert r is True


def test_remove_member_from_station():
    stations_repo.remove_member_from_station.return_value = True

    # Call
    r = stations_service.remove_member_from_station(STATION_ID, USER_ID)

    # Assert
    assert r is True


def test_delete_station():
    stations_repo.delete_station.return_value = True

    # Call
    r = stations_service.delete_station(STATION_ID)

    # Assert
    assert r is True


def test_add_machines_to_station():
    stations_repo.add_machines_to_station.return_value = True

    # Call
    r = stations_service.add_machines_to_station(STATION_ID, MIDS)

    # Assert
    assert r is True


def test_remove_machines_to_station():
    stations_repo.remove_machines_from_station.return_value = True

    # Call
    r = stations_service.remove_machines_from_station(STATION_ID, MIDS)

    # Assert
    assert r is True


def test_add_volumes_to_station():
    stations_repo.add_volumes_to_station.return_value = Volume(
        STATION_ID, "name", "mount_point", EVolumeAccess.READWRITE, [], "volumeid",
    )

    # Call
    r = stations_service.add_volumes_to_station(STATION_ID, NAME, MOUNT_POINT, ACCESS)

    # Assert
    assert r.name == "name"
    assert r.stationid == STATION_ID


def test_add_host_path_to_volume():
    stations_repo.add_host_path_to_volume.return_value = Volume(
        STATION_ID, "name", "mount_point", EVolumeAccess.READWRITE, [], "volumeid",
    )

    # Call
    r = stations_service.add_host_path_to_volume(
        STATION_ID, VOLUMES_ID, MIDS[0], HOST_PATH
    )

    # Assert
    assert r.name == "name"
    assert r.stationid == STATION_ID


def test_remove_path_from_volume():
    stations_repo.delete_host_path_from_volume.return_value = True

    # Call
    r = stations_service.delete_host_path_from_volume(STATION_ID, VOLUMES_ID, HOST_PATH)

    # Assert
    assert r is True


def test_remove_volume_from_station():
    stations_repo.remove_volume_from_station.return_value = True

    # Call
    r = stations_service.remove_volume_from_station(STATION_ID, VOLUMES_ID)

    # Assert
    assert r is True
