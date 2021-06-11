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
UNIVERSE_ID = "universe_id"
HEADERS = {"Authorization": "Bearer ACCESS_TOKEN", "universe-id": UNIVERSE_ID}
# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
settings_repo.get_settings().universe = UNIVERSE_ID
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
lz_repo = LzRepository(settings_repo, auth_provider, NAMESPACE)



def mocked_requests_get(*args, **kwargs):
    if args[0] == "{backend}{namespace}/machines/{mid}".format(
        backend=BACKEND, namespace=NAMESPACE, mid=LZ_ID
    ):
        x = 1
        return MockResponse(
            {
                "mid": str(x),
                "gpu": str(x),
                "cpu": str(x),
                "gpu_count": x,
                "cpu_count": x,
                "arch": str(x),
                "memory": str(x),
                "memory_amount": x,
                "job_runner": str(x),
                "container_technology": str(x),
                "name": str(x),
                "operating_system": str(x),
                "running_jobs_limit": x,
                "status": "online",
                "userid": str(x),
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
                        "gpu_count": x,
                        "cpu_count": x,
                        "arch": str(x),
                        "memory": str(x),
                        "memory_amount": x,
                        "job_runner": str(x),
                        "container_technology": str(x),
                        "name": str(x),
                        "operating_system": str(x),
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
                "machine": {
                    "mid": str(x),
                    "gpu": str(x),
                    "cpu": str(x),
                    "gpu_count": str(x),
                    "cpu_count": str(x),
                    "arch": str(x),
                    "memory": str(x),
                    "memory_amount": str(x),
                    "job_runner": str(x),
                    "container_technology": str(x),
                    "name": str(x),
                    "operating_system": str(x),
                    "running_jobs_limit": x,
                    "status": "online",
                    "userid": str(x),
                }
            },
            200,
        )

    return MockResponse(None, 404)

def mocked_requests_delete(*args, **kwargs):
    if args[0] == "{backend}{namespace}/machines/{lz_id}".format(
        backend=BACKEND, namespace=NAMESPACE, lz_id=LZ_ID
    ):
        return MockResponse(
            {
            "success" : True
        }, 200)
    return MockResponse(None, 404)

@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_get_lz_by_id(mocked_requests):
    # Call
    r = lz_repo.get_lz_by_id(LZ_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/machines/{mid}".format(
            backend=BACKEND, namespace=NAMESPACE, mid=LZ_ID
        ),
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r.name == "1"


@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_list_lzs(mocked_requests):
    # Call
    r = lz_repo.list_lz("")

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/machines".format(backend=BACKEND, namespace=NAMESPACE),
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert len(r) == 5
    for i in range(5):
        assert r[i].userid == str(i)
        assert r[i].status == ELzStatus.online

@mock.patch("galileo_sdk.compat.requests.delete", side_effect=mocked_requests_delete)
def test_delete_lz(mocked_requests):
    # Call
    r = lz_repo.delete_lz_by_id(LZ_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/machines/{lz_id}".format(backend=BACKEND, namespace=NAMESPACE, lz_id=LZ_ID),
        headers=HEADERS,
        json=None,
    )

    # Assert
    assert r["success"] is True
# @mock.patch("galileo_sdk.compat.requests.put", side_effect=mocked_requests_put)
# def test_update_max_concurrent_jobs(mocked_requests):
    # # Call
    # r = lz_repo.update(UpdateLzRequest(LZ_ID))

    # # Act
    # mocked_requests.assert_called_once_with(
        # "{backend}{namespace}/machines/{mid}".format(
            # backend=BACKEND, namespace=NAMESPACE, mid=LZ_ID
        # ),
        # headers=HEADERS,
        # json={"amount": AMOUNT},
    # )

    # # Assert
    # assert isinstance(r, Lz)
    # assert r == True
