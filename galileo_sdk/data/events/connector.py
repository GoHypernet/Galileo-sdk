from typing import Any

import socketio

from galileo_sdk.data.repositories.jobs import job_dict_to_job
from galileo_sdk.data.repositories.machines import machine_dict_to_machine
from galileo_sdk.data.repositories.stations import (station_dict_to_station,
                                                    volume_dict_to_volume)

from ...business.objects.jobs import (JobLauncherSubmittedEvent,
                                      JobLauncherUpdatedEvent, JobsEvents,
                                      StationJobUpdatedEvent)
from ...business.objects.machines import (EMachineStatus,
                                          MachineHardwareUpdateEvent,
                                          MachineRegisteredEvent,
                                          MachinesEvents,
                                          MachineStatusUpdateEvent)
from ...business.objects.projects import ProjectsEvents
from ...business.objects.stations import (
    NewStationEvent, StationAdminDestroyedEvent,
    StationAdminInviteAcceptedEvent, StationAdminInviteRejectedEvent,
    StationAdminInviteSentEvent, StationAdminMachineAddedEvent,
    StationAdminMachineRemovedEvent, StationAdminMemberRemovedEvent,
    StationAdminRequestAcceptedEvent, StationAdminRequestReceivedEvent,
    StationAdminRequestRejectedEvent, StationAdminStationUpdated,
    StationAdminVolumeAddedEvent, StationAdminVolumeHostPathAddedEvent,
    StationAdminVolumeHostPathRemovedEvent, StationAdminVolumeRemovedEvent,
    StationMemberDestroyedEvent, StationMemberMachineAddedEvent,
    StationMemberMachineRemovedEvent, StationMemberMemberEvent,
    StationMemberMemberRemovedEvent, StationMemberStationUpdated,
    StationMemberVolumeAddedEvent, StationMemberVolumeHostPathAddedEvent,
    StationMemberVolumeHostPathRemovedEvent, StationMemberVolumeRemovedEvent,
    StationsEvents, StationUserExpelledEvent, StationUserInviteAcceptedEvent,
    StationUserInviteDestroyedEvent, StationUserInviteReceivedEvent,
    StationUserInviteRejectedEvent, StationUserRequestAcceptedEvent,
    StationUserRequestDestroyedEvent, StationUserRequestRejectedEvent,
    StationUserRequestSentEvent, StationUserWithdrawnEvent)
from ..providers.auth import AuthProvider
from ..repositories.settings import SettingsRepository


