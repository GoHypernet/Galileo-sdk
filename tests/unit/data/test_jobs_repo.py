import os
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
from galileo_sdk.business.utils.generate_query_str import generate_query_str

BACKEND = "http://BACKEND"
NAMESPACE = "/galileo/user_interface/v1"
FILENAME = "filename"
LOCATION = os.path.join("", FILENAME)
JOB_ID = "job_id"
DEST_MID = "dest_mid"
STATION_ID = "station_id"
QUERY = generate_query_str({"filename": FILENAME, "path": LOCATION})

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
    "status_history": [
        {"timestamp": int(datetime.now().timestamp()), "status": "uploaded"}
    ],
}

jobObject = job_dict_to_job(job)


def mocked_requests_get(*args, **kwargs):
    if args[0] == f"{BACKEND}{NAMESPACE}/job/upload_request":
        return MockResponse({"location": LOCATION, "filename": FILENAME}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/results/location":
        return MockResponse({"location": LOCATION, "filename": FILENAME}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/results":
        return MockResponse({"files": [{"path": LOCATION, "filename": FILENAME}]}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/top":
        return MockResponse(
            {
                "top": {
                    "Processes": [
                        ["process11", "process12"],
                        ["process21", "process22"],
                    ],
                    "Titles": ["title1", "title2"],
                }
            },
            200,
        )
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/logs":
        return MockResponse({"logs": "logs"}, 200)
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
        job_copy = job.copy()
        job_copy["status"] = "submit"
        return MockResponse({"job": job_copy}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/stop":
        job_copy = job.copy()
        job_copy["status"] = "stop"
        return MockResponse({"job": job_copy}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/pause":
        job_copy = job.copy()
        job_copy["status"] = "pause"
        return MockResponse({"job": job_copy}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/start":
        job_copy = job.copy()
        job_copy["status"] = "start"
        return MockResponse({"job": job_copy}, 200)
    elif args[0] == f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/kill":
        job_copy = job.copy()
        job_copy["status"] = "kill"
        return MockResponse({"job": job_copy}, 200)
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
    assert r == {"location": LOCATION, "filename": FILENAME}


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
    assert r["location"] == LOCATION
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
    assert r["job"]["status"] == "submit"


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_request_stop_job(mocked_requests):
    # Call
    r = job_repo.request_stop_job(JOB_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/stop",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r.status == "stop"


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_request_pause_job(mocked_requests):
    # Call
    r = job_repo.request_pause_job(JOB_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/pause",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r.status == "pause"


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_request_start_job(mocked_requests):
    # Call
    r = job_repo.request_start_job(JOB_ID)

    # Act
    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/start",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    # Assert
    assert r.status == "start"


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

    print(r)
    # Assert
    assert len(r) == 2
    assert r[0].items[0].title == "title1"
    assert r[0].items[0].detail == "process11"
    assert r[0].items[1].title == "title2"
    assert r[0].items[1].detail == "process12"
    assert r[1].items[0].title == "title1"
    assert r[1].items[0].detail == "process21"
    assert r[1].items[1].title == "title2"
    assert r[1].items[1].detail == "process22"


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
    assert r == "logs"


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
    assert r[0].job_id == jobObject.job_id


@mock.patch("requests.put", side_effect=mocked_requests_put)
def test_kill_request(mocked_requests):
    r = job_repo.request_kill_job(JOB_ID)

    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/kill",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    assert r.status == "kill"


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_get_results_url(mocked_requests):
    r = job_repo.get_results_url(JOB_ID)

    mocked_requests.assert_called_once_with(
        f"{BACKEND}{NAMESPACE}/jobs/{JOB_ID}/results",
        headers={"Authorization": f"Bearer ACCESS_TOKEN"},
        json=None,
    )

    assert len(r) == 1
    assert r[0].filename == FILENAME
    assert r[0].path == LOCATION
