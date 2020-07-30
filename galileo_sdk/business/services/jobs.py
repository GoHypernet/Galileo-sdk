import os
import zipfile

from ..objects.exceptions import JobsException
from ..utils.generate_query_str import generate_query_str
from galileo_sdk.compat import quote


class JobsService:
    def __init__(self, jobs_repo, profile_repo):
        self._jobs_repo = jobs_repo
        self._profile_repo = profile_repo

    def request_send_job(self):
        r = self._jobs_repo.request_send_job()
        return r.json()

    def request_send_job_completed(self, destination_mid, file_name, station_id):
        r = self._jobs_repo.request_send_job_completed(
            destination_mid, file_name, station_id
        )
        return r.json()

    def request_receive_job(self, job_id):
        r = self._jobs_repo.request_receive_job(job_id)
        return r.json()

    def request_receive_job_completed(self, job_id):
        r = self._jobs_repo.request_receive_job_completed(job_id)
        return r.json()

    def submit_job(self, job_id):
        r = self._jobs_repo.submit_job(job_id)
        return r.json()

    def request_stop_job(self, job_id):
        return self._jobs_repo.request_stop_job(job_id)

    def request_pause_job(self, job_id):
        return self._jobs_repo.request_pause_job(job_id)

    def request_start_job(self, job_id):
        return self._jobs_repo.request_start_job(job_id)

    def request_top_from_job(self, job_id):
        return self._jobs_repo.request_top_from_job(job_id)

    def request_logs_from_job(self, job_id):
        return self._jobs_repo.request_logs_from_jobs(job_id)

    def list_jobs(
        self,
        jobids=None,
        receiverids=None,
        oaids=None,
        userids=None,
        stationids=None,
        statuses=None,
        page=1,
        items=25,
        projectids=None,
        archived=False,
        receiver_archived=False,
        partial_names=None,
        lz=None,
        ownerids=None,
        sort_by=None,
        sort_order=None,
    ):
        if userids is None:
            self_profile = self._profile_repo.self()
            userids = [self_profile.userid]
        query = generate_query_str(
            {
                "page": page,
                "items": items,
                "jobids": jobids,
                "receiverids": receiverids,
                "oaids": oaids,
                "userids": userids,
                "stationids": stationids,
                "statuses": statuses,
                "projectids": projectids,
                "archived": archived,
                "receiver_archived": receiver_archived,
                "partial_names": partial_names,
                "machines": lz,
                "ownerids": ownerids,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
        )
        return self._jobs_repo.list_jobs(query)

    def download_job_results(self, job_id, path, nonce=None):
        files = self._jobs_repo.get_results_metadata(job_id)

        if not files:
            raise JobsException(job_id, "No files to download")

        files_downloaded = []

        for file in files:
            absolute_path = os.path.join(path, file.filename)
            self._jobs_repo.download_results(
                job_id,
                generate_query_str(
                    {
                        "filename": quote(file.filename, safe=""),
                        "path": file.path,
                        "nonce": nonce,
                    }
                ),
                os.path.join(path, file.filename),
            )
            files_downloaded.append(absolute_path)

        return files_downloaded

    def download_and_extract_job_results(self, job_id, path, nonce=None):
        files_downloaded = self.download_job_results(job_id, path, nonce)
        for file in files_downloaded:
            dir = file.rsplit(".zip", 1)[0]
            if not os.path.exists(dir):
                os.mkdir(dir)
            with zipfile.ZipFile(file) as zf:
                zf.extractall(dir)

    def update_job(self, request):
        return self._jobs_repo.update_job(request)

    def request_kill_job(self, job_id):
        return self._jobs_repo.request_kill_job(job_id)
