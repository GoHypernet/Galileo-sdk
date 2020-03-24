from galileo_sdk.compat import mock
from galileo_sdk.business.services.jobs import JobsService
from galileo_sdk.mock_response import MockResponse

BACKEND = "http://BACKEND"
JOB_ID = "job_id"
DEST_MID = "mid"
FILENAME = "filename"
STATION_ID = "station_id"

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
jobs_repo = mock.Mock()
jobs_service = JobsService(jobs_repo)


def test_request_send_job():
    jobs_repo.request_send_job.return_value = MockResponse(
        {"location": "location", "filename": "filename"}, 200
    )

    # Call
    r = jobs_service.request_send_job()

    # Assert
    assert r == {"location": "location", "filename": "filename"}


def test_request_job_completed():
    jobs_repo.request_send_job_completed.return_value = MockResponse(
        {"job": {"job_info": "job_info"}}, 200
    )

    # Call
    r = jobs_service.request_send_job_completed(DEST_MID, FILENAME, STATION_ID)

    # Assert
    assert r["job"] == {"job_info": "job_info"}


def test_request_receive_job():
    jobs_repo.request_receive_job.return_value = MockResponse(
        {"location": "location", "filename": "filename"}, 200
    )

    # Call
    r = jobs_service.request_receive_job(JOB_ID)

    # Assert
    assert r == {"location": "location", "filename": "filename"}


def test_request_receive_job_completed():
    jobs_repo.request_receive_job_completed.return_value = MockResponse(True, 200)

    # Call
    r = jobs_service.request_receive_job_completed(JOB_ID)

    # Assert
    assert r == True
    assert isinstance(r, bool)


def test_submit_job():
    jobs_repo.submit_job.return_value = MockResponse({"job": {"status": "submit"}}, 200)

    # Call
    r = jobs_service.submit_job(JOB_ID)

    # Assert
    assert r["job"] == {"status": "submit"}


def request_stop_job():
    jobs_repo.stop_job.return_value = MockResponse({"job": {"status": "stop"}}, 200)

    # Call
    r = jobs_service.request_stop_job(JOB_ID)

    # Assert
    assert r["job"] == {"status": "stop"}


def request_pause_job():
    jobs_repo.pause_job.return_value = MockResponse({"job": {"status": "pause"}}, 200)

    # Call
    r = jobs_service.request_pause_job(JOB_ID)

    # Assert
    assert r["job"] == {"status": "pause"}


def request_top_from_job():
    jobs_repo.request_top_from_job.return_value = MockResponse(True, 200)

    # Call
    r = jobs_service.request_top_from_job(JOB_ID)

    # Assert
    assert r == True
    assert isinstance(r, bool)


def request_logs_from_job():
    jobs_repo.request_logs_from_job.return_value = MockResponse(True, 200)

    # Call
    r = jobs_service.request_logs_from_job(JOB_ID)

    # Assert
    assert r == True
    assert isinstance(r, bool)


def list_jobs():
    jobs_repo.list_jobs.return_value = MockResponse(
        {"jobs": [{"job": i} for i in range(10)]}, 200
    )

    # Call
    r = jobs_service.list_jobs()

    # Assert
    assert r["jobs"] == [{"job": i} for i in range(10)]
    assert r["jobs"][9] == {"job": 9}
