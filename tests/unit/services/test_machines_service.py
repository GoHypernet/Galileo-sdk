from unittest import mock

from src.business.services.machines import MachinesService
from src.mock_response import MockResponse

BACKEND = "http://BACKEND"
MID = "machine_id"
AMOUNT = 10

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = f"{BACKEND}"
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
machines_repo = mock.Mock()
machines_service = MachinesService(machines_repo)


def test_get_machine_by_id():
    machines_repo.get_machine_by_id.return_value = MockResponse(
        {"machine_info": "machine_info"}, 200
    )

    # Call
    r = machines_service.get_machine_by_id(MID)

    # Assert
    assert r["machine_info"] == "machine_info"


def test_list_machines():
    machines_repo.list_machines.return_value = MockResponse(
        {"machines": [{"machine": i} for i in range(10)]}, 200
    )

    # Call
    r = machines_service.list_machines()

    # Assert
    assert len(r["machines"]) == 10
    assert r["machines"][5] == {"machine": 5}


def test_update_max_concurrent_jobs():
    machines_repo.update_max_concurrent_jobs.return_value = MockResponse(True, 200)

    # Call
    r = machines_service.update_max_concurrent_jobs(MID, AMOUNT)

    # Assert
    assert isinstance(r, bool)
    assert r == True
