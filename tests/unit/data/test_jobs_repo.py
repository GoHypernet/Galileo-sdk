import os

from galileo_sdk.compat import mock
from galileo_sdk.business.utils.generate_query_str import generate_query_str
from galileo_sdk.data.repositories.jobs import JobsRepository, job_dict_to_job
from galileo_sdk.mock_response import MockResponse

BACKEND = "http://BACKEND"
NAMESPACE = "/galileo/user_interface/v1"
FILENAME = "filename"
LOCATION = os.path.join("", FILENAME)
JOB_ID = "job_id"
DEST_MID = "dest_mid"
STATION_ID = "station_id"
UNIVERSE_ID = "universe_id"
QUERY = generate_query_str({"filename": FILENAME, "path": LOCATION})
TIMESTAMP = 1584946381


# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
settings_repo.get_settings().universe = UNIVERSE_ID 
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
job_repo = JobsRepository(settings_repo, auth_provider, NAMESPACE)


# TODO Missing a bunch of key, value pairs
job = {
    "jobid": "jobid",
    "receiverid": "receiverid",
    "project_id": "project_id",
    "time_created": TIMESTAMP,
    "last_updated": TIMESTAMP,
    "status": "uploaded",
    "cpu_count": 1,
    "gpu_count": 0,
    "memory_amount": 0,    
    "enable_tunnel": False,
    "tunnel_port": 8080,
    "tunnel_url": "https://example.com",
    "name": "name",
    "stationid": "stationid",
    "userid": "userid",
    "state": "state",
    "pay_status": "pay_status",
    "pay_interval": 1,
    "total_runtime": 10000,
    "archived": False,
    "container": "container",
    "oaid": "oaid",
    "status_history": [{"timestamp": TIMESTAMP, "status": "uploaded"}],
}

jobObject = job_dict_to_job(job)


def mocked_requests_get(*args, **kwargs):
    if args[0] == "{backend}{namespace}/job/upload_request".format(
        backend=BACKEND, namespace=NAMESPACE
    ):
        return MockResponse({"location": LOCATION, "filename": FILENAME}, 200)
    elif args[0] == "{backend}{namespace}/jobs/{job_id}/results/location".format(
        backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
    ):
        return MockResponse({"location": LOCATION, "filename": FILENAME}, 200)
    elif args[0] == "{backend}{namespace}/jobs/{job_id}/results".format(
        backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
    ):
        return MockResponse({"files": [{"path": LOCATION, "filename": FILENAME}]}, 200)
    elif args[0] == "{backend}{namespace}/jobs/{job_id}/top".format(
        backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
    ):
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
    elif args[0] == "{backend}{namespace}/jobs/{job_id}/logs".format(
        backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
    ):
        return MockResponse({"logs": "logs"}, 200)
    elif args[0] == "{backend}{namespace}/jobs".format(
        backend=BACKEND, namespace=NAMESPACE
    ):
        return MockResponse({"jobs": [job]}, 200)
    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    if args[0] == "{backend}{namespace}/jobs".format(
        backend=BACKEND, namespace=NAMESPACE
    ):
        return MockResponse({"job": {"jobinfo": "jobinfo"}}, 200)
    return MockResponse(None, 404)


def mocked_requests_put(*args, **kwargs):
    if args[0] == "{backend}{namespace}/jobs/{job_id}/results/download_complete".format(
        backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
    ):
        return MockResponse(True, 200)
    elif args[0] == "{backend}{namespace}/jobs/{job_id}/run".format(
        backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
    ):
        job_copy = job.copy()
        job_copy["status"] = "submit"
        return MockResponse({"job": job_copy}, 200)
    elif args[0] == "{backend}{namespace}/jobs/{job_id}/stop".format(
        backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
    ):
        job_copy = job.copy()
        job_copy["status"] = "stop"
        return MockResponse({"job": job_copy}, 200)
    elif args[0] == "{backend}{namespace}/jobs/{job_id}/pause".format(
        backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
    ):
        job_copy = job.copy()
        job_copy["status"] = "pause"
        return MockResponse({"job": job_copy}, 200)
    elif args[0] == "{backend}{namespace}/jobs/{job_id}/start".format(
        backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
    ):
        job_copy = job.copy()
        job_copy["status"] = "start"
        return MockResponse({"job": job_copy}, 200)
    elif args[0] == "{backend}{namespace}/jobs/{job_id}/kill".format(
        backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
    ):
        job_copy = job.copy()
        job_copy["status"] = "kill"
        return MockResponse({"job": job_copy}, 200)
    return MockResponse(None, 404)


@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_request_send_job(mocked_requests):
    # Call
    r = job_repo.request_send_job()
    r = r.json()

    # Act
    # Universes is being mocked and messing stuff up
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/job/upload_request".format(
            backend=BACKEND, namespace=NAMESPACE
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID,
            },
        json=None,
    )

    # Assert
    assert r == {"location": LOCATION, "filename": FILENAME}


