from unittest import mock

from src.data.repositories.machines import MachinesRepository
from src.mock_response import MockResponse

BACKEND = "http://BACKEND"
NAMESPACE = "/galileo/user_interface/v1"
MID = "machines_id"
AMOUNT = 10

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = f"{BACKEND}"
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
machines_repo = MachinesRepository(settings_repo, auth_provider)


def mocked_requests_get(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/machines/{MID}":
        return MockResponse({"machine_info": "machine_info"}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/machines":
        return MockResponse({"machines": [{"machine": i} for i in range(10)]}, 200)
    return MockResponse(None, 404)


def mocked_requests_put(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/machines/{MID}/update_max":
        return MockResponse(True, 200)

    return MockResponse(None, 404)


@mock.patch("requests.get", side_effect=mocked_requests_get)
def get_machine_by_id(mocked_requests):
    # Call
    r = machines_repo.get_machine_by_id(MID)
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/machines/{MID}",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r["machine_info"] == "machine_info"


@mock.patch("requests.get", side_effect=mocked_requests_get)
def list_machines(mocked_requests):
    # Call
    r = machines_repo.list_machines("")

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/machines",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json={"page": None, "items": None, "mids": None, "userids": None},
    )

    # Assert
    assert len(r["machines"]) == 10
    assert r["machines"][9] == {"machine": 9}


@mock.patch("requests.put", side_effect=mocked_requests_put)
def update_max_concurrent_jobs(mocked_requests):
    # Call
    r = machines_repo.update_max_concurrent_jobs(MID, AMOUNT)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/machines/{MID}/update_max",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json={"amount": AMOUNT},
    )

    # Assert
    assert isinstance(r, bool)
    assert r == True
