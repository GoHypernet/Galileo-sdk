import enum
from typing import Callable, List, Optional

from ...business.objects.event import EventEmitter


class UpdateStationRequest:
    def __init__(
        self,
        station_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self.station_id = station_id
        self.name = name
        self.description = description


class EVolumeAccess(enum.Enum):
    READ = "r"
    READWRITE = "rw"


class VolumeHostPath:
    def __init__(self, volumehostpathid: str, mid: str, host_path: str):
        self.volumehostpathid = volumehostpathid
        self.mid = mid
        self.host_path = host_path


class Volume:
    def __init__(
        self,
        stationid: str,
        name: str,
        mount_point: str,
        access: EVolumeAccess,
        host_paths: List[VolumeHostPath],
        volumeid: str,
    ):

        self.volumeid = volumeid
        self.stationid = stationid
        self.name = name

        self.mount_point = mount_point
        self.access = access

        self.host_paths = host_paths


class EStationUserRole(enum.Enum):
    OWNER = 0
    ADMIN = 1
    MEMBER = 2
    PENDING = 3
    INVITED = 4
    BLOCKED = 5


class StationUser:
    def __init__(self, stationuserid: str, userid: str, status: EStationUserRole):
        self.stationuserid = stationuserid
        self.userid = userid
        self.status = status


class Station:
    def __init__(
        self,
        stationid: str,
        name: str,
        description: str,
        users: List[StationUser],
        machine_ids: Optional[List[str]] = None,
        volumes: Optional[List[Volume]] = None,
    ):
        self.stationid = stationid
        self.name = name
        self.description = description
        self.users = users
        self.mids = machine_ids
        self.volumes = volumes


class NewStationEvent:
    def __init__(self, station: Station):
        self.station = station


class StationAdminInviteSentEvent:
    def __init__(self, stationid: str, userids: List[str]):
        self.stationid: str = stationid
        self.userids: List[str] = userids


class StationUserInviteReceivedEvent:
    def __init__(self, station):
        self.station = station


class StationAdminInviteAcceptedEvent:
    def __init__(self, stationid: str, userid: str):
        self.stationid: str = stationid
        self.userid: str = userid


class StationMemberMemberEvent:
    def __init__(self, stationid: str, userid: str):
        self.stationid: str = stationid
        self.userid: str = userid


class StationUserInviteAcceptedEvent:
    def __init__(self, stationid: str, userid: str):
        self.stationid: str = stationid
        self.userid: str = userid


class StationAdminInviteRejectedEvent:
    def __init__(self, stationid: str, userids: List[str]):
        self.stationid: str = stationid
        self.userids: List[str] = userids


class StationUserInviteRejectedEvent:
    def __init__(self, stationid: str, userids: List[str]):
        self.stationid: str = stationid
        self.userids: List[str] = userids


class StationAdminRequestReceivedEvent:
    def __init__(self, stationid: str, userid: str):
        self.stationid: str = stationid
        self.userid: str = userid


class StationUserRequestSentEvent:
    def __init__(self, stationid: str, userid: str):
        self.stationid: str = stationid
        self.userid: str = userid


class StationAdminRequestAcceptedEvent:
    def __init__(self, stationid: str, userid: str):
        self.stationid: str = stationid
        self.userid: str = userid


class StationUserRequestAcceptedEvent:
    def __init__(self, stationid: str):
        self.stationid: str = stationid


class StationAdminRequestRejectedEvent:
    def __init__(self, stationid: str, userid: str):
        self.stationid: str = stationid
        self.userid: str = userid


class StationUserRequestRejectedEvent:
    def __init__(self, stationid: str):
        self.stationid: str = stationid


class StationAdminMemberRemovedEvent:
    def __init__(self, stationid: str, userids: List[str]):
        self.stationid: str = stationid
        self.userids: List[str] = userids


class StationAdminMachineRemovedEvent:
    def __init__(self, stationid: str, mids: List[str]):
        self.stationid: str = stationid
        self.mids: List[str] = mids


class StationMemberMemberRemovedEvent:
    def __init__(self, stationid: str, userid: str):
        self.stationid: str = stationid
        self.userid: str = userid


class StationMemberMachineRemovedEvent:
    def __init__(self, stationid: str, mids: List[str]):
        self.stationid: str = stationid
        self.mids: List[str] = mids


class StationUserWithdrawnEvent:
    def __init__(self, stationid: str, mids: List[str]):
        self.stationid: str = stationid
        self.mids: List[str] = mids


class StationUserExpelledEvent:
    def __init__(self, stationid: str):
        self.stationid: str = stationid


class StationAdminDestroyedEvent:
    def __init__(self, stationid: str):
        self.stationid: str = stationid


class StationMemberDestroyedEvent:
    def __init__(self, stationid: str):
        self.stationid: str = stationid


class StationUserInviteDestroyedEvent:
    def __init__(self, stationid: str):
        self.stationid: str = stationid


class StationUserRequestDestroyedEvent:
    def __init__(self, stationid: str):
        self.stationid: str = stationid


class StationAdminMachineAddedEvent:
    def __init__(self, stationid: str, mids: List[str]):
        self.stationid: str = stationid
        self.mids: List[str] = mids


class StationMemberMachineAddedEvent:
    def __init__(self, stationid: str, mids: List[str]):
        self.stationid: str = stationid
        self.mids: List[str] = mids


class StationAdminVolumeAddedEvent:
    def __init__(self, stationid: str, volumes: List[Volume]):
        self.stationid: str = stationid
        self.volumes: List[str] = volumes


class StationMemberVolumeAddedEvent:
    def __init__(self, stationid: str, volumes: List[Volume]):
        self.stationid: str = stationid
        self.volumes: List[Volume] = volumes


class StationAdminVolumeHostPathAddedEvent:
    def __init__(self, stationid: str, volumes: List[Volume]):
        self.stationid: str = stationid
        self.volumes: List[Volume] = volumes


class StationMemberVolumeHostPathAddedEvent:
    def __init__(self, stationid: str, volumes: List[Volume]):
        self.stationid: str = stationid
        self.volumes: List[Volume] = volumes


class StationAdminVolumeHostPathRemovedEvent:
    def __init__(self, stationid: str, volumes: List[Volume]):
        self.stationid: str = stationid
        self.volumes: List[Volume] = volumes


class StationMemberVolumeHostPathRemovedEvent:
    def __init__(self, stationid: str, volumes: List[Volume]):
        self.stationid: str = stationid
        self.volumes: List[Volume] = volumes


class StationAdminVolumeRemovedEvent:
    def __init__(self, stationid: str, volume_names: List[str]):
        self.stationid: str = stationid
        self.volume_names: List[str] = volume_names


class StationMemberVolumeRemovedEvent:
    def __init__(self, stationid: str, volume_names: List[str]):
        self.stationid: str = stationid
        self.volume_names: List[str] = volume_names


class StationAdminStationUpdated:
    def __init__(self, station: Station):
        self.station = station


class StationMemberStationUpdated:
    def __init__(self, station: Station):
        self.station = station


class StationsEvents:
    _event: EventEmitter

    def __init__(self):
        self._event = EventEmitter()

    def on_new_station(self, func: Callable[[NewStationEvent], None]):
        self._event.on("new_station", func)

    def new_station(self, event: NewStationEvent):
        self._event.emit("new_station", event)

    def on_station_admin_invite_sent(
        self, func: Callable[[StationAdminInviteSentEvent], None]
    ):
        self._event.on("station_admin_invite_sent", func)

    def station_admin_invite_sent(self, event: StationAdminInviteSentEvent):
        self._event.emit("station_admin_invite_sent", event)

    def on_station_user_invite_received(
        self, func: Callable[[StationUserInviteReceivedEvent], None]
    ):
        self._event.on("station_user_invite_received", func)

    def station_user_invite_received(self, event: StationUserInviteReceivedEvent):
        self._event.emit("station_user_invite_received", event)

    def on_station_admin_invite_accepted(
        self, func: Callable[[StationAdminInviteAcceptedEvent], None]
    ):
        self._event.on("station_admin_invite_accepted", func)

    def station_admin_invite_accepted(self, event: StationAdminInviteAcceptedEvent):
        self._event.emit("station_admin_invite_accepted", event)

    def on_station_member_member_added(
        self, func: Callable[[StationMemberMemberEvent], None]
    ):
        self._event.on("station_member_member_added", func)

    def station_member_member_added(self, event: StationMemberMemberEvent):
        self._event.emit("station_member_member_added", event)

    def on_station_user_invite_accepted(
        self, func: Callable[[StationUserInviteAcceptedEvent], None]
    ):
        self._event.on("station_user_invite_accepted", func)

    def station_user_invite_accepted(self, event: StationUserInviteAcceptedEvent):
        self._event.emit("station_user_invite_accept", event)

    def on_station_admin_invite_rejected(
        self, func: Callable[[StationAdminInviteRejectedEvent], None]
    ):
        self._event.on("station_admin_invite_rejected", func)

    def station_admin_invite_rejected(self, event: StationAdminInviteRejectedEvent):
        self._event.emit("station_admin_invite_rejected", event)

    def on_station_user_invite_rejected(
        self, func: Callable[[StationUserInviteRejectedEvent], None]
    ):
        self._event.on("station_user_invite_rejected", func)

    def station_user_invite_rejected(self, event: StationUserInviteRejectedEvent):
        self._event.emit("station_user_invite_rejected", event)

    def on_station_admin_request_received(
        self, func: Callable[[StationAdminRequestReceivedEvent], None]
    ):
        self._event.on("station_admin_request_received", func)

    def station_admin_request_received(self, event: StationAdminRequestReceivedEvent):
        self._event.emit("station_admin_request_received", event)

    def on_station_user_request_sent(
        self, func: Callable[[StationUserRequestSentEvent], None]
    ):
        self._event.on("station_user_request_sent", func)

    def station_user_request_sent(self, event: StationUserRequestSentEvent):
        self._event.emit("station_user_request_sent", event)

    def on_station_admin_request_accepted(
        self, func: Callable[[StationAdminRequestAcceptedEvent], None]
    ):
        self._event.on("station_admin_request_accepted", func)

    def station_admin_request_accepted(self, event: StationAdminRequestAcceptedEvent):
        self._event.emit("station_admin_request_accepted", event)

    def on_station_user_request_accepted(
        self, func: Callable[[StationUserRequestAcceptedEvent], None]
    ):
        self._event.on("station_user_request_accepted", func)

    def station_user_request_accepted(self, event: StationUserRequestAcceptedEvent):
        self._event.emit("station_user_request_accepted", event)

    def on_station_admin_request_rejected(
        self, func: Callable[[StationAdminRequestRejectedEvent], None]
    ):
        self._event.on("station_admin_request_rejected", func)

    def station_admin_request_rejected(self, event: StationAdminRequestRejectedEvent):
        self._event.emit("station_admin_request_rejected", event)

    def on_station_user_request_rejected(
        self, func: Callable[[StationUserRequestRejectedEvent], None]
    ):
        self._event.on("station_user_request_rejected", func)

    def station_user_request_rejected(self, event: StationUserRequestRejectedEvent):
        self._event.emit("station_user_request_rejected", event)

    def on_station_admin_member_removed(
        self, func: Callable[[StationAdminMemberRemovedEvent], None]
    ):
        self._event.on("station_admin_member_removed", func)

    def station_admin_member_removed(self, event: StationAdminMemberRemovedEvent):
        self._event.emit("station_admin_member_removed", event)

    def on_station_admin_machine_removed(
        self, func: Callable[[StationAdminMachineRemovedEvent], None]
    ):
        self._event.on("station_admin_machine_removed", func)

    def station_admin_machine_removed(self, event: StationAdminMachineRemovedEvent):
        self._event.emit("station_admin_machine_removed", event)

    def on_station_member_member_removed(
        self, func: Callable[[StationMemberMemberRemovedEvent], None]
    ):
        self._event.on("station_member_member_removed", func)

    def station_member_member_removed(self, event: StationMemberMemberRemovedEvent):
        self._event.emit("station_member_member_removed", event)

    def on_station_member_machine_removed(
        self, func: Callable[[StationMemberMachineRemovedEvent], None]
    ):
        self._event.on("station_member_machine_removed", func)

    def station_member_machine_removed(self, event: StationMemberMachineRemovedEvent):
        self._event.emit("station_member_machine_removed", event)

    def on_station_user_withdrawn(
        self, func: Callable[[StationUserWithdrawnEvent], None]
    ):
        self._event.on("station_user_withdrawn", func)

    def station_user_withdrawn(self, event: StationUserWithdrawnEvent):
        self._event.emit("station_user_withdrawn", event)

    def on_station_user_expelled(
        self, func: Callable[[StationUserExpelledEvent], None]
    ):
        self._event.on("station_user_expelled", func)

    def station_user_expelled(self, event: StationUserExpelledEvent):
        self._event.emit("station_user_expelled", event)

    def on_station_admin_destroyed(
        self, func: Callable[[StationAdminDestroyedEvent], None]
    ):
        self._event.on("station_admin_destroyed", func)

    def station_admin_destroyed(self, event: StationAdminDestroyedEvent):
        self._event.emit("station_admin_destroyed", event)

    def on_station_member_destroyed(
        self, func: Callable[[StationMemberDestroyedEvent], None]
    ):
        self._event.on("station_member_destroyed", func)

    def station_member_destroyed(self, event: StationMemberDestroyedEvent):
        self._event.emit("station_member_destroyed", event)

    def on_station_user_invite_destroyed(
        self, func: Callable[[StationUserInviteDestroyedEvent], None]
    ):
        self._event.on("station_user_invite_destroyed", func)

    def station_user_invite_destroyed(self, event: StationUserInviteDestroyedEvent):
        self._event.emit("station_user_invite_destroyed", event)

    def on_station_user_request_destroyed(
        self, func: Callable[[StationUserRequestDestroyedEvent], None]
    ):
        self._event.on("station_user_request_destroyed", func)

    def station_user_request_destroyed(self, event: StationUserRequestDestroyedEvent):
        self._event.emit("station_user_request_destroyed", event)

    def on_station_admin_machine_added(
        self, func: Callable[[StationAdminMachineAddedEvent], None]
    ):
        self._event.on("station_admin_machine_added", func)

    def station_admin_machine_added(self, event: StationAdminMachineAddedEvent):
        self._event.emit("station_admin_machine_added", event)

    def on_station_member_machine_added(
        self, func: Callable[[StationMemberMachineAddedEvent], None]
    ):
        self._event.on("station_member_machine_added", func)

    def station_member_machine_added(self, event: StationMemberMachineAddedEvent):
        self._event.emit("station_member_machine_added", event)

    def on_station_admin_volume_added(
        self, func: Callable[[StationAdminVolumeAddedEvent], None]
    ):
        self._event.on("station_admin_volume_added", func)

    def station_admin_volume_added(self, event: StationAdminVolumeAddedEvent):
        self._event.emit("station_admin_volume_added", event)

    def on_station_member_volume_added(
        self, func: Callable[[StationMemberVolumeAddedEvent], None]
    ):
        self._event.on("station_member_volume_added", func)

    def station_member_volume_added(self, event: StationMemberVolumeAddedEvent):
        self._event.emit("station_member_volume_added", event)

    def on_station_admin_volume_host_path_added(
        self, func: Callable[[StationAdminVolumeHostPathAddedEvent], None]
    ):
        self._event.on("station_admin_volume_host_path_added", func)

    def station_admin_volume_host_path_added(
        self, event: StationAdminVolumeHostPathAddedEvent
    ):
        self._event.emit("station_admin_volume_host_path_added", event)

    def on_station_member_volume_host_path_added(
        self, func: Callable[[StationMemberVolumeHostPathAddedEvent], None]
    ):
        self._event.on("station_member_volume_host_path_added", func)

    def station_member_volume_host_path_added(
        self, event: StationMemberVolumeHostPathAddedEvent
    ):
        self._event.emit("station_member_volume_host_path_added", event)

    def on_station_admin_volume_host_path_removed(
        self, func: Callable[[StationAdminVolumeHostPathRemovedEvent], None]
    ):
        self._event.on("station_admin_volume_host_path_removed", func)

    def station_admin_volume_host_path_removed(
        self, event: StationAdminVolumeHostPathRemovedEvent
    ):
        self._event.emit("station_admin_volume_host_path_removed", event)

    def on_station_member_volume_host_path_removed(
        self, func: Callable[[StationMemberVolumeHostPathRemovedEvent], None]
    ):
        self._event.on("station_member_volume_host_path_removed", func)

    def station_member_volume_host_path_removed(
        self, event: StationMemberVolumeHostPathRemovedEvent
    ):
        self._event.emit("station_member_volume_host_path_removed", event)

    def on_station_admin_volume_removed(
        self, func: Callable[[StationAdminVolumeRemovedEvent], None]
    ):
        self._event.on("station_admin_volume_removed", func)

    def station_admin_volume_removed(self, event: StationAdminVolumeRemovedEvent):
        self._event.emit("station_admin_volume_removed", event)

    def on_station_member_volume_removed(
        self, func: Callable[[StationMemberVolumeRemovedEvent], None]
    ):
        self._event.on("station_member_volume_removed", func)

    def station_member_volume_removed(self, event: StationMemberVolumeRemovedEvent):
        self._event.emit("station_member_volume_removed", event)

    def on_station_admin_station_updated(
        self, func: Callable[[StationAdminStationUpdated], None]
    ):
        self._event.on("station_admin_station_updated", func)

    def station_admin_station_updated(self, event: StationAdminStationUpdated):
        self._event.emit("station_admin_station_updated", event)

    def on_station_member_station_updated(
        self, func: Callable[[StationMemberStationUpdated], None]
    ):
        self._event.on("station_member_station_updated", func)

    def station_member_station_updated(self, event: StationMemberStationUpdated):
        self._event.emit("station_admin_station_updated", event)
