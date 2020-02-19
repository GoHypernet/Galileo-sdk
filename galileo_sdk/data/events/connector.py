from typing import Any

import socketio

from ...business.objects.jobs import (JobLauncherResultsDownloadedEvent,
                                      JobLauncherUpdatedEvent, JobLogEvent,
                                      JobsEvents, JobTopEvent,
                                      StationJobUpdatedEvent)
from ...business.objects.machines import (MachinesEvents,
                                          MachineStatusUpdateEvent)
from ...business.objects.projects import ProjectsEvents
from ...business.objects.stations import (
    NewStationEvent, StationAdminDestroyedEvent,
    StationAdminInviteAcceptedEvent, StationAdminInviteSentEvent,
    StationAdminMachineAddedEvent, StationAdminMachineRemovedEvent,
    StationAdminMemberRemovedEvent, StationAdminRequestAcceptedEvent,
    StationAdminRequestReceivedEvent, StationAdminRequestRejectedEvent,
    StationAdminVolumeAddedEvent, StationAdminVolumeHostPathAddedEvent,
    StationAdminVolumeHostPathRemovedEvent, StationAdminVolumeRemovedEvent,
    StationMemberDestroyedEvent, StationMemberMachineAddedEvent,
    StationMemberMachineRemovedEvent, StationMemberMemberEvent,
    StationMemberMemberRemovedEvent, StationMemberVolumeAddedEvent,
    StationMemberVolumeHostPathAddedEvent,
    StationMemberVolumeHostPathRemovedEvent, StationMemberVolumeRemovedEvent,
    StationsEvents, StationUserExpelledEvent, StationUserInviteAcceptedEvent,
    StationUserInviteDestroyedEvent, StationUserInviteReceivedEvent,
    StationUserInviteRejectedEvent, StationUserRequestAcceptedEvent,
    StationUserRequestDestroyedEvent, StationUserRequestRejectedEvent,
    StationUserRequestSentEvent, StationUserWithdrawnEvent)
from ..providers.auth import AuthProvider
from ..repositories.settings import SettingsRepository


