from galileo_sdk import GalileoSdk
# Must set env variables before running tests
from galileo_sdk.business.objects import Job
from galileo_sdk.business.objects.jobs import UpdateJobRequest

CONFIG = "http://localhost:8080"

galileo = GalileoSdk(config=CONFIG)
job_list = galileo.jobs.list_jobs()
jobid = ""


def test_list_jobs():
    assert isinstance(job_list[0], Job)


def test_update_job():
    archived_job = galileo.jobs.update_job(UpdateJobRequest(job_list[0].job_id, True))
    assert archived_job.archived == True
    unarchived_job = galileo.jobs.update_job(
        UpdateJobRequest(job_list[0].job_id, False)
    )
    assert unarchived_job.archived == False


galileo.disconnect()
