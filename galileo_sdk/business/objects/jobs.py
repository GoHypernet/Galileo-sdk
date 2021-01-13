import enum

from galileo_sdk.business.objects import EventEmitter


class EJobStatus(enum.Enum):
    uploaded = 0  # job has been uploaded
    submitted = 1  # LZ has been or is cleared to download job
    downloaded = 2  # Job has been downloaded by LZ
    building_image = 3  # Building docker image
    building_container = 4  # Buiding docker container
    start_requested = 5  # Start
    running = 6
    pause_requested = 7
    paused = 8
    stop_requested = 9
    stopped = 10
    exited = 11
    collecting_results = 12
    posting_results = 13
    terminated = 14
    completed = 15
    removed_by_host = 16
    unknown = 17  # Just in case arbitrary update occurs
    post_processing = 18
    started = 19
    built_image = 20
    built_container = 21
    results_posted = 22
    error = 23
    build_error = 24
    kill_requested = 25


class EJobRunningStatus(enum.Enum):
    not_running = 0  # job isn't running
    running = 1  # job is running


class EPaymentStatus(enum.Enum):
    current = 0  # all paid
    payment_due = 1  # Missing a payment
    delinquent = 2  # Delinquent on payments
    missing_offer = 3  # No valid offer found


class UpdateJobRequest:
    def __init__(self, job_id, archived):
        self.job_id = job_id
        self.archived = archived


class JobStatus:
    def __init__(
        self, timestamp, status, jobstatusid=None, jobid=None,
    ):
        self.jobstatusid = jobstatusid
        self.jobid = jobid
        self.timestamp = timestamp
        self.status = status


class Job:
    def __init__(
        self,
        jobid,
        receiverid,
        project_id,
        time_created,
        last_updated,
        status=None,
        cpu_count=1,
        gpu_count=0,
        memory_amount=1000,
        enable_tunnel=False,
        tunnel_port=None,
        tunnel_url=None,
        name=None,
        stationid=None,
        userid=None,
        state=None,
        pay_status=None,
        pay_interval=None,
        total_runtime=None,
        archived=False,
        status_history=None,
    ):
        """
        Job Object 
        
        :param jobid: UUID of the Job
        :param receiver_id: UUID of the recipient Landing Zone
        :param project_id: UUID of the originating Mission
        :param time_created: Time stamp of the Job run time
        :param last_updated: Time stamp of last Job update
        :param status: Current status of the Job
        :param cpu_count: Number of CPUs claimed by the Job
        :param gpu_count: Number of GPUs claimed by the Job
        :param memory_amount: Amount of Memory in MB claimed by the Job
        :param enable_tunnel: Boolean indicated if the job has tunnel access
        :param tunnel_port: The container port exposed if tunneling is enabled
        :param tunnel_url: The URL of the tunnel exposing the container if the job has tunneling enabled
        :param name: Human readable name of the Job
        :param stationid: UUID of the Station the Job was deployed to
        :param userid: UUID of the user who deployed the Job
        :param state: Current state of the Job (potentially superceded by status)
        :param pay_status: Currently unused
        :param pay_interval: Currently unused
        :param total_runtime: Total Job runtime in seconds
        :param archived: Boolean indicating if job is archived 
        :param status_history: Dictionary of Job status and time stamp history
        """
        self.job_id = jobid
        self.receiver_id = receiverid
        self.project_id = project_id
        self.mission_id = project_id
        self.time_created = time_created
        self.last_updated = last_updated
        self.status = status
        self.cpu_count = cpu_count,
        self.gpu_count = gpu_count,
        self.memory_amount = memory_amount,
        self.enable_tunnel = enable_tunnel,
        self.tunnel_port = tunnel_port,
        self.tunnel_url = tunnel_url,
        self.name = name
        self.station_id = stationid
        self.user_id = userid
        self.state = state
        self.pay_status = pay_status
        self.pay_interval = pay_interval
        self.total_runtime = total_runtime
        self.status_history = status_history
        self.archived = archived


class JobLauncherUpdatedEvent:
    def __init__(self, job):
        self.job = job


class JobLauncherResultsDownloadedEvent:
    def __init__(self, resultsid, status):
        self.resultsid = resultsid
        self.status = status


class StationJobUpdatedEvent:
    def __init__(self, job):
        self.job = job


class JobTopEvent:
    def __init__(self, job, top):
        self.job = job
        self.top = top


class JobLogEvent:
    def __init__(self, job, log):
        self.job = job
        self.log = log


class JobLauncherSubmittedEvent:
    def __init__(self, job):
        self.job = job


class TopDetails:
    def __init__(self, title, detail):
        self.title = title
        self.detail = detail


class TopProcess:
    def __init__(self, items):
        self.items = items


class JobsEvents:
    def __init__(self):
        self._events = EventEmitter()

    def on_job_launcher_updated(self, func):
        self._events.on("job_launcher_updated", func)

    def job_launcher_updated(self, event):
        self._events.emit("job_launcher_updated", event)

    def on_job_launcher_results_downloaded(self, func):
        self._events.on("job_launcher_results_downloaded", func)

    def job_launcher_results_downloaded(self, event):
        self._events.emit("job_launcher_results_downloaded", event)

    def on_station_job_updated(self, func):
        self._events.on("station_job_updated", func)

    def station_job_updated(self, event):
        self._events.emit("station_job_updated", event)

    def on_job_top(self, func):
        self._events.on("top", func)

    def job_top(self, event):
        self._events.emit("top", event)

    def on_job_log(self, func):
        self._events.on("log", func)

    def job_log(self, event):
        self._events.emit("log", event)

    def on_job_launcher_submitted(self, func):
        self._events.on("job_launcher_submitted", func)

    def job_launcher_submitted(self, event):
        self._events.emit("job_launcher_submitted", event)
