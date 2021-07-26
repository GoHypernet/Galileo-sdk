import sys

if sys.version_info[0] == 3:
    import socketio

    from galileo_sdk.business.objects.jobs import (
        JobLauncherSubmittedEvent,
        JobLauncherUpdatedEvent,
        JobsEvents,
        StationJobUpdatedEvent,
    )
    from galileo_sdk.business.objects.lz import (
        ELzStatus,
        LzHardwareUpdateEvent,
        LzRegisteredEvent,
        LzEvents,
        LzStatusUpdateEvent,
    )
    from galileo_sdk.business.objects.stations import (
        NewStationEvent,
        StationAdminDestroyedEvent,
        StationAdminInviteAcceptedEvent,
        StationAdminInviteRejectedEvent,
        StationAdminInviteSentEvent,
        StationAdminLzAddedEvent,
        StationAdminLzRemovedEvent,
        StationAdminMemberRemovedEvent,
        StationAdminRequestAcceptedEvent,
        StationAdminRequestReceivedEvent,
        StationAdminRequestRejectedEvent,
        StationAdminStationUpdated,
        StationAdminVolumeAddedEvent,
        StationAdminVolumeHostPathAddedEvent,
        StationAdminVolumeHostPathRemovedEvent,
        StationAdminVolumeRemovedEvent,
        StationMemberDestroyedEvent,
        StationMemberLzAddedEvent,
        StationMemberLzRemovedEvent,
        StationMemberMemberEvent,
        StationMemberMemberRemovedEvent,
        StationMemberStationUpdated,
        StationMemberVolumeAddedEvent,
        StationMemberVolumeHostPathAddedEvent,
        StationMemberVolumeHostPathRemovedEvent,
        StationMemberVolumeRemovedEvent,
        StationsEvents,
        StationUserExpelledEvent,
        StationUserInviteAcceptedEvent,
        StationUserInviteDestroyedEvent,
        StationUserInviteReceivedEvent,
        StationUserInviteRejectedEvent,
        StationUserRequestAcceptedEvent,
        StationUserRequestDestroyedEvent,
        StationUserRequestRejectedEvent,
        StationUserRequestSentEvent,
        StationUserWithdrawnEvent,
    )
    from galileo_sdk.data.repositories.jobs import job_dict_to_job
    from galileo_sdk.data.repositories.lz import lz_dict_to_lz
    from galileo_sdk.data.repositories.stations import (
        station_dict_to_station,
        volume_dict_to_volume,
    )

    class GalileoConnector:
        def __init__(
            self,
            settings_repo,
            auth_provider,
            namespace,
        ):
            self._settings_repo = settings_repo
            self._auth_provider = auth_provider
            self.lz_events = None
            self.jobs_events = None
            self.stations_events = None
            self._socket = None
            self.namespace = namespace

        def on(self, event, handler=None):
            def wrapper(handler):
                self._socket.on(event, handler, self.namespace)

            if handler is None:
                return wrapper
            wrapper(handler)

        def set_socket_io_connection(self):
            settings = self._settings_repo.get_settings()
            token = self._auth_provider.get_access_token()
            self._socket = socketio.Client()
            self._socket.connect(
                "{backend}{namespace}".format(backend=settings.backend,
                                              namespace=self.namespace),
                headers={
                    "Authorization": "Bearer {token}".format(token=token)
                },
                transports="websocket",
                namespaces=[self.namespace],
            )

        def set_lz_events(self):
            self.set_socket_io_connection()
            self.lz_events = LzEvents()
            self._register_machines_listeners()
            return self.lz_events

        def set_jobs_events(self):
            self.set_socket_io_connection()
            self.jobs_events = JobsEvents()
            self._register_jobs_listeners()
            return self.jobs_events

        def set_stations_events(self):
            self.set_socket_io_connection()
            self.stations_events = StationsEvents()
            self._register_stations_listeners()
            return self.stations_events

        def _register_machines_listeners(self):
            # Machines
            @self.on("machine/status_updated")
            def on_lz_status_update(data):
                self.lz_events.lz_status_update(
                    LzStatusUpdateEvent(lz_id=data["mid"],
                                        status=ELzStatus[data["status"]]))

            @self.on("machine/registered")
            def on_lz_registered(data):
                self.lz_events.lz_registered(
                    LzRegisteredEvent(lz_dict_to_lz(data["machine"])))

            @self.on("machine/hardware_updated")
            def on_machine_hardware_updated(data):
                self.lz_events.lz_hardware_update(
                    LzHardwareUpdateEvent(lz_dict_to_lz(data["machine"])))

        def _register_jobs_listeners(self):
            # Jobs
            @self.on("job_launcher_updated")
            def on_job_launcher_updated(data):
                self.jobs_events.job_launcher_updated(
                    JobLauncherUpdatedEvent(job_dict_to_job(data["job"])))

            @self.on("station_job_updated")
            def on_station_job_updated(data):
                self.jobs_events.station_job_updated(
                    StationJobUpdatedEvent(job_dict_to_job(data["job"])))

            @self.on("job_launcher_submitted")
            def on_job_launcher_submitted(data):
                self.jobs_events.job_launcher_submitted(
                    JobLauncherSubmittedEvent(job_dict_to_job(data["job"])))

        def _register_stations_listeners(self):
            # Stations
            @self.on("new_station")
            def on_new_station(data):
                self.stations_events.new_station(
                    NewStationEvent(station_dict_to_station(data["station"])))

            @self.on("station_admin_invite_sent")
            def on_station_admin_invite_sent(data):
                self.stations_events.station_admin_invite_sent(
                    StationAdminInviteSentEvent(data["stationid"],
                                                data["userids"]))

            @self.on("station_user_invite_received")
            def on_station_user_invite_received(data):
                self.stations_events.station_user_invite_received(
                    StationUserInviteReceivedEvent(
                        station_dict_to_station(data["station"])))

            @self.on("station_admin_invite_accepted")
            def on_station_admin_invite_accepted(data):
                self.stations_events.station_admin_invite_accepted(
                    StationAdminInviteAcceptedEvent(data["stationid"],
                                                    data["userid"]))

            @self.on("station_member_member_added")
            def on_station_member_member_added(data):
                self.stations_events.station_member_member_added(
                    StationMemberMemberEvent(data["stationid"],
                                             data["userid"]))

            @self.on("station_user_invite_accepted")
            def on_station_user_invite_accepted(data):
                self.stations_events.station_user_invite_accepted(
                    StationUserInviteAcceptedEvent(data["stationid"],
                                                   data["userid"]))

            @self.on("station_admin_invite_rejected")
            def on_station_admin_invite_rejected(data):
                self.stations_events.station_admin_invite_rejected(
                    StationAdminInviteRejectedEvent(data["stationid"],
                                                    data["userids"]))

            @self.on("station_user_invite_rejected")
            def on_station_user_invite_rejected(data):
                self.stations_events.station_user_invite_rejected(
                    StationUserInviteRejectedEvent(data["stationid"],
                                                   data["userids"]))

            @self.on("station_admin_request_received")
            def on_station_admin_request_received(data):
                self.stations_events.station_admin_request_received(
                    StationAdminRequestReceivedEvent(data["stationid"],
                                                     data["userid"]))

            @self.on("station_user_request_sent")
            def on_station_user_request_sent(data):
                self.stations_events.station_user_request_sent(
                    StationUserRequestSentEvent(data["stationid"],
                                                data["userid"]))

            @self.on("station_admin_request_accepted")
            def on_station_admin_request_accepted(data):
                self.stations_events.station_admin_request_accepted(
                    StationAdminRequestAcceptedEvent(data["stationid"],
                                                     data["userid"]))

            @self.on("station_user_request_accepted")
            def on_station_user_request_accepted(data):
                self.stations_events.station_user_request_accepted(
                    StationUserRequestAcceptedEvent(data["stationid"]))

            @self.on("station_admin_request_rejected")
            def on_station_admin_request_rejected(data):
                self.stations_events.station_admin_request_rejected(
                    StationAdminRequestRejectedEvent(data["stationid"],
                                                     data["userid"]))

            @self.on("station_user_request_rejected")
            def on_station_user_request_rejected(data):
                self.stations_events.station_user_request_rejected(
                    StationUserRequestRejectedEvent(data["stationid"]))

            @self.on("station_admin_member_removed")
            def on_station_admin_member_removed(data):
                self.stations_events.station_admin_member_removed(
                    StationAdminMemberRemovedEvent(data["stationid"],
                                                   data["userids"]))

            @self.on("station_admin_machine_removed")
            def on_station_admin_machine_removed(data):
                self.stations_events.station_admin_machine_removed(
                    StationAdminLzRemovedEvent(data["stationid"],
                                               data["mids"]))

            @self.on("station_member_member_removed")
            def on_station_member_member_removed(data):
                self.stations_events.station_member_member_removed(
                    StationMemberMemberRemovedEvent(data["stationid"],
                                                    data["userids"]))

            @self.on("station_member_machine_removed")
            def on_station_member_machine_removed(data):
                self.stations_events.station_member_machine_removed(
                    StationMemberLzRemovedEvent(data["stationid"],
                                                data["mids"]))

            @self.on("station_user_withdrawn")
            def on_station_user_withdrawn(data):
                self.stations_events.station_user_withdrawn(
                    StationUserWithdrawnEvent(data["stationid"], data["mids"]))

            @self.on("station_user_expelled")
            def on_station_user_expelled(data):
                self.stations_events.station_user_expelled(
                    StationUserExpelledEvent(data["stationid"]))

            @self.on("station_admin_destroyed")
            def on_station_admin_destroyed(data):
                self.stations_events.station_admin_destroyed(
                    StationAdminDestroyedEvent(data["stationid"]))

            @self.on("station_member_destroyed")
            def on_station_member_destroyed(data):
                self.stations_events.station_member_destroyed(
                    StationMemberDestroyedEvent(data["stationid"]))

            @self.on("station_user_invite_destroyed")
            def on_station_user_invite_destroyed(data):
                self.stations_events.station_user_invite_destroyed(
                    StationUserInviteDestroyedEvent(data["stationid"]))

            @self.on("station_user_request_destroyed")
            def on_station_user_request_destroyed(data):
                self.stations_events.station_user_request_destroyed(
                    StationUserRequestDestroyedEvent(data["stationid"]))

            @self.on("station_admin_machine_added")
            def on_station_admin_machine_added(data):
                self.stations_events.station_admin_machine_added(
                    StationAdminLzAddedEvent(data["stationid"], data["mids"]))

            @self.on("station_member_machine_added")
            def on_station_member_machine_added(data):
                self.stations_events.station_member_machine_added(
                    StationMemberLzAddedEvent(data["stationid"], data["mids"]))

            @self.on("station_admin_volume_added")
            def on_station_admin_volume_added(data):
                self.stations_events.station_admin_volume_added(
                    StationAdminVolumeAddedEvent(
                        data["stationid"],
                        [
                            volume_dict_to_volume(value)
                            for key, value in data["volumes"].items()
                        ],
                    ))

            @self.on("station_member_volume_added")
            def on_station_member_volume_added(data):
                self.stations_events.station_member_volume_added(
                    StationMemberVolumeAddedEvent(
                        data["stationid"],
                        [
                            volume_dict_to_volume(value)
                            for key, value in data["volumes"].items()
                        ],
                    ))

            @self.on("station_admin_volume_host_path_added")
            def on_station_admin_volume_host_path_added(data):
                self.stations_events.station_admin_volume_host_path_added(
                    StationAdminVolumeHostPathAddedEvent(
                        data["stationid"],
                        [
                            volume_dict_to_volume(value)
                            for key, value in data["volumes"].items()
                        ],
                    ))

            @self.on("station_member_volume_host_path_added")
            def on_station_member_volume_host_path_added(data):
                self.stations_events.station_member_volume_host_path_added(
                    StationMemberVolumeHostPathAddedEvent(
                        data["stationid"],
                        [
                            volume_dict_to_volume(value)
                            for key, value in data["volumes"].items()
                        ],
                    ))

            @self.on("station_admin_volume_host_path_removed")
            def on_station_admin_volume_host_path_removed(data):
                self.stations_events.station_admin_volume_host_path_removed(
                    StationAdminVolumeHostPathRemovedEvent(
                        data["stationid"],
                        [
                            volume_dict_to_volume(value)
                            for key, value in data["volumes"].items()
                        ],
                    ))

            @self.on("station_member_volume_host_path_removed")
            def on_station_member_volume_host_path_removed(data):
                self.stations_events.station_member_volume_host_path_removed(
                    StationMemberVolumeHostPathRemovedEvent(
                        data["stationid"],
                        [
                            volume_dict_to_volume(value)
                            for key, value in data["volumes"].items()
                        ],
                    ))

            @self.on("station_admin_volume_removed")
            def on_station_admin_volume_removed(data):
                self.stations_events.station_admin_volume_removed(
                    StationAdminVolumeRemovedEvent(data["stationid"],
                                                   data["volume_names"]))

            @self.on("station_member_volume_removed")
            def on_station_member_volume_removed(data):
                self.stations_events.station_member_volume_removed(
                    StationMemberVolumeRemovedEvent(data["stationid"],
                                                    data["volume_names"]))

            @self.on("station_admin_station_updated")
            def on_station_admin_station_updated(data):
                self.stations_events.station_admin_station_updated(
                    StationAdminStationUpdated(
                        station_dict_to_station(data["station"])))

            @self.on("station_member_station_updated")
            def on_station_member_station_updated(data):
                self.stations_events.station_member_station_updated(
                    StationMemberStationUpdated(
                        station_dict_to_station(data["station"])))

        def disconnect(self):
            if self._socket is None:
                return
            self._socket.disconnect()
