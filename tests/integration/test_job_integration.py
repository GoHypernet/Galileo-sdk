from galileo_sdk import GalileoSdk

# Must set env variables before running tests
from galileo_sdk.business.objects import Job

CONFIG = "development"
# TODO Give Galileo authentication
galileo = GalileoSdk(config=CONFIG)
job_list = galileo.jobs.list_jobs(sort_by="upload_date", sort_order="desc")
jobid = ""
self = galileo.profiles.self()


def test_list_jobs():
    assert isinstance(job_list[0], Job)


galileo.disconnect()
