from typing import Callable, List, Optional

from ..business.objects.stations import (
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
from ..business.services.stations import StationsService


class StationsSdk:
    _stations_service: StationsService
    _events: StationsEvents

    def __init__(self, stations_service: StationsService, events: StationsEvents):
        self._stations_service = stations_service
        self._events = events

    def on_new_station(self, func: Callable[[NewStationEvent], None]):
        """
        Callback will execute upon a creation of a new station

        :param func: Callback
        :return: None
        """
        self._events.on_new_station(func)

    def on_station_admin_invite_sent(
        self, func: Callable[[StationAdminInviteSentEvent], None]
    ):
        """
        Callback will execute upon an invite sent
        Emitted to admin of a station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_invite_sent(func)

    def on_station_user_invite_received(
        self, func: Callable[[StationUserInviteReceivedEvent], None]
    ):
        """
        Callback will execute upon a user receiving an invite to a station
        Emitted to the user that receives the invite

        :param func: Callback
        :return: None
        """
        self._events.on_station_user_invite_received(func)

    def on_station_admin_invite_accepted(
        self, func: Callable[[StationAdminInviteAcceptedEvent], None]
    ):
        """
        Callback will execute upon an invite to a station being accepted
        Emitted to admin of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_invite_accepted(func)

    def on_station_member_member_added(
        self, func: Callable[[StationMemberMemberEvent], None]
    ):
        """
        Callback will execute upon a member has been added (request has been approved or invitation has been accepted)
        Emitted to all members of a station

        :param func: Callback
        :return: None
        """
        self._events.on_station_member_member_added(func)

    def on_station_user_invite_accepted(
        self, func: Callable[[StationUserInviteAcceptedEvent], None]
    ):
        """
        Callback will execute upon a user accepting an invite to a station
        Emitted to user who has accepted the invitation

        :param func: Callback
        :return: None
        """
        self._events.on_station_user_invite_accepted(func)

    def on_station_admin_invite_rejected(
        self, func: Callable[[StationUserInviteRejectedEvent], None]
    ):
        """
        Callback will execute when an invite to a station has been rejected
        Emitted to admin of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_invite_rejected(func)

    def on_station_admin_request_received(
        self, func: Callable[[StationAdminRequestReceivedEvent], None]
    ):
        """
        Callback will execute when a request to join the station has been received
        Emitted to admin of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_request_received(func)

    def on_station_user_request_sent(
        self, func: Callable[[StationUserRequestSentEvent], None]
    ):
        """
        Callback will execute when a request to join the station has been sent
        Emitted to user requesting to join the station

        :param func: Callback
        :return: None
        """
        self._events.on_station_user_request_sent(func)

    def on_station_admin_request_accepted(
        self, func: Callable[[StationAdminRequestAcceptedEvent], None]
    ):
        """
        Callback will execute when a request to join a station has been accepted
        Emitted to admin of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_request_accepted(func)

    def on_station_user_request_accepted(
        self, func: Callable[[StationUserRequestAcceptedEvent], None]
    ):
        """
        Callback will execute when a request to join a station has been accepted
        Emitted to user who sent the request

        :param func: Callback
        :return: None
        """
        self._events.on_station_user_request_accepted(func)

    def on_station_admin_request_rejected(
        self, func: Callable[[StationAdminRequestRejectedEvent], None]
    ):
        """
        Callback will execute when a request to join a station has been rejected
        Emitted to admin of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_request_rejected(func)

    def on_station_user_request_rejected(
        self, func: Callable[[StationUserRequestRejectedEvent], None]
    ):
        """
        Callback will execute when a request to join a station has been rejected
        Emitted to user who sent the request

        :param func: Callback
        :return: None
        """
        self._events.on_station_user_request_rejected(func)

    def on_station_admin_member_removed(
        self, func: Callable[[StationAdminMemberRemovedEvent], None]
    ):
        """
        Callback will execute when a member has been removed from a station
        Emitted to admin of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_member_removed(func)

    def on_station_admin_machine_removed(
        self, func: Callable[[StationAdminMachineRemovedEvent], None]
    ):
        """
        Callback will execute when a machine has been removed from a station
        Emitted to admin of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_machine_removed(func)

    def on_station_member_member_removed(
        self, func: Callable[[StationMemberMemberRemovedEvent], None]
    ):
        """
        Callback will execute when a member has been removed from a station
        Emitted to members of a station

        :param func: Callback
        :return: None
        """
        self._events.on_station_member_member_removed(func)

    def on_station_member_machine_removed(
        self, func: Callable[[StationMemberMachineRemovedEvent], None]
    ):
        """
        Callback will execute when a machine has been removed from a station
        Emitted to members of a station

        :param func: Callback
        :return: None
        """
        self._events.on_station_member_machine_removed(func)

    def on_station_user_withdrawn(
        self, func: Callable[[StationUserWithdrawnEvent], None]
    ):
        """
        Callback will execute when a user has withdrawn from the station
        Emitted to user that is withdrawing

        :param func: Callback
        :return: None
        """
        self._events.on_station_user_withdrawn(func)

    def on_station_user_expelled(
        self, func: Callable[[StationUserExpelledEvent], None]
    ):
        """
        Callback will execute when a user has been expelled from the station
        Emitted to user that has been expelled

        :param func: Callback
        :return: None
        """
        self._events.on_station_user_expelled(func)

    def on_station_admin_destroyed(
        self, func: Callable[[StationAdminDestroyedEvent], None]
    ):
        """
        Callback will execute when a station has been destroyed
        Emitted to admin of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_destroyed(func)

    def on_station_member_destroyed(
        self, func: Callable[[StationMemberDestroyedEvent], None]
    ):
        """
        Callback will execute when a station has been destroyed
        Emitted to member of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_member_destroyed(func)

    def on_station_user_invite_destroyed(
        self, func: Callable[[StationUserInviteDestroyedEvent], None]
    ):
        """
        Callback will execute when a station has been destroyed
        Emitted to anyone who received an invite to join the station

        :param func: Callback
        :return: None
        """
        self._events.on_station_user_invite_destroyed(func)

    def on_station_user_request_destroyed(
        self, func: Callable[[StationUserRequestDestroyedEvent], None]
    ):
        """
        Callback will execute when a station has been destroyed
        Emitted to anyone who sent a request to join to the station

        :param func: Callback
        :return: None
        """
        self._events.on_station_user_request_destroyed(func)

    def on_station_admin_machine_added(
        self, func: Callable[[StationAdminMachineAddedEvent], None]
    ):
        """
        Callback will execute when a machine has been added to the station
        Emitted to admin of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_machine_added(func)

    def on_station_member_machine_added(
        self, func: Callable[[StationMemberMachineAddedEvent], None]
    ):
        """
        Callback will execute when a machine has been added to the station
        Emitted to members of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_member_machine_added(func)

    def on_station_admin_volume_added(
        self, func: Callable[[StationAdminVolumeAddedEvent], None]
    ):
        """
        Callback will execute when a volume has been added to the station
        Emitted to admin of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_volume_added(func)

    def on_station_member_volume_added(
        self, func: Callable[[StationMemberVolumeAddedEvent], None]
    ):
        """
        Callback will execute when a volume has been added to the station
        Emitted to members of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_member_volume_added(func)

    def on_station_admin_volume_host_path_added(
        self, func: Callable[[StationAdminVolumeHostPathAddedEvent], None]
    ):
        """
        Callback will execute when a volume host path has been added
        Emitted to admin of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_volume_host_path_added(func)

    def on_station_member_volume_host_path_added(
        self, func: Callable[[StationMemberVolumeHostPathAddedEvent], None]
    ):
        """
        Callback will execute when a volume host path has been added
        Emitted to members of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_member_volume_host_path_added(func)

    def on_station_admin_volume_host_path_removed(
        self, func: Callable[[StationAdminVolumeHostPathRemovedEvent], None]
    ):
        """
        Callback will execute when a volume host path has been removed
        Emitted to admin of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_volume_host_path_removed(func)

    def on_station_member_volume_host_path_removed(
        self, func: Callable[[StationMemberVolumeHostPathRemovedEvent], None]
    ):
        """
        Callback will execute when a volume host path has been removed
        Emitted to members of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_member_volume_host_path_removed(func)

    def on_station_admin_volume_removed(
        self, func: Callable[[StationAdminVolumeRemovedEvent], None]
    ):
        """
        Callback will execute when a volume has been removed
        Emitted to admin of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_admin_volume_removed(func)

    def on_station_member_volume_removed(
        self, func: Callable[[StationMemberVolumeRemovedEvent], None]
    ):
        """
        Callback will execute when a volume has been removed
        Emitted to members of station

        :param func: Callback
        :return: None
        """
        self._events.on_station_member_volume_removed(func)

    def list_stations(
        self,
        stationids: Optional[List[str]] = None,
        names: Optional[List[str]] = None,
        mids: Optional[List[str]] = None,
        user_roles: Optional[List[str]] = None,
        volumeids: Optional[List[str]] = None,
        descriptions: Optional[List[str]] = None,
        page: Optional[int] = 1,
        items: Optional[int] = 25,
    ):
        """
        List of your Galileo stations

        :param stationids: Filter based on station ids
        :param names: Filter based on names
        :param mids: Filter based on mids
        :param user_roles: Filter based on user roles
        :param volumeids: Filter based on volumeids
        :param descriptions: Filter based on descriptions
        :param page: Page #
        :param items: Items per page
        :return: {'stations': [Stations]}
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

    def create_station(
        self, name: str, description: str, userids: Optional[List[str]] = None
    ):
        """
        Create a new station

        :param name: name of station
        :param userids: list of members's user ids to invite
        :param description: description of station
        :return: {"station": Station}
        """
        return self._stations_service.create_station(name, description, userids)

    def invite_to_station(self, station_id: str, userids: List[str]):
        """
        Invite user(s) to a station

        :param userids: list of user's ids
        :param station_id: station's id
        :return: boolean
        """
        return self._stations_service.invite_to_station(station_id, userids)

    def accept_station_invite(self, station_id: str):
        """
        Accept an invitation to join a station

        :param station_id: station's id
        :return: boolean
        """
        return self._stations_service.accept_station_invite(station_id)

    def reject_station_invite(self, station_id: str):
        """
        Reject an invitation to join a station

        :param station_id: station's id
        :return: boolean
        """
        return self._stations_service.reject_station_invite(station_id)

    def request_to_join(self, station_id: str):
        """
        Request to join a station

        :param station_id: station's id
        :return: boolean, True for success
        """
        return self._stations_service.request_to_join(station_id)

    def approve_request_to_join(self, station_id: str, userids: List[str]):
        """
        Admins and owners can approve members to join a station

        :param station_id: station's id
        :param userids: list of user ids that will be approved
        :return: boolean
        """
        return self._stations_service.approve_request_to_join(station_id, userids)

    def reject_request_to_join(self, station_id: str, userids: List[str]):
        """
        Admins and owners can reject members that want to join a station

        :param station_id: station's id
        :param userids: list of user ids that will be rejected
        :return: boolean
        """
        return self._stations_service.reject_request_to_join(station_id, userids)

    def leave_station(self, station_id: str):
        """
        Leave a station as a member

        :param station_id: station's id
        :return: boolean, True for success
        """
        return self._stations_service.leave_station(station_id)

    def remove_member_from_station(self, station_id: str, userid: str):
        """
        Remove a member from a station

        :param station_id: station's id
        :param userid: the id of the user you want to remove
        :return: boolean
        """
        return self._stations_service.remove_member_from_station(station_id, userid)

    def delete_station(self, station_id: str):
        """
        Permanently delete a station

        :param station_id: station's id
        :return: boolean
        """
        return self._stations_service.delete_station(station_id)

    def add_machines_to_station(self, station_id: str, mids: List[str]):
        """
        Add machines to a station

        :param station_id: station's id
        :param mids: list of machine ids that will be added
        :return: boolean
        """
        return self._stations_service.add_machines_to_station(station_id, mids)

    def remove_machines_from_station(self, station_id: str, mids: List[str]):
        """
        Remove machines from a station

        :param station_id: station's id
        :param mids: list of machine ids that will be added
        :return: boolean
        """
        return self._stations_service.remove_machines_from_station(station_id, mids)

    def add_volumes_to_station(
        self, station_id: str, name: str, mount_point: str, access: str
    ):
        """
        Add volumes to a station

        :param station_id: station's id
        :param name: volume name
        :param mount_point: directory path from inside the container
        :param access: read/write access: either 'r' or 'rw'
        :return: {"volumes": Volume}
        """
        return self._stations_service.add_volumes_to_station(
            station_id, name, mount_point, access
        )

    def add_host_path_to_volume(
        self, station_id: str, volume_id: str, mid: str, host_path: str
    ):
        """
        Add host path to volume before running a job
        Host path is where the landing zone will store the results of a job

        :param station_id: station's id
        :param volume_id: volume's id
        :param mid: machine id
        :param host_path: directory path for landing zone
        :return: {"volume": Volume}
        """
        return self._stations_service.add_host_path_to_volume(
            station_id, volume_id, mid, host_path
        )

    def delete_host_path_from_volume(
        self, station_id: str, volume_id: str, host_path_id: str
    ):
        """
        Remove a host path
        Host path is where the landing zone will store the results of a job

        :param station_id: station's id
        :param volume_id: volume's id
        :param host_path_id: host path id
        :return: boolean
        """
        return self._stations_service.delete_host_path_from_volume(
            station_id, volume_id, host_path_id
        )

    def remove_volume_from_station(self, station_id: str, volume_id):
        """
        Remove a volume from station

        :param station_id: station's id
        :param volume_id: volume's id
        :return: boolean
        """
        return self._stations_service.remove_volume_from_station(station_id, volume_id)