@mock.patch("galileo_sdk.compat.requests.post", side_effect=mocked_requests_post)
def test_request_send_job_completed(mocked_requests):
    # Call
    r = job_repo.request_send_job_completed(DEST_MID, FILENAME, STATION_ID)
    r = r.json()

    # Act
    # Universes is being mocked and messing stuff up

    #TODO Added "universe-id" to headers
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/jobs".format(backend=BACKEND, namespace=NAMESPACE),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID  
            },
        json={
            "destination_mid": DEST_MID,
            "filename": FILENAME,
            "stationid": STATION_ID,
        },
    )

    # Assert
    assert r["job"] == {"jobinfo": "jobinfo"}


#TODO Added "universe-id" to headers
@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_request_receive_job(mocked_requests):
    # Call
    r = job_repo.request_receive_job(JOB_ID)
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/jobs/{job_id}/results/location".format(
            backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN", 
            "universe-id": UNIVERSE_ID
        },
        json=None,
    )

    # Assert
    assert r["location"] == LOCATION
    assert r["filename"] == FILENAME


#TODO Added "universe-id" to headers
@mock.patch("galileo_sdk.compat.requests.put", side_effect=mocked_requests_put)
def test_request_receive_job_completed(mocked_requests):
    # Call
    r = job_repo.request_receive_job_completed(JOB_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/jobs/{job_id}/results/download_complete".format(
            backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID
        },
        json=None,
    )

    # Assert
    assert r.json() == True
    assert r.status_code == 200

#TODO Added "universe-id" to headers
@mock.patch("galileo_sdk.compat.requests.put", side_effect=mocked_requests_put)
def test_submit_job(mocked_requests):
    # Call
    r = job_repo.submit_job(JOB_ID)
    r = r.json()

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/jobs/{job_id}/run".format(
            backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID
            },
        json=None,
    )

    # Assert
    assert r["job"]["status"] == "submit"

#TODO Added "universe-id" to headers
@mock.patch("galileo_sdk.compat.requests.put", side_effect=mocked_requests_put)
def test_request_stop_job(mocked_requests):
    # Call
    r = job_repo.request_stop_job(JOB_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/jobs/{job_id}/stop".format(
            backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID
        },
        json=None,
    )

    # Assert
    assert r.status == "stop"

#TODO Added "universe-id" to headers
@mock.patch("galileo_sdk.compat.requests.put", side_effect=mocked_requests_put)
def test_request_pause_job(mocked_requests):
    # Call
    r = job_repo.request_pause_job(JOB_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/jobs/{job_id}/pause".format(
            backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID
            },
        json=None,
    )

    # Assert
    assert r.status == "pause"

#TODO Added "universe-id" to headers
@mock.patch("galileo_sdk.compat.requests.put", side_effect=mocked_requests_put)
def test_request_start_job(mocked_requests):
    # Call
    r = job_repo.request_start_job(JOB_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/jobs/{job_id}/start".format(
            backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID
        },
        json=None,
    )

    # Assert
    assert r.status == "start"

#TODO Added "universe-id" to headers
@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_request_top_from_job(mocked_requests):
    # Call
    r = job_repo.request_top_from_job(JOB_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/jobs/{job_id}/top".format(
            backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID
        },
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

#TODO Added "universe-id" to headers
@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_request_logs_from_job(mocked_requests):
    # Call
    r = job_repo.request_logs_from_jobs(JOB_ID)

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/jobs/{job_id}/logs".format(
            backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID
            },
        json=None,
    )

    # Assert
    assert r == "logs"

#TODO Added "universe-id" to headers
@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_list_jobs(mocked_requests):
    # Call
    r = job_repo.list_jobs("")

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/jobs".format(backend=BACKEND, namespace=NAMESPACE),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID
        },
        json=None,
    )

    # Assert
    assert r[0].job_id == jobObject.job_id

#TODO Added "universe-id" to headers
@mock.patch("galileo_sdk.compat.requests.put", side_effect=mocked_requests_put)
def test_kill_request(mocked_requests):
    r = job_repo.request_kill_job(JOB_ID)

    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/jobs/{job_id}/kill".format(
            backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID
        },
        json=None,
    )

    assert r.status == "kill"

#TODO Added "universe-id" to headers
@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_get_results_url(mocked_requests):
    r = job_repo.get_results_metadata(JOB_ID)

    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/jobs/{job_id}/results".format(
            backend=BACKEND, namespace=NAMESPACE, job_id=JOB_ID
        ),
        headers={
            "Authorization": "Bearer ACCESS_TOKEN",
            "universe-id": UNIVERSE_ID
        },
        json=None,
    )

    assert len(r) == 1
    assert r[0].filename == FILENAME
    assert r[0].path == LOCATION
