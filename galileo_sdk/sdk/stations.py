class StationsSdk:
    def __init__(self, stations_service, events=None):
        self._stations_service = stations_service
        self._events = events

    def on_new_station(self, func):
        """
        Callback will execute upon a creation of a new station

        :param func: Callable[[NewStationEvent], None]
        :return: None
        """
        self._events.on_new_station(func)

    def on_station_admin_invite_sent(self, func):
        """
        Callback will execute upon an invite sent
        Emitted to admin of a station

        :param func: Callable[[StationAdminInviteSentEvent], None]
        :return: None
        """
        self._events.on_station_admin_invite_sent(func)

    def on_station_user_invite_received(self, func):
        """
        Callback will execute upon a user receiving an invite to a station
        Emitted to the user that receives the invite

        :param func: Callable[[StationUserInviteReceivedEvent], None]
        :return: None
        """
        self._events.on_station_user_invite_received(func)

    def on_station_admin_invite_accepted(self, func):
        """
        Callback will execute upon an invite to a station being accepted
        Emitted to admin of station

        :param func: Callable[[StationAdminInviteAcceptedEvent], None]
        :return: None
        """
        self._events.on_station_admin_invite_accepted(func)

    def on_station_member_member_added(self, func):
        """
        Callback will execute upon a member has been added (request has been approved or invitation has been accepted)
        Emitted to all members of a station

        :param func: Callable[[StationMemberMemberEvent], None]
        :return: None
        """
        self._events.on_station_member_member_added(func)

    def on_station_user_invite_accepted(self, func):
        """
        Callback will execute upon a user accepting an invite to a station
        Emitted to user who has accepted the invitation

        :param func: Callable[[StationUserInviteAcceptedEvent], None]
        :return: None
        """
        self._events.on_station_user_invite_accepted(func)

    def on_station_admin_invite_rejected(self, func):
        """
        Callback will execute when an invite to a station has been rejected
        Emitted to admin of station

        :param func: Callable[[StationAdminInviteRejectedEvent], None]
        :return: None
        """
        self._events.on_station_admin_invite_rejected(func)

    def on_station_user_invite_rejected(self, func):
        """
        Callback will execute when an invite to a station has been rejected
        Emitted to admin of station

        :param func: Callable[[StationUserInviteRejectedEvent], None]
        :return: None
        """
        self._events.on_station_user_invite_rejected(func)

    def on_station_admin_request_received(self, func):
        """
        Callback will execute when a request to join the station has been received
        Emitted to admin of station

        :param func: Callable[[StationAdminRequestReceivedEvent], None]
        :return: None
        """
        self._events.on_station_admin_request_received(func)

    def on_station_user_request_sent(self, func):
        """
        Callback will execute when a request to join the station has been sent
        Emitted to user requesting to join the station

        :param func: Callable[[StationUserRequestSentEvent], None]
        :return: None
        """
        self._events.on_station_user_request_sent(func)

    def on_station_admin_request_accepted(self, func):
        """
        Callback will execute when a request to join a station has been accepted
        Emitted to admin of station

        :param func: Callable[[StationAdminRequestAcceptedEvent], None]
        :return: None
        """
        self._events.on_station_admin_request_accepted(func)

    def on_station_user_request_accepted(self, func):
        """
        Callback will execute when a request to join a station has been accepted
        Emitted to user who sent the request

        :param func: Callable[[StationUserRequestAcceptedEvent], None]
        :return: None
        """
        self._events.on_station_user_request_accepted(func)

    def on_station_admin_request_rejected(
        self, func,
    ):
        """
        Callback will execute when a request to join a station has been rejected
        Emitted to admin of station

        :param func: Callable[[StationAdminRequestRejectedEvent], None]
        :return: None
        """
        self._events.on_station_admin_request_rejected(func)

    def on_station_user_request_rejected(
        self, func,
    ):
        """
        Callback will execute when a request to join a station has been rejected
        Emitted to user who sent the request

        :param func: Callable[[StationUserRequestRejectedEvent], None]
        :return: None
        """
        self._events.on_station_user_request_rejected(func)

    def on_station_admin_member_removed(
        self, func,
    ):
        """
        Callback will execute when a member has been removed from a station
        Emitted to admin of station

        :param func: Callable[[StationAdminMemberRemovedEvent], None]
        :return: None
        """
        self._events.on_station_admin_member_removed(func)

    def on_station_admin_machine_removed(
        self, func,
    ):
        """
        Callback will execute when a machine has been removed from a station
        Emitted to admin of station

        :param func: Callable[[StationAdminMachineRemovedEvent], None]
        :return: None
        """
        self._events.on_station_admin_machine_removed(func)

    def on_station_member_member_removed(
        self, func,
    ):
        """
        Callback will execute when a member has been removed from a station
        Emitted to members of a station

        :param func: Callable[[StationMemberMemberRemovedEvent], None]
        :return: None
        """
        self._events.on_station_member_member_removed(func)

    def on_station_member_machine_removed(
        self, func,
    ):
        """
        Callback will execute when a machine has been removed from a station
        Emitted to members of a station

        :param func: Callable[[StationMemberMachineRemovedEvent], None]
        :return: None
        """
        self._events.on_station_member_machine_removed(func)

    def on_station_user_withdrawn(
        self, func,
    ):
        """
        Callback will execute when a user has withdrawn from the station
        Emitted to user that is withdrawing

        :param func: Callable[[StationUserWithdrawnEvent], None]
        :return: None
        """
        self._events.on_station_user_withdrawn(func)

    def on_station_user_expelled(
        self, func,
    ):
        """
        Callback will execute when a user has been expelled from the station
        Emitted to user that has been expelled

        :param func: Callable[[StationUserExpelledEvent], None]
        :return: None
        """
        self._events.on_station_user_expelled(func)

    def on_station_admin_destroyed(
        self, func,
    ):
        """
        Callback will execute when a station has been destroyed
        Emitted to admin of station

        :param func: Callable[[StationAdminDestroyedEvent], None]
        :return: None
        """
        self._events.on_station_admin_destroyed(func)

    def on_station_member_destroyed(
        self, func,
    ):
        """
        Callback will execute when a station has been destroyed
        Emitted to member of station

        :param func: Callable[[StationMemberDestroyedEvent], None]
        :return: None
        """
        self._events.on_station_member_destroyed(func)

    def on_station_user_invite_destroyed(
        self, func,
    ):
        """
        Callback will execute when a station has been destroyed
        Emitted to anyone who received an invite to join the station

        :param func: Callable[[StationUserInviteDestroyedEvent], None]
        :return: None
        """
        self._events.on_station_user_invite_destroyed(func)

    def on_station_user_request_destroyed(
        self, func,
    ):
        """
        Callback will execute when a station has been destroyed
        Emitted to anyone who sent a request to join to the station

        :param func: Callable[[StationUserRequestDestroyedEvent], None]
        :return: None
        """
        self._events.on_station_user_request_destroyed(func)

    def on_station_admin_machine_added(
        self, func,
    ):
        """
        Callback will execute when a machine has been added to the station
        Emitted to admin of station

        :param func: Callable[[StationAdminMachineAddedEvent], None]
        :return: None
        """
        self._events.on_station_admin_machine_added(func)

    def on_station_member_machine_added(
        self, func,
    ):
        """
        Callback will execute when a machine has been added to the station
        Emitted to members of station

        :param func: Callable[[StationMemberMachineAddedEvent], None]
        :return: None
        """
        self._events.on_station_member_machine_added(func)

    def on_station_admin_volume_added(self, func):
        """
        Callback will execute when a volume has been added to the station
        Emitted to admin of station

        :param func: Callable[[StationAdminVolumeAddedEvent], None]
        :return: None
        """
        self._events.on_station_admin_volume_added(func)

    def on_station_member_volume_added(
        self, func,
    ):
        """
        Callback will execute when a volume has been added to the station
        Emitted to members of station

        :param func: Callable[[StationMemberVolumeAddedEvent], None]
        :return: None
        """
        self._events.on_station_member_volume_added(func)

    def on_station_admin_volume_host_path_added(
        self, func,
    ):
        """
        Callback will execute when a volume host path has been added
        Emitted to admin of station

        :param func: Callable[[StationAdminVolumeHostPathAddedEvent], None]
        :return: None
        """
        self._events.on_station_admin_volume_host_path_added(func)

    def on_station_member_volume_host_path_added(
        self, func,
    ):
        """
        Callback will execute when a volume host path has been added
        Emitted to members of station

        :param func: Callable[[StationMemberVolumeHostPathAddedEvent], None]
        :return: None
        """
        self._events.on_station_member_volume_host_path_added(func)

    def on_station_admin_volume_host_path_removed(
        self, func,
    ):
        """
        Callback will execute when a volume host path has been removed
        Emitted to admin of station

        :param func: Callable[[StationAdminVolumeHostPathRemovedEvent], None]
        :return: None
        """
        self._events.on_station_admin_volume_host_path_removed(func)

    def on_station_member_volume_host_path_removed(
        self, func,
    ):
        """
        Callback will execute when a volume host path has been removed
        Emitted to members of station

        :param func: Callable[[StationMemberVolumeHostPathRemovedEvent], None]
        :return: None
        """
        self._events.on_station_member_volume_host_path_removed(func)

    def on_station_admin_volume_removed(
        self, func,
    ):
        """
        Callback will execute when a volume has been removed
        Emitted to admin of station

        :param func: Callable[[StationAdminVolumeRemovedEvent], None]
        :return: None
        """
        self._events.on_station_admin_volume_removed(func)

    def on_station_member_volume_removed(
        self, func,
    ):
        """
        Callback will execute when a volume has been removed
        Emitted to members of station

        :param func: Callable[[StationMemberVolumeRemovedEvent], None]
        :return: None
        """
        self._events.on_station_member_volume_removed(func)

    def on_station_admin_station_updated(
        self, func,
    ):
        """
        Callback will execute when a station has been updated
        Emitted to admin

        :param func: Callable[[StationAdminStationUpdated], None]
        :return: None
        """
        self._events.on_station_admin_station_updated(func)

    def on_station_member_station_updated(
        self, func,
    ):
        """
        Callback will execute when a station has been updated
        Emitted to members of the station

        :param func: Callable[[StationMemberStationUpdated], None]
        :return: None
        """
        self._events.on_station_member_station_updated(func)

    def list_stations(
        self,
        stationids=None,
        names=None,
        mids=None,
        user_roles=None,
        volumeids=None,
        descriptions=None,
        page=1,
        items=25,
    ):
        """
        List of your Galileo stations

        :param stationids: Optional[List[str]]: Filter based on station ids
        :param names: Optional[List[str]]: Filter based on names
        :param mids: Optional[List[str]]: Filter based on mids
        :param user_roles: Optional[List[str]]: Filter based on user roles
        :param volumeids: Optional[List[str]]: Filter based on volumeids
        :param descriptions: Optional[List[str]]: Filter based on descriptions
        :param page: Optional[int]: Page #
        :param items: Optional[int]: Items per page
        :return: List[Station]
        """
        return self._stations_service.list_stations(
            stationids=stationids,
            names=names,
            mids=mids,
            user_roles=user_roles,
            volumeids=volumeids,
            descriptions=descriptions,
            page=page,
            items=items,
        )

    def create_station(self, name, description="", userids=None):
        """
        Create a new station

        :param name: str: name of station
        :param userids: List[str]: list of members's user ids to invite
        :param description: str: description of station
        :return: Station
        """
        return self._stations_service.create_station(name, description, userids)

    def invite_to_station(self, station_id, userids):
        """
        Invite user(s) to a station

        :param userids: List[str]: list of user's ids to invite
        :param station_id: str
        :return: boolean
        """
        return self._stations_service.invite_to_station(station_id, userids)

    def accept_station_invite(self, station_id):
        """
        Accept an invitation to join a station

        :param station_id: str
        :return: boolean
        """
        return self._stations_service.accept_station_invite(station_id)

    def reject_station_invite(self, station_id):
        """
        Reject an invitation to join a station

        :param station_id: str
        :return: boolean
        """
        return self._stations_service.reject_station_invite(station_id)

    def request_to_join(self, station_id):
        """
        Request to join a station

        :param station_id: str
        :return: boolean
        """
        return self._stations_service.request_to_join(station_id)

    def approve_request_to_join(self, station_id, userids):
        """
        Admins and owners can approve members to join a station

        :param station_id: str
        :param userids: List[str]: list of user ids that will be approved
        :return: boolean
        """
        return self._stations_service.approve_request_to_join(station_id, userids)

    def reject_request_to_join(self, station_id, userids):
        """
        Admins and owners can reject members that want to join a station

        :param station_id: str
        :param userids: List[str]: list of user ids that will be rejected
        :return: boolean
        """
        return self._stations_service.reject_request_to_join(station_id, userids)

    def leave_station(self, station_id):
        """
        Leave a station as a member

        :param station_id: str
        :return: boolean
        """
        return self._stations_service.leave_station(station_id)

    def remove_member_from_station(self, station_id, userid):
        """
        Remove a member from a station

        :param station_id: str
        :param userid: List[str]: the id of the user you want to remove
        :return: boolean
        """
        return self._stations_service.remove_member_from_station(station_id, userid)

    def delete_station(self, station_id):
        """
        Permanently delete a station

        :param station_id: str
        :return: boolean
        """
        return self._stations_service.delete_station(station_id)

    def add_machines_to_station(self, station_id, mids):
        """
        Add machines to a station

        :param station_id: str
        :param mids: List[str]: list of machine ids that will be added
        :return: boolean
        """
        return self._stations_service.add_machines_to_station(station_id, mids)

    def remove_machines_from_station(self, station_id, mids):
        """
        Remove machines from a station

        :param station_id: str
        :param mids: List[str]: list of machine ids that will be added
        :return: boolean
        """
        return self._stations_service.remove_machines_from_station(station_id, mids)

    def add_volumes_to_station(self, station_id, name, mount_point, access):
        """
        Add volumes to a station

        :param station_id: str
        :param name: str: volume name
        :param mount_point: str: directory path from inside the container
        :param access: EVolumeAccess: read/write access: either 'r' or 'rw'
        :return: Volume
        """
        return self._stations_service.add_volumes_to_station(
            station_id, name, mount_point, access
        )

    def add_host_path_to_volume(self, station_id, volume_id, mid, host_path):
        """
        Add host path to volume before running a job
        Host path is where the landing zone will store the results of a job

        :param station_id: str
        :param volume_id: tr
        :param mid: str: machine id
        :param host_path: str: directory path for landing zone
        :return: Volume
        """
        return self._stations_service.add_host_path_to_volume(
            station_id, volume_id, mid, host_path
        )

    def delete_host_path_from_volume(self, station_id, volume_id, host_path_id):
        """
        Remove a host path
        Host path is where the landing zone will store the results of a job

        :param station_id: str
        :param volume_id: srt
        :param host_path_id: str
        :return: boolean
        """
        return self._stations_service.delete_host_path_from_volume(
            station_id, volume_id, host_path_id
        )

    def remove_volume_from_station(self, station_id, volume_id):
        """
        Remove a volume from station

        :param station_id: str
        :param volume_id: str
        :return: boolean
        """
        return self._stations_service.remove_volume_from_station(station_id, volume_id)

    def update_station(self, request):
        return self._stations_service.update_station(request)
