from galileo_sdk.compat import mock
from galileo_sdk.business.objects.lz import (
    ELzStatus,
    Lz,
    UpdateLzRequest,
)
from galileo_sdk.business import LzService

BACKEND = "http://BACKEND"
LZ_ID = "lz_id"
AMOUNT = 10

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
lzs_repo = mock.Mock()
lzs_service = LzService(lzs_repo)


def test_get_lz_by_id():
    x = 1
    lzs_repo.get_lz_by_id.return_value = Lz(
        lz_id=str(x),
        gpu_count=str(x),
        cpu_count=str(x),
        arch=str(x),
        memory=str(x),
        name=str(x),
        operating_system=str(x),
        status=ELzStatus.online,
        userid=str(x),
        container_technology="container_tech",
        job_runner="job runner",
        memory_amount=str(x),
    )

    # Call
    r = lzs_service.get_lz_by_id(LZ_ID)

    # Assert
    assert r.userid == str(x)


def test_list_machines():
    lzs_repo.list_lz.return_value = [
        Lz(
            lz_id=str(x),
            gpu_count=str(x),
            cpu_count=str(x),
            arch=str(x),
            memory=str(x),
            name=str(x),
            operating_system=str(x),
            status=ELzStatus.online,
            userid=str(x),
            container_technology="container_tech",
            job_runner="job runner",
            memory_amount=str(x),
        )
        for x in range(5)
    ]

    # Call
    r = lzs_service.list_lz()

    # Assert
    for i in range(5):
        assert r[i].userid == str(i)


def test_update():
    x = 1
    lzs_repo.update.return_value = Lz(
        lz_id=str(x),
        gpu_count=str(x),
        cpu_count=str(x),
        arch=str(x),
        memory=str(x),
        name=str(x),
        operating_system=str(x),
        status=ELzStatus.online,
        userid=str(x),
        container_technology="container_tech",
        job_runner="job runner",
        memory_amount=str(x),
    )

    # Call
    r = lzs_service.update(UpdateLzRequest(lz_id=LZ_ID))

    # Assert
    assert r.userid == str(x)

def test_delete_lz():
    # Arrange
    lzs_repo.delete_lz.return_value = True

    # Call 
    r = lzs_service.delete_lz_by_id(LZ_ID)

    assert r["success"] is True
