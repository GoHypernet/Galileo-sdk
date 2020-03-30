from datetime import datetime
from galileo_sdk.compat import urlunparse, requests

from galileo_sdk.business.objects import (EJobStatus, Job, JobStatus,
                                          UpdateJobRequest)
from galileo_sdk.business.objects.jobs import (FileListing, TopDetails,
                                               TopProcess)

import sys

_ver = sys.version_info

is_py2 = (_ver[0] == 2)
is_py3 = (_ver[0] == 3)

class JobsRepository:
    def __init__(
        self, settings_repository, auth_provider, namespace,
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider
        self._namespace = namespace

    def _make_url(
        self, endpoint, params, query, fragment,
    ):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse(
            (
                schema,
                "{addr}{namespace}".format(addr=addr, namespace=self._namespace),
                endpoint,
                params,
                query,
                fragment,
            )
        )

    def _request(
        self, request, endpoint, data=None, params=None, query=None, fragment=None,
    ):
        url = self._make_url(endpoint, params, query, fragment)
        access_token = self._auth_provider.get_access_token()
        headers = {
            "Authorization": "Bearer {access_token}".format(access_token=access_token)
        }
        r = request(url, json=data, headers=headers)
        r.raise_for_status()
        return r

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request(requests.post, *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request(requests.put, *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._request(requests.delete, *args, **kwargs)

    def request_send_job(self):
        return self._get("/job/upload_request")

    def request_send_job_completed(self, destination_mid, filename, station_id):
        return self._post(
            "/jobs",
            {
                "destination_mid": destination_mid,
                "filename": filename,
                "stationid": station_id,
            },
        )

    def request_receive_job(self, job_id):
        return self._get("/jobs/{job_id}/results/location".format(job_id=job_id))

    def request_receive_job_completed(self, job_id):
        return self._put(
            "/jobs/{job_id}/results/download_complete".format(job_id=job_id)
        )

    def submit_job(self, job_id):
        return self._put("/jobs/{job_id}/run".format(job_id=job_id))

    def request_stop_job(self, job_id):
        response = self._put("/jobs/{job_id}/stop".format(job_id=job_id))
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def request_pause_job(self, job_id):
        response = self._put("/jobs/{job_id}/pause".format(job_id=job_id))
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def request_start_job(self, job_id):
        response = self._put("/jobs/{job_id}/start".format(job_id=job_id))
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def request_top_from_job(self, job_id):
        response = self._get("/jobs/{job_id}/top".format(job_id=job_id))
        json = response.json()
        top = json["top"]
        return [
            top_dict_to_jobs_top(process, top["Titles"]) for process in top["Processes"]
        ]

    def request_logs_from_jobs(self, job_id):
        response = self._get("/jobs/{job_id}/logs".format(job_id=job_id))
        json = response.json()
        logs = json["logs"]
        return logs

    def list_jobs(self, query):
        response = self._get("/jobs", query=query)
        json = response.json()
        jobs = json["jobs"]
        return [job_dict_to_job(job) for job in jobs]

    def get_results_url(self, job_id):
        response = self._get("/jobs/{job_id}/results".format(job_id=job_id))
        json = response.json()
        files = json["files"]
        return [file_dict_to_file_listing(file) for file in files]

    def download_results(self, job_id, query, filename):
        if is_py3:
            with self._get(
                "/jobs/{job_id}/results".format(job_id=job_id), query=query
            ) as r:
                with open(filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
        elif is_py2:
            r = self._get("/jobs/{job_id}/results".format(job_id=job_id), query=query)
            f = open(filename, "wb")
            f.write(r.json_obj)
            
        return filename

    def update_job(self, request):
        response = self._put(
            "/jobs/{job_id}".format(job_id=request.job_id),
            {"archived": request.archived},
        )
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)

    def request_kill_job(self, job_id):
        response = self._put("/jobs/{job_id}/kill".format(job_id=job_id))
        json = response.json()
        job = json["job"]
        return job_dict_to_job(job)


def top_dict_to_jobs_top(process, titles):
    return TopProcess(
        [TopDetails(title, detail) for detail, title in zip(process, titles)]
    )


def file_dict_to_file_listing(file):
    return FileListing(file["filename"], file["path"])


def job_dict_to_job(job):
    return Job(
        job["jobid"],
        job["receiverid"],
        job["project_id"],
        datetime.fromtimestamp(job["time_created"]),
        datetime.fromtimestamp(job["last_updated"]),
        job["status"],
        job["container"],
        job["name"],
        job["stationid"],
        job["userid"],
        job["state"],
        job["oaid"],
        job["pay_status"],
        job["pay_interval"],
        job["total_runtime"],
        job["archived"],
        [
            job_status_dict_to_job_status(job_status)
            for job_status in job["status_history"]
        ],
    )


def job_status_dict_to_job_status(job_status):
    status = JobStatus(
        datetime.fromtimestamp(job_status["timestamp"]),
        EJobStatus[job_status["status"]],
    )
    status.jobstatusid = (
        job_status["jobstatusid"] if "jobstatusid" in job_status else None
    )
    status.jobid = job_status["jobid"] if "jobid" in job_status else None
    return status