class GalileoConnector:
    _socket: socketio.Client
    machines_events: MachinesEvents
    jobs_events: JobsEvents
    stations_events: StationsEvents
    projects_events: ProjectsEvents

    def __init__(self, settings_repo: SettingsRepository, auth_provider: AuthProvider):
        self._settings_repo = settings_repo
        self._auth_provider = auth_provider
        self.machines_events = MachinesEvents()
        self.jobs_events = JobsEvents()
        self.stations_events = StationsEvents()
        settings = self._settings_repo.get_settings()
        token = self._auth_provider.get_access_token()
        self._socket = socketio.Client()
        self._socket.connect(
            f"{settings.backend}/galileo/user_interface/v1",
            headers={"Authorization": f"Bearer {token}"},
        )
        self._register_jobs_listeners()
        self._register_machines_listeners()
        self._register_stations_listeners()

    def _register_machines_listeners(self):
        # Machines
        @self._socket.on("machine/status_updated")
        def on_machine_status_updated(data: Any):
            self.machines_events.machine_status_update(
                MachineStatusUpdateEvent(mid=data["mid"], status=data["status"])
            )

    def _register_jobs_listeners(self):
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

    def _register_stations_listeners(self):
        # Stations
        @self._socket.on("new_station")
        def on_new_station(data: Any):
            self.stations_events.new_station(NewStationEvent(data["station"]))

        @self._socket.on("station_admin_invite_sent")
        def on_station_admin_invite_sent(data: Any):
            self.stations_events.station_admin_invite_sent(
                StationAdminInviteSentEvent(data["stationid"], data["userids"])
            )

        @self._socket.on("station_user_invite_received")
        def on_station_user_invite_received(data: Any):
            self.stations_events.station_user_invite_received(
                StationUserInviteReceivedEvent(data["station"])
            )

        @self._socket.on("station_admin_invite_accepted")
        def on_station_admin_invite_accepted(data: Any):
            self.stations_events.station_admin_invite_accepted(
                StationAdminInviteAcceptedEvent(data["stationid"], data["userids"])
            )

        @self._socket.on("station_member_member_added")
        def on_station_member_member_added(data: Any):
            self.stations_events.station_member_member_added(
                StationMemberMemberEvent(data["stationid"], data["userid"])
            )

        @self._socket.on("station_user_invite_accepted")
        def on_station_user_invite_accepted(data: Any):
            self.stations_events.station_user_invite_accepted(
                StationUserInviteAcceptedEvent(data["stationid"])
            )

        @self._socket.on("station_admin_invite_rejected")
        def on_station_admin_invite_rejected(data: Any):
            self.station_events.station_admin_invite_rejected(
                StationUserInviteRejectedEvent(data["stationid"])
            )

        @self._socket.on("station_admin_request_received")
        def on_station_admin_request_received(data: Any):
            self.stations_events.station_admin_request_received(
                StationAdminRequestReceivedEvent(data["stationid"], data["userid"])
            )

        @self._socket.on("station_user_request_sent")
        def on_station_user_request_sent(data: Any):
            self.stations_events.station_user_request_sent(
                StationUserRequestSentEvent(data["stationid"], data["userid"])
            )

        @self._socket.on("station_admin_request_accepted")
        def on_station_admin_request_accepted(data: Any):
            self.stations_events.station_admin_request_accepted(
                StationAdminRequestAcceptedEvent(data["stationid"], data["userid"])
            )

        @self._socket.on("station_user_request_accepted")
        def on_station_user_request_accepted(data: Any):
            self.stations_events.station_user_request_accepted(
                StationUserRequestAcceptedEvent(data["stationid"])
            )

        @self._socket.on("station_admin_request_rejected")
        def on_station_admin_request_rejected(data: Any):
            self.stations_events.station_admin_request_rejected(
                StationAdminRequestRejectedEvent(data["stationid"], data["userid"])
            )

        @self._socket.on("station_user_request_rejected")
        def on_station_user_request_rejected(data: Any):
            self.stations_events.station_user_request_rejected(
                StationUserRequestRejectedEvent(data["stationid"])
            )

        @self._socket.on("station_admin_member_removed")
        def on_station_admin_member_removed(data: Any):
            self.stations_events.station_admin_member_removed(
                StationAdminMemberRemovedEvent(data["stationid"], data["userid"])
            )

        @self._socket.on("station_admin_machine_removed")
        def on_station_admin_machine_removed(data: Any):
            self.stations_events.station_admin_machine_removed(
                StationAdminMachineRemovedEvent(data["stationid"], data["mids"])
            )

        @self._socket.on("station_member_member_removed")
        def on_station_member_member_removed(data: Any):
            self.stations_events.station_member_member_removed(
                StationMemberMemberRemovedEvent(data["stationid"], data["mids"])
            )

        @self._socket.on("station_member_machine_removed")
        def on_station_member_machine_removed(data: Any):
            self.stations_events.station_member_machine_removed(
                StationMemberMachineRemovedEvent(data["stationid"], data["mids"])
            )

        @self._socket.on("station_user_withdrawn")
        def on_station_user_withdrawn(data: Any):
            self.stations_events.station_user_withdrawn(
                StationUserWithdrawnEvent(data["stationid"], data["mids"])
            )

        @self._socket.on("station_user_expelled")
        def on_station_user_expelled(data: Any):
            self.stations_events.station_user_expelled(
                StationUserExpelledEvent(data["stationid"])
            )

        @self._socket.on("station_admin_destroyed")
        def on_station_admin_destroyed(data: Any):
            self.stations_events.station_admin_destroyed(
                StationAdminDestroyedEvent(data["admin"])
            )

        @self._socket.on("station_member_destroyed")
        def on_station_member_destroyed(data: Any):
            self.stations_events.station_member_destroyed(
                StationMemberDestroyedEvent(data["stationid"])
            )

        @self._socket.on("station_user_invite_destroyed")
        def on_station_user_invite_destroyed(data: Any):
            self.stations_events.station_user_invite_destroyed(
                StationUserInviteDestroyedEvent(data["stationid"])
            )

        @self._socket.on("station_user_request_destroyed")
        def on_station_user_request_destroyed(data: Any):
            self.stations_events.station_user_request_destroyed(
                StationUserRequestDestroyedEvent(data["stationid"])
            )

        @self._socket.on("station_admin_machine_added")
        def on_station_admin_machine_added(data: Any):
            self.stations_events.station_admin_machine_added(
                StationAdminMachineAddedEvent(data["stationid"], data["mids"])
            )

        @self._socket.on("station_member_machine_added")
        def on_station_member_machine_added(data: Any):
            self.stations_events.station_member_machine_added(
                StationMemberMachineAddedEvent(data["stationid"], data["mids"])
            )

        @self._socket.on("station_admin_volume_added")
        def on_station_admin_volume_added(data: Any):
            self.stations_events.station_admin_volume_added(
                StationAdminVolumeAddedEvent(data["stationid"], data["volumes"])
            )

        @self._socket.on("station_member_volume_added")
        def on_station_member_volume_added(data: Any):
            self.stations_events.station_member_volume_added(
                StationMemberVolumeAddedEvent(data["stationid"], data["volumes"])
            )

        @self._socket.on("station_admin_volume_host_path_added")
        def on_station_admin_volume_host_path_added(data: Any):
            self.stations_events.station_admin_volume_host_path_added(
                StationAdminVolumeHostPathAddedEvent(data["stationid"], data["volumes"])
            )

        @self._socket.on("station_member_volume_host_path_added")
        def on_station_member_volume_host_path_added(data: Any):
            self.stations_events.station_member_volume_host_path_added(
                StationMemberVolumeHostPathAddedEvent(
                    data["stationid"], data["volumes"]
                )
            )

        @self._socket.on("station_admin_volume_host_path_removed")
        def on_station_admin_volume_host_path_removed(data: Any):
            self.stations_events.station_admin_volume_host_path_removed(
                StationAdminVolumeHostPathRemovedEvent(
                    data["stationid"], data["volumes"]
                )
            )

        @self._socket.on("station_member_volume_host_path_removed")
        def on_station_member_volume_host_path_removed(data: Any):
            self.stations_events.station_member_volume_host_path_removed(
                StationMemberVolumeHostPathRemovedEvent(
                    data["stationid"], data["volumes"]
                )
            )

        @self._socket.on("station_admin_volume_removed")
        def on_station_admin_volume_removed(data: Any):
            self.stations_events.station_admin_volume_removed(
                StationAdminVolumeRemovedEvent(data["stationid"], data["volume_names"])
            )

        @self._socket.on("station_member_volume_removed")
        def on_station_member_volume_removed(data: Any):
            self.stations_events.station_member_volume_removed(
                StationMemberVolumeRemovedEvent(data["stationid"], data["volume_names"])
            )
