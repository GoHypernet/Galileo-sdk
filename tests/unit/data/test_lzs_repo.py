from galileo_sdk.compat import mock
from galileo_sdk.business.objects.lz import (
    ELzStatus,
    Lz,
    UpdateLzRequest,
)
from galileo_sdk.data.repositories.lz import LzRepository
from galileo_sdk.mock_response import MockResponse

BACKEND = "http://BACKEND"
NAMESPACE = "/galileo/user_interface/v1"
LZ_ID = "lzs_id"
AMOUNT = 10

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
machines_repo = LzRepository(settings_repo, auth_provider, NAMESPACE)


def mocked_requests_get(*args, **kwargs):
    if args[0] == "{backend}{namespace}/machines/{mid}".format(
        backend=BACKEND, namespace=NAMESPACE, mid=LZ_ID
    ):
        x = 1
        return MockResponse(
            {
                "machine": {
                    "mid": str(x),
                    "gpu": str(x),
                    "cpu": str(x),
                    "arch": str(x),
                    "memory": str(x),
                    "name": str(x),
                    "os": str(x),
                    "running_jobs_limit": x,
                    "status": "online",
                    "userid": str(x),
                }
            },
            200,
        )
    elif args[0] == "{backend}{namespace}/machines".format(
        backend=BACKEND, namespace=NAMESPACE
    ):
        return MockResponse(
            {
                "machines": [
                    {
                        "mid": str(x),
                        "gpu": str(x),
                        "cpu": str(x),
                        "arch": str(x),
                        "memory": str(x),
                        "name": str(x),
                        "os": str(x),
                        "running_jobs_limit": x,
                        "status": "online",
                        "userid": str(x),
                    }
                    for x in range(5)
                ]
            },
            200,
        )
    return MockResponse(None, 404)


def mocked_requests_put(*args, **kwargs):
    if args[0] == "{backend}{namespace}/machines/{mid}".format(
        backend=BACKEND, namespace=NAMESPACE, mid=LZ_ID
    ):
        x = 1
        return MockResponse(
            {
                "machines": {
                    "mid": str(x),
                    "gpu": str(x),
                    "cpu": str(x),
                    "arch": str(x),
                    "memory": str(x),
                    "name": str(x),
                    "os": str(x),
                    "running_jobs_limit": x,
                    "status": "online",
                    "userid": str(x),
                }
            },
            200,
        )

    return MockResponse(None, 404)


@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def get_machine_by_id(mocked_requests):
    # Call
    r = machines_repo.get_machine_by_id(LZ_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/machines/{mid}".format(
            backend=BACKEND, namespace=NAMESPACE, mid=LZ_ID
        ),
        headers={"Authorization": "Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r["machine_info"] == "machine_info"


@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def list_machines(mocked_requests):
    # Call
    r = machines_repo.list_machines("")

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/machines".format(backend=BACKEND, namespace=NAMESPACE),
        headers={"Authorization": "Bearer ACCESS_TOKEN"},
        json={"page": None, "items": None, "mids": None, "userids": None},
    )

    # Assert
    assert len(r) == 5
    for i in range(5):
        assert r[i].userid == i
        assert r[i].status == ELzStatus.online


@mock.patch("galileo_sdk.compat.requests.put", side_effect=mocked_requests_put)
def update_max_concurrent_jobs(mocked_requests):
    # Call
    r = machines_repo.update(UpdateLzRequest(LZ_ID))

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/machines/{mid}".format(
            backend=BACKEND, namespace=NAMESPACE, mid=LZ_ID
        ),
        headers={"Authorization": "Bearer ACCESS_TOKEN"},
        json={"amount": AMOUNT},
    )

    # Assert
    assert isinstance(r, Lz)
    assert r == True
