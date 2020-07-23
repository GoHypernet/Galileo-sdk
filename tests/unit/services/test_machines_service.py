from galileo_sdk.compat import mock
from galileo_sdk.business.objects.machines import (EMachineStatus, Machine,
                                                   UpdateMachineRequest)
from galileo_sdk.business.services.machines import MachinesService

BACKEND = "http://BACKEND"
MID = "machine_id"
AMOUNT = 10

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
machines_repo = mock.Mock()
machines_service = MachinesService(machines_repo)


def test_get_machine_by_id():
    x = 1
    machines_repo.get_machine_by_id.return_value = Machine(
        mid=str(x),
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
        memory_amount=str(x)
    )

    # Call
    r = machines_service.get_machine_by_id(MID)

    # Assert
    assert r.userid == str(x)


def test_list_machines():
    machines_repo.list_machines.return_value = [
        Machine(
            mid=str(x),
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
            memory_amount=str(x)
        )
        for x in range(5)
    ]

    # Call
    r = machines_service.list_machines()

    # Assert
    for i in range(5):
        assert r[i].userid == str(i)


def test_update():
    x = 1
    machines_repo.update.return_value = Machine(
        mid=str(x),
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
        memory_amount=str(x)
    )

    # Call
    r = machines_service.update(UpdateMachineRequest(mid=MID))

    # Assert
    assert r.userid == str(x)
