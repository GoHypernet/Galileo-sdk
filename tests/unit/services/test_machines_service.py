from galileo_sdk.compat import mock
from galileo_sdk.business.objects.lz import (
    EMachineStatus,
    Lz,
    UpdateMachineRequest,
)
from galileo_sdk.business import LzService

BACKEND = "http://BACKEND"
MID = "machine_id"
AMOUNT = 10

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
machines_repo = mock.Mock()
machines_service = LzService(machines_repo)


def test_get_machine_by_id():
    x = 1
    machines_repo.get_lz_by_id.return_value = Lz(
        lz_id=str(x),
        gpu_count=str(x),
        cpu_count=str(x),
        arch=str(x),
        memory=str(x),
        name=str(x),
        operating_system=str(x),
        status=EMachineStatus.online,
        userid=str(x),
        container_technology="container_tech",
        job_runner="job runner",
        memory_amount=str(x),
    )

    # Call
    r = machines_service.get_lz_by_id(MID)

    # Assert
    assert r.userid == str(x)


def test_list_machines():
    machines_repo.list_lz.return_value = [
        Lz(
            lz_id=str(x),
            gpu_count=str(x),
            cpu_count=str(x),
            arch=str(x),
            memory=str(x),
            name=str(x),
            operating_system=str(x),
            status=EMachineStatus.online,
            userid=str(x),
            container_technology="container_tech",
            job_runner="job runner",
            memory_amount=str(x),
        )
        for x in range(5)
    ]

    # Call
    r = machines_service.list_lz()

    # Assert
    for i in range(5):
        assert r[i].userid == str(i)


def test_update():
    x = 1
    machines_repo.update.return_value = Lz(
        lz_id=str(x),
        gpu_count=str(x),
        cpu_count=str(x),
        arch=str(x),
        memory=str(x),
        name=str(x),
        operating_system=str(x),
        status=EMachineStatus.online,
        userid=str(x),
        container_technology="container_tech",
        job_runner="job runner",
        memory_amount=str(x),
    )

    # Call
    r = machines_service.update(UpdateMachineRequest(mid=MID))

    # Assert
    assert r.userid == str(x)