class GalileoConnector:
    machines_events: MachinesEvents
    jobs_events: JobsEvents
    stations_events: StationsEvents
    projects_events: ProjectsEvents

    def __init__(
        self,
        settings_repo: SettingsRepository,
        auth_provider: AuthProvider,
        namespace: str,
    ):
        self._settings_repo = settings_repo
        self._auth_provider = auth_provider
        self.machines_events = MachinesEvents()
        self.jobs_events = JobsEvents()
        self.stations_events = StationsEvents()
        settings = self._settings_repo.get_settings()
        token = self._auth_provider.get_access_token()
        self.namespace = namespace
        self._socket = socketio.Client()
        self._socket.connect(
            f"{settings.backend}{self.namespace}",
            headers={"Authorization": f"Bearer {token}"},
            transports="websocket",
            namespaces=[self.namespace],
        )
        self._register_jobs_listeners()
        self._register_machines_listeners()
        self._register_stations_listeners()

    def on(self, event, handler=None):
        def wrapper(handler):
            self._socket.on(event, handler, self.namespace)

        if handler is None:
            return wrapper
        wrapper(handler)

    def _register_machines_listeners(self):
        # Machines
        @self.on("machine/status_updated")
        def on_machine_status_updated(data: Any):
            self.machines_events.machine_status_update(
                MachineStatusUpdateEvent(
                    mid=data["mid"], status=EMachineStatus[data["status"]]
                )
            )

        @self.on("machine/registered")
        def on_machine_registered(data: Any):
            self.machines_events.machine_registered(
                MachineRegisteredEvent(machine_dict_to_machine(data["machine"]))
            )

        @self.on("machine/hardware_updated")
        def on_machine_hardware_updated(data: Any):
            self.machines_events.machine_hardware_update(
                MachineHardwareUpdateEvent(machine_dict_to_machine(data["machine"]))
            )

    def _register_jobs_listeners(self):
        # Jobs
        @self.on("job_launcher_updated")
        def on_job_launcher_updated(data: Any):
            self.jobs_events.job_launcher_updated(
                JobLauncherUpdatedEvent(job_dict_to_job(data["job"]))
            )

        @self.on("station_job_updated")
        def on_station_job_updated(data: Any):
            self.jobs_events.station_job_updated(
                StationJobUpdatedEvent(job_dict_to_job(data["job"]))
            )

        @self.on("job_launcher_submitted")
        def on_job_launcher_submitted(data: Any):
            self.jobs_events.job_launcher_submitted(
                JobLauncherSubmittedEvent(job_dict_to_job(data["job"]))
            )

    def _register_stations_listeners(self):
        # Stations
        @self.on("new_station")
        def on_new_station(data: Any):
            self.stations_events.new_station(
                NewStationEvent(station_dict_to_station(data["station"]))
            )

        @self.on("station_admin_invite_sent")
        def on_station_admin_invite_sent(data: Any):
            self.stations_events.station_admin_invite_sent(
                StationAdminInviteSentEvent(data["stationid"], data["userids"])
            )

        @self.on("station_user_invite_received")
        def on_station_user_invite_received(data: Any):
            self.stations_events.station_user_invite_received(
                StationUserInviteReceivedEvent(station_dict_to_station(data["station"]))
            )

        @self.on("station_admin_invite_accepted")
        def on_station_admin_invite_accepted(data: Any):
            self.stations_events.station_admin_invite_accepted(
                StationAdminInviteAcceptedEvent(data["stationid"], data["userid"])
            )

        @self.on("station_member_member_added")
        def on_station_member_member_added(data: Any):
            self.stations_events.station_member_member_added(
                StationMemberMemberEvent(data["stationid"], data["userid"])
            )

        @self.on("station_user_invite_accepted")
        def on_station_user_invite_accepted(data: Any):
            self.stations_events.station_user_invite_accepted(
                StationUserInviteAcceptedEvent(data["stationid"], data["userid"])
            )

        @self.on("station_admin_invite_rejected")
        def on_station_admin_invite_rejected(data: Any):
            self.stations_events.station_admin_invite_rejected(
                StationAdminInviteRejectedEvent(data["stationid"], data["userids"])
            )

        @self.on("station_user_invite_rejected")
        def on_station_user_invite_rejected(data: Any):
            self.stations_events.station_user_invite_rejected(
                StationUserInviteRejectedEvent(data["stationid"], data["userids"])
            )

        @self.on("station_admin_request_received")
        def on_station_admin_request_received(data: Any):
            self.stations_events.station_admin_request_received(
                StationAdminRequestReceivedEvent(data["stationid"], data["userid"])
            )

        @self.on("station_user_request_sent")
        def on_station_user_request_sent(data: Any):
            self.stations_events.station_user_request_sent(
                StationUserRequestSentEvent(data["stationid"], data["userid"])
            )

        @self.on("station_admin_request_accepted")
        def on_station_admin_request_accepted(data: Any):
            self.stations_events.station_admin_request_accepted(
                StationAdminRequestAcceptedEvent(data["stationid"], data["userid"])
            )

        @self.on("station_user_request_accepted")
        def on_station_user_request_accepted(data: Any):
            self.stations_events.station_user_request_accepted(
                StationUserRequestAcceptedEvent(data["stationid"])
            )

        @self.on("station_admin_request_rejected")
        def on_station_admin_request_rejected(data: Any):
            self.stations_events.station_admin_request_rejected(
                StationAdminRequestRejectedEvent(data["stationid"], data["userid"])
            )

        @self.on("station_user_request_rejected")
        def on_station_user_request_rejected(data: Any):
            self.stations_events.station_user_request_rejected(
                StationUserRequestRejectedEvent(data["stationid"])
            )

        @self.on("station_admin_member_removed")
        def on_station_admin_member_removed(data: Any):
            self.stations_events.station_admin_member_removed(
                StationAdminMemberRemovedEvent(data["stationid"], data["userids"])
            )

        @self.on("station_admin_machine_removed")
        def on_station_admin_machine_removed(data: Any):
            self.stations_events.station_admin_machine_removed(
                StationAdminMachineRemovedEvent(data["stationid"], data["mids"])
            )

        @self.on("station_member_member_removed")
        def on_station_member_member_removed(data: Any):
            self.stations_events.station_member_member_removed(
                StationMemberMemberRemovedEvent(data["stationid"], data["userids"])
            )

        @self.on("station_member_machine_removed")
        def on_station_member_machine_removed(data: Any):
            self.stations_events.station_member_machine_removed(
                StationMemberMachineRemovedEvent(data["stationid"], data["mids"])
            )

        @self.on("station_user_withdrawn")
        def on_station_user_withdrawn(data: Any):
            self.stations_events.station_user_withdrawn(
                StationUserWithdrawnEvent(data["stationid"], data["mids"])
            )

        @self.on("station_user_expelled")
        def on_station_user_expelled(data: Any):
            self.stations_events.station_user_expelled(
                StationUserExpelledEvent(data["stationid"])
            )

        @self.on("station_admin_destroyed")
        def on_station_admin_destroyed(data: Any):
            self.stations_events.station_admin_destroyed(
                StationAdminDestroyedEvent(data["stationid"])
            )

        @self.on("station_member_destroyed")
        def on_station_member_destroyed(data: Any):
            self.stations_events.station_member_destroyed(
                StationMemberDestroyedEvent(data["stationid"])
            )

        @self.on("station_user_invite_destroyed")
        def on_station_user_invite_destroyed(data: Any):
            self.stations_events.station_user_invite_destroyed(
                StationUserInviteDestroyedEvent(data["stationid"])
            )

        @self.on("station_user_request_destroyed")
        def on_station_user_request_destroyed(data: Any):
            self.stations_events.station_user_request_destroyed(
                StationUserRequestDestroyedEvent(data["stationid"])
            )

        @self.on("station_admin_machine_added")
        def on_station_admin_machine_added(data: Any):
            self.stations_events.station_admin_machine_added(
                StationAdminMachineAddedEvent(data["stationid"], data["mids"])
            )

        @self.on("station_member_machine_added")
        def on_station_member_machine_added(data: Any):
            self.stations_events.station_member_machine_added(
                StationMemberMachineAddedEvent(data["stationid"], data["mids"])
            )

        @self.on("station_admin_volume_added")
        def on_station_admin_volume_added(data: Any):
            self.stations_events.station_admin_volume_added(
                StationAdminVolumeAddedEvent(
                    data["stationid"],
                    [
                        volume_dict_to_volume(value)
                        for key, value in data["volumes"].items()
                    ],
                )
            )

        @self.on("station_member_volume_added")
        def on_station_member_volume_added(data: Any):
            self.stations_events.station_member_volume_added(
                StationMemberVolumeAddedEvent(
                    data["stationid"],
                    [
                        volume_dict_to_volume(value)
                        for key, value in data["volumes"].items()
                    ],
                )
            )

        @self.on("station_admin_volume_host_path_added")
        def on_station_admin_volume_host_path_added(data: Any):
            self.stations_events.station_admin_volume_host_path_added(
                StationAdminVolumeHostPathAddedEvent(
                    data["stationid"],
                    [
                        volume_dict_to_volume(value)
                        for key, value in data["volumes"].items()
                    ],
                )
            )

        @self.on("station_member_volume_host_path_added")
        def on_station_member_volume_host_path_added(data: Any):
            self.stations_events.station_member_volume_host_path_added(
                StationMemberVolumeHostPathAddedEvent(
                    data["stationid"],
                    [
                        volume_dict_to_volume(value)
                        for key, value in data["volumes"].items()
                    ],
                )
            )

        @self.on("station_admin_volume_host_path_removed")
        def on_station_admin_volume_host_path_removed(data: Any):
            self.stations_events.station_admin_volume_host_path_removed(
                StationAdminVolumeHostPathRemovedEvent(
                    data["stationid"],
                    [
                        volume_dict_to_volume(value)
                        for key, value in data["volumes"].items()
                    ],
                )
            )

        @self.on("station_member_volume_host_path_removed")
        def on_station_member_volume_host_path_removed(data: Any):
            self.stations_events.station_member_volume_host_path_removed(
                StationMemberVolumeHostPathRemovedEvent(
                    data["stationid"],
                    [
                        volume_dict_to_volume(value)
                        for key, value in data["volumes"].items()
                    ],
                )
            )

        @self.on("station_admin_volume_removed")
        def on_station_admin_volume_removed(data: Any):
            self.stations_events.station_admin_volume_removed(
                StationAdminVolumeRemovedEvent(data["stationid"], data["volume_names"])
            )

        @self.on("station_member_volume_removed")
        def on_station_member_volume_removed(data: Any):
            self.stations_events.station_member_volume_removed(
                StationMemberVolumeRemovedEvent(data["stationid"], data["volume_names"])
            )

        @self.on("station_admin_station_updated")
        def on_station_admin_station_updated(data: Any):
            self.stations_events.station_admin_station_updated(
                StationAdminStationUpdated(station_dict_to_station(data["station"]))
            )

        @self.on("station_member_station_updated")
        def on_station_member_station_updated(data: Any):
            self.stations_events.station_member_station_updated(
                StationMemberStationUpdated(station_dict_to_station(data["station"]))
            )

    def disconnect(self):
        self._socket.disconnect()
