from typing import Callable, List, Optional

from ..business.objects.stations import (
    NewStationEvent,
    StationAdminDestroyedEvent,
    StationAdminInviteAcceptedEvent,
    StationAdminInviteSentEvent,
    StationAdminMachineAddedEvent,
    StationAdminMachineRemovedEvent,
    StationAdminMemberRemovedEvent,
    StationAdminRequestAcceptedEvent,
    StationAdminRequestReceivedEvent,
    StationAdminRequestRejectedEvent,
    StationAdminVolumeAddedEvent,
    StationAdminVolumeHostPathAddedEvent,
    StationAdminVolumeHostPathRemovedEvent,
    StationAdminVolumeRemovedEvent,
    StationMemberDestroyedEvent,
    StationMemberMachineAddedEvent,
    StationMemberMachineRemovedEvent,
    StationMemberMemberEvent,
    StationMemberMemberRemovedEvent,
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
from ..business.services.stations import StationsService


class StationsSdk:
    _stations_service: StationsService
    _events: StationsEvents

    def __init__(self, stations_service: StationsService, events: StationsEvents):
        self._stations_service = stations_service
        self._events = events

    def on_new_station(self, func: Callable[[NewStationEvent], None]):
        self._events.on_new_station(func)

    def on_station_admin_invite_sent(
        self, func: Callable[[StationAdminInviteSentEvent], None]
    ):
        self._events.on_station_admin_invite_sent(func)

    def on_station_user_invite_received(
        self, func: Callable[[StationUserInviteReceivedEvent], None]
    ):
        self._events.on_station_user_invite_received(func)

    def on_station_admin_invite_accepted(
        self, func: Callable[[StationAdminInviteAcceptedEvent], None]
    ):
        self._events.on_station_admin_invite_accepted(func)

    def on_station_member_member_added(
        self, func: Callable[[StationMemberMemberEvent], None]
    ):
        self._events.on_station_member_member_added(func)

    def on_station_user_invite_accepted(
        self, func: Callable[[StationUserInviteAcceptedEvent], None]
    ):
        self._events.on_station_user_invite_accepted(func)

    def on_station_admin_invite_rejected(
        self, func: Callable[[StationUserInviteRejectedEvent], None]
    ):
        self._events.on_station_admin_invite_rejected(func)

    def on_station_admin_request_received(
        self, func: Callable[[StationAdminRequestReceivedEvent], None]
    ):
        self._events.on_station_admin_request_received(func)

    def on_station_user_request_sent(
        self, func: Callable[[StationUserRequestSentEvent], None]
    ):
        self._events.on_station_user_request_sent(func)

    def on_station_admin_request_accepted(
        self, func: Callable[[StationAdminRequestAcceptedEvent], None]
    ):
        self._events.on_station_admin_request_accepted(func)

    def on_station_user_request_accepted(
        self, func: Callable[[StationUserRequestAcceptedEvent], None]
    ):
        self._events.on_station_user_request_accepted(func)

    def on_station_admin_request_rejected(
        self, func: Callable[[StationAdminRequestRejectedEvent], None]
    ):
        self._events.on_station_admin_request_rejected(func)

    def on_station_user_request_rejected(
        self, func: Callable[[StationUserRequestRejectedEvent], None]
    ):
        self._events.on_station_user_request_rejected(func)

    def on_station_admin_member_removed(
        self, func: Callable[[StationAdminMemberRemovedEvent], None]
    ):
        self._events.on_station_admin_member_removed(func)

    def on_station_admin_machine_removed(
        self, func: Callable[[StationAdminMachineRemovedEvent], None]
    ):
        self._events.on_station_admin_machine_removed(func)

    def on_station_member_member_removed(
        self, func: Callable[[StationMemberMemberRemovedEvent], None]
    ):
        self._events.on_station_member_member_removed(func)

    def on_station_member_machine_removed(
        self, func: Callable[[StationMemberMachineRemovedEvent], None]
    ):
        self._events.on_station_member_machine_removed(func)

    def on_station_user_withdrawn(
        self, func: Callable[[StationUserWithdrawnEvent], None]
    ):
        self._events.on_station_user_withdrawn(func)

    def on_station_user_expelled(
        self, func: Callable[[StationUserExpelledEvent], None]
    ):
        self._events.on_station_user_expelled(func)

    def on_station_admin_destroyed(
        self, func: Callable[[StationAdminDestroyedEvent], None]
    ):
        self._events.on_station_admin_destroyed(func)

    def on_station_member_destroyed(
        self, func: Callable[[StationMemberDestroyedEvent], None]
    ):
        self._events.on_station_member_destroyed(func)

    def on_station_user_invite_destroyed(
        self, func: Callable[[StationUserInviteDestroyedEvent], None]
    ):
        self._events.on_station_user_invite_destroyed(func)

    def on_station_user_request_destroyed(
        self, func: Callable[[StationUserRequestDestroyedEvent], None]
    ):
        self._events.on_station_user_request_destroyed(func)

    def on_station_admin_machine_added(
        self, func: Callable[[StationAdminMachineAddedEvent], None]
    ):
        self._events.on_station_admin_machine_added(func)

    def on_station_member_machine_added(
        self, func: Callable[[StationMemberMachineAddedEvent], None]
    ):
        self._events.on_station_member_machine_added(func)

    def on_station_admin_volume_added(
        self, func: Callable[[StationAdminVolumeAddedEvent], None]
    ):
        self._events.on_station_admin_volume_added(func)

    def on_station_member_volume_added(
        self, func: Callable[[StationMemberVolumeAddedEvent], None]
    ):
        self._events.on_station_member_volume_added(func)

    def on_station_admin_volume_host_path_added(
        self, func: Callable[[StationAdminVolumeHostPathAddedEvent], None]
    ):
        self._events.on_station_admin_volume_host_path_added(func)

    def on_station_member_volume_host_path_added(
        self, func: Callable[[StationMemberVolumeHostPathAddedEvent], None]
    ):
        self._events.on_station_member_volume_host_path_added(func)

    def on_station_admin_volume_host_path_removed(
        self, func: Callable[[StationAdminVolumeHostPathRemovedEvent], None]
    ):
        self._events.on_station_admin_volume_host_path_removed(func)

    def on_station_member_volume_host_path_removed(
        self, func: Callable[[StationMemberVolumeHostPathRemovedEvent], None]
    ):
        self._events.on_station_member_volume_host_path_removed(func)

    def on_station_admin_volume_removed(
        self, func: Callable[[StationAdminVolumeRemovedEvent], None]
    ):
        self._events.on_station_admin_volume_removed(func)

    def on_station_member_volume_removed(
        self, func: Callable[[StationMemberVolumeRemovedEvent], None]
    ):
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

    def create_station(self, name: str, usernames: List[str], description: str):
        return self._stations_service.create_station(name, usernames, description)

    def invite_to_station(self, station_id: str, userids: List[str]):
        return self._stations_service.invite_to_station(station_id, userids)

    def accept_station_invite(self, station_id: str):
        return self._stations_service.accept_station_invite(station_id)

    def reject_station_invite(self, station_id: str):
        return self._stations_service.reject_station_invite(station_id)

    def request_to_join(self, station_id: str):
        return self._stations_service.request_to_join(station_id)

    def approve_request_to_join(self, station_id: str, userids: List[str]):
        return self._stations_service.approve_request_to_join(station_id, userids)

    def reject_request_to_join(self, station_id: str, userids: List[str]):
        return self._stations_service.reject_request_to_join(station_id, userids)

    def leave_station(self, station_id: str):
        return self._stations_service.leave_station(station_id)

    def remove_member_from_station(self, station_id: str, userid: str):
        return self._stations_service.remove_member_from_station(station_id, userid)

    def delete_station(self, station_id: str):
        return self._stations_service.delete_station(station_id)

    def add_machines_to_station(self, station_id: str, mids: List[str]):
        return self._stations_service.add_machines_to_station(station_id, mids)

    def remove_machines_from_station(self, station_id: str, mids: List[str]):
        return self._stations_service.remove_machines_from_station(station_id, mids)

    def add_volumes_to_station(
        self, station_id: str, name: str, mount_point: str, access: str
    ):
        return self._stations_service.add_volumes_to_station(
            station_id, name, mount_point, access
        )

    def add_host_path_to_volume(
        self, station_id: str, volume_id: str, mid: str, host_path: str
    ):
        return self._stations_service.add_host_path_to_volume(
            station_id, volume_id, mid, host_path
        )

    def delete_host_path_from_volume(
        self, station_id: str, volume_id: str, host_path_id: str
    ):
        return self._stations_service.delete_host_path_from_volume(
            station_id, volume_id, host_path_id
        )

    def remove_volume_from_station(self, station_id: str, volume_id):
        return self._stations_service.remove_volume_from_station(station_id, volume_id)
