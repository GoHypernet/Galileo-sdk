from unittest import mock

from galileo_sdk.data.repositories.jobs import JobsRepository
from galileo_sdk.mock_response import MockResponse
from galileo_sdk.business.objects import (
    Job,
    EJobStatus,
    EPaymentStatus,
    EJobRunningStatus,
    JobStatus,
)

from galileo_sdk.data.repositories.jobs import job_dict_to_job
from datetime import datetime

BACKEND = "http://BACKEND"
NAMESPACE = "/galileo/user_interface/v1"
RETURN_URL = "GOOGLE"
FILENAME = "filename"
JOB_ID = "job_id"
DEST_MID = "dest_mid"
STATION_ID = "station_id"

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = f"{BACKEND}"
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
job_repo = JobsRepository(settings_repo, auth_provider)

job = {
    "jobid": "jobid",
    "receiverid": "receiverid",
    "project_id": "project_id",
    "time_created": int(datetime.now().timestamp()),
    "last_updated": int(datetime.now().timestamp()),
    "status": "uploaded",
    "container": "container",
    "name": "name",
    "stationid": "stationid",
    "userid": "userid",
    "state": "state",
    "oaid": "oaid",
    "pay_status": "pay_status",
    "pay_interval": 1,
    "total_runtime": 10000,
    "archived": False,
    "status_history": [{"time": int(datetime.now().timestamp()), "status": "uploaded"}],
}

jobObject = job_dict_to_job(job)


def mocked_requests_get(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/job/upload_request":
        return MockResponse({"location": RETURN_URL, "filename": FILENAME}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/results/location":
        return MockResponse({"location": RETURN_URL, "filename": FILENAME}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/top":
        return MockResponse(True, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/logs":
        return MockResponse(True, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs":
        return MockResponse({"jobs": [job]}, 200)
    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/jobs":
        return MockResponse({"job": {"jobinfo": "jobinfo"}}, 200)
    return MockResponse(None, 404)


def mocked_requests_put(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/results/download_complete":
        return MockResponse(True, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/run":
        return MockResponse({"job": {"status": "submit"}}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/stop":
        return MockResponse({"job": {"status": "stop"}}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/pause":
        return MockResponse({"job": {"status": "pause"}}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/start":
        return MockResponse({"job": {"status": "start"}}, 200)
    return MockResponse(None, 404)


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_request_send_job(mocked_requests):
    # Call
    r = job_repo.request_send_job()
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/job/upload_request",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r == {"location": RETURN_URL, "filename": FILENAME}


@mock.patch("requests.post", side_effect=mocked_requests_post)
def test_request_send_job_completed(mocked_requests):
    # Call
    r = job_repo.request_send_job_completed(DEST_MID, FILENAME, STATION_ID)
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json={
            "destination_mid": DEST_MID,
            "filename": FILENAME,
            "stationid": STATION_ID,
        },
    )

    # Assert
    assert r["job"] == {"jobinfo": "jobinfo"}


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_request_receive_job(mocked_requests):
    # Call
    r = job_repo.request_receive_job(JOB_ID)
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/results/location",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r["location"] == RETURN_URL
    assert r["filename"] == FILENAME


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_request_receive_job_completed(mocked_requests):
    # Call
    r = job_repo.request_receive_job_completed(JOB_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/results/download_complete",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r.json() == True
    assert r.status_code == 200


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_submit_job(mocked_requests):
    # Call
    r = job_repo.submit_job(JOB_ID)
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/run",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r["job"] == {"status": "submit"}


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_request_stop_job(mocked_requests):
    # Call
    r = job_repo.request_stop_job(JOB_ID)
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/stop",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r["job"] == {"status": "stop"}


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_request_pause_job(mocked_requests):
    # Call
    r = job_repo.request_pause_job(JOB_ID)
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/pause",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r["job"] == {"status": "pause"}


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_request_start_job(mocked_requests):
    # Call
    r = job_repo.request_start_job(JOB_ID)
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/start",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r["job"] == {"status": "start"}


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_request_top_from_job(mocked_requests):
    # Call
    r = job_repo.request_top_from_job(JOB_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/top",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r.json() == True
    assert r.status_code == 200


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_request_logs_from_job(mocked_requests):
    # Call
    r = job_repo.request_logs_from_jobs(JOB_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/logs",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r.json() == True
    assert r.status_code == 200


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_list_jobs(mocked_requests):
    # Call
    r = job_repo.list_jobs("")

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r[0].jobid == jobObject.jobid
