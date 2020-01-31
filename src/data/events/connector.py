from typing import Any

import socketio

from ...business.objects.jobs import (JobLauncherResultsDownloadedEvent,
                                      JobLauncherUpdatedEvent, JobLogEvent,
                                      JobsEvents, JobTopEvent,
                                      StationJobUpdatedEvent)
from ...business.objects.machines import (MachinesEvents,
                                          MachineStatusUpdateEvent)
from ...business.objects.stations import (NewStationEvent,
                                          StationAdminInviteSentEvent,
                                          StationsEvents,
                                          StationUserInviteReceivedEvent)
from ..providers.auth import AuthProvider
from ..repositories.settings import SettingsRepository


class GalileoConnector:
    _socket: socketio.Client
    machines_events: MachinesEvents
    jobs_events: JobsEvents
    station_events: StationsEvents

    def __init__(self, settings_repo: SettingsRepository, auth_provider: AuthProvider):
        self._settings_repo = settings_repo
        self._auth_provider = auth_provider
        self.machines_events = MachinesEvents()
        self.jobs_events = JobsEvents()
        settings = self._settings_repo.get_settings()
        token = self._auth_provider.get_access_token()
        self._socket = socketio.Client()
        self._socket.connect(
            f"{settings.backend}/galileo/user_interface/v1",
            headers={"Authorization": f"Bearer {token}"},
        )

        self._register_listeners()

    def _register_listeners(self):
        # Machines
        @self._socket.on("machine/status_updated")
        def on_machine_status_updated(data: Any):
            self.machines_events.machine_status_update(
                MachineStatusUpdateEvent(mid=data["mid"], status=data["status"])
            )

        # Jobs
        @self._socket.on("job_launcher_updated")
        def on_job_launcher_updated(data: Any):
            self.jobs_events.job_launcher_updated(JobLauncherUpdatedEvent(data["job"]))

        @self._socket.on("job_launcher_results_downloaded")
        def on_job_launcher_results_downloaded(resultsid, status):
            self.jobs_events.job_launcher_results_downloaded(
                JobLauncherResultsDownloadedEvent(resultsid, status)
            )

        @self._socket.on("station_job_updated")
        def on_station_job_updated(data: Any):
            self.jobs_events.station_job_updated(StationJobUpdatedEvent(data["job"]))

        @self._socket.on("top")
        def on_job_top(data: Any):
            self.jobs_events.job_top(JobTopEvent(data["job"], data["top"]))

        @self._socket.on("log")
        def on_job_log(data: Any):
            self.jobs_events.job_log(JobLogEvent(data["job"], data["log"]))

        # Stations
        @self._socket.on("new_station")
        def on_new_station(data: Any):
            self.station_events.new_station(NewStationEvent(data["station"]))

        @self._socket.on("station_admin_invite_sent")
        def on_station_admin_invite_sent(data: Any):
            self.station_events.station_admin_invite_sent(
                StationAdminInviteSentEvent(data["stationid"], data["userids"])
            )

        @self._socket.on("station_user_invite_received")
        def on_station_user_invite_received(data: Any):
            self.station_events.station_user_invite_received(
                StationUserInviteReceivedEvent(data["station"])
            )

        # @self._socket.on("station_admin_invite_accepted")
        # @self._socket.on("station_member_member_added")
        # @self._socket.on("station_user_invite_accepted")
        # @self._socket.on("station_admin_invite_rejected")
        # @self._socket.on("station_admin_request_received")
        # @self._socket.on("station_user_request_sent")
        # @self._socket.on("station_admin_request_accepted")
        # @self._socket.on("station_user_request_accepted")
        # @self._socket.on("station_admin_request_rejected")
        # @self._socket.on("station_user_request_rejected")
        # @self._socket.on("station_admin_member_removed")
        # @self._socket.on("station_admin_machine_removed")
        # @self._socket.on("station_member_member_removed")
        # @self._socket.on("station_member_machine_removed")
        # @self._socket.on("station_user_withdrawn")
        # @self._socket.on("station_user_expelled")
        # @self._socket.on("station_admin_destroyed")
        # @self._socket.on("station_member_destroyed")
        # @self._socket.on("station_user_invite_destroyed")
        # @self._socket.on("station_user_request_destroyed")
        # @self._socket.on("station_admin_machine_added")
        # @self._socket.on("station_member_machine_added")
        # @self._socket.on("station_admin_volume_added")
        # @self._socket.on("station_member_volume_added")
        # @self._socket.on("station_admin_volume_host_path_added")
        # @self._socket.on("station_member_volume_host_path_added")
        # @self._socket.on("station_admin_volume_host_path_removed")
        # @self._socket.on("station_member_volume_host_path_removed")
        # @self._socket.on("station_admin_volume_removed")
        # @self._socket.on("station_member_volume_removed")
