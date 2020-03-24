import enum

from ...business.objects.event import EventEmitter


class UpdateStationRequest:
    def __init__(
        self, station_id, name=None, description=None,
    ):
        self.station_id = station_id
        self.name = name
        self.description = description


class EVolumeAccess(enum.Enum):
    READ = "r"
    READWRITE = "rw"


class VolumeHostPath:
    def __init__(self, volumehostpathid, mid, host_path):
        self.volumehostpathid = volumehostpathid
        self.mid = mid
        self.host_path = host_path


class Volume:
    def __init__(
        self, stationid, name, mount_point, access, host_paths, volumeid,
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
    def __init__(self, stationuserid, userid, status):
        self.stationuserid = stationuserid
        self.userid = userid
        self.status = status


class Station:
    def __init__(
        self, stationid, name, description, users, machine_ids=None, volumes=None,
    ):
        self.stationid = stationid
        self.name = name
        self.description = description
        self.users = users
        self.mids = machine_ids
        self.volumes = volumes


class NewStationEvent:
    def __init__(self, station):
        self.station = station


class StationAdminInviteSentEvent:
    def __init__(self, stationid, userids):
        self.stationid = stationid
        self.userids = userids


class StationUserInviteReceivedEvent:
    def __init__(self, station):
        self.station = station


class StationAdminInviteAcceptedEvent:
    def __init__(self, stationid, userid):
        self.stationid = stationid
        self.userid = userid


class StationMemberMemberEvent:
    def __init__(self, stationid, userid):
        self.stationid = stationid
        self.userid = userid


class StationUserInviteAcceptedEvent:
    def __init__(self, stationid, userid):
        self.stationid = stationid
        self.userid = userid


class StationAdminInviteRejectedEvent:
    def __init__(self, stationid, userids):
        self.stationid = stationid
        self.userids = userids


class StationUserInviteRejectedEvent:
    def __init__(self, stationid, userids):
        self.stationid = stationid
        self.userids = userids


class StationAdminRequestReceivedEvent:
    def __init__(self, stationid, userid):
        self.stationid = stationid
        self.userid = userid


class StationUserRequestSentEvent:
    def __init__(self, stationid, userid):
        self.stationid = stationid
        self.userid = userid


class StationAdminRequestAcceptedEvent:
    def __init__(self, stationid, userid):
        self.stationid = stationid
        self.userid = userid


class StationUserRequestAcceptedEvent:
    def __init__(self, stationid):
        self.stationid = stationid


class StationAdminRequestRejectedEvent:
    def __init__(self, stationid, userid):
        self.stationid = stationid
        self.userid = userid


class StationUserRequestRejectedEvent:
    def __init__(self, stationid):
        self.stationid = stationid


class StationAdminMemberRemovedEvent:
    def __init__(self, stationid, userids):
        self.stationid = stationid
        self.userids = userids


class StationAdminMachineRemovedEvent:
    def __init__(self, stationid, mids):
        self.stationid = stationid
        self.mids = mids


class StationMemberMemberRemovedEvent:
    def __init__(self, stationid, userid):
        self.stationid = stationid
        self.userid = userid


class StationMemberMachineRemovedEvent:
    def __init__(self, stationid, mids):
        self.stationid = stationid
        self.mids = mids


class StationUserWithdrawnEvent:
    def __init__(self, stationid, mids):
        self.stationid = stationid
        self.mids = mids


class StationUserExpelledEvent:
    def __init__(self, stationid):
        self.stationid = stationid


class StationAdminDestroyedEvent:
    def __init__(self, stationid):
        self.stationid = stationid


class StationMemberDestroyedEvent:
    def __init__(self, stationid):
        self.stationid = stationid


class StationUserInviteDestroyedEvent:
    def __init__(self, stationid):
        self.stationid = stationid


class StationUserRequestDestroyedEvent:
    def __init__(self, stationid):
        self.stationid = stationid


class StationAdminMachineAddedEvent:
    def __init__(self, stationid, mids):
        self.stationid = stationid
        self.mids = mids


class StationMemberMachineAddedEvent:
    def __init__(self, stationid, mids):
        self.stationid = stationid
        self.mids = mids


class StationAdminVolumeAddedEvent:
    def __init__(self, stationid, volumes):
        self.stationid = stationid
        self.volumes = volumes


class StationMemberVolumeAddedEvent:
    def __init__(self, stationid, volumes):
        self.stationid = stationid
        self.volumes = volumes


class StationAdminVolumeHostPathAddedEvent:
    def __init__(self, stationid, volumes):
        self.stationid = stationid
        self.volumes = volumes


class StationMemberVolumeHostPathAddedEvent:
    def __init__(self, stationid, volumes):
        self.stationid = stationid
        self.volumes = volumes


class StationAdminVolumeHostPathRemovedEvent:
    def __init__(self, stationid, volumes):
        self.stationid = stationid
        self.volumes = volumes


class StationMemberVolumeHostPathRemovedEvent:
    def __init__(self, stationid, volumes):
        self.stationid = stationid
        self.volumes = volumes


class StationAdminVolumeRemovedEvent:
    def __init__(self, stationid, volume_names):
        self.stationid = stationid
        self.volume_names = volume_names


class StationMemberVolumeRemovedEvent:
    def __init__(self, stationid, volume_names):
        self.stationid = stationid
        self.volume_names = volume_names


class StationAdminStationUpdated:
    def __init__(self, station):
        self.station = station


class StationMemberStationUpdated:
    def __init__(self, station):
        self.station = station


class StationsEvents:
    def __init__(self):
        self._event = EventEmitter()

    def on_new_station(self, func):
        self._event.on("new_station", func)

    def new_station(self, event):
        self._event.emit("new_station", event)

    def on_station_admin_invite_sent(self, func):
        self._event.on("station_admin_invite_sent", func)

    def station_admin_invite_sent(self, event):
        self._event.emit("station_admin_invite_sent", event)

    def on_station_user_invite_received(self, func):
        self._event.on("station_user_invite_received", func)

    def station_user_invite_received(self, event):
        self._event.emit("station_user_invite_received", event)

    def on_station_admin_invite_accepted(self, func):
        self._event.on("station_admin_invite_accepted", func)

    def station_admin_invite_accepted(self, event):
        self._event.emit("station_admin_invite_accepted", event)

    def on_station_member_member_added(self, func):
        self._event.on("station_member_member_added", func)

    def station_member_member_added(self, event):
        self._event.emit("station_member_member_added", event)

    def on_station_user_invite_accepted(self, func):
        self._event.on("station_user_invite_accepted", func)

    def station_user_invite_accepted(self, event):
        self._event.emit("station_user_invite_accept", event)

    def on_station_admin_invite_rejected(self, func):
        self._event.on("station_admin_invite_rejected", func)

    def station_admin_invite_rejected(self, event):
        self._event.emit("station_admin_invite_rejected", event)

    def on_station_user_invite_rejected(self, func):
        self._event.on("station_user_invite_rejected", func)

    def station_user_invite_rejected(self, event):
        self._event.emit("station_user_invite_rejected", event)

    def on_station_admin_request_received(self, func):
        self._event.on("station_admin_request_received", func)

    def station_admin_request_received(self, event):
        self._event.emit("station_admin_request_received", event)

    def on_station_user_request_sent(self, func):
        self._event.on("station_user_request_sent", func)

    def station_user_request_sent(self, event):
        self._event.emit("station_user_request_sent", event)

    def on_station_admin_request_accepted(self, func):
        self._event.on("station_admin_request_accepted", func)

    def station_admin_request_accepted(self, event):
        self._event.emit("station_admin_request_accepted", event)

    def on_station_user_request_accepted(self, func):
        self._event.on("station_user_request_accepted", func)

    def station_user_request_accepted(self, event):
        self._event.emit("station_user_request_accepted", event)

    def on_station_admin_request_rejected(self, func):
        self._event.on("station_admin_request_rejected", func)

    def station_admin_request_rejected(self, event):
        self._event.emit("station_admin_request_rejected", event)

    def on_station_user_request_rejected(self, func):
        self._event.on("station_user_request_rejected", func)

    def station_user_request_rejected(self, event):
        self._event.emit("station_user_request_rejected", event)

    def on_station_admin_member_removed(self, func):
        self._event.on("station_admin_member_removed", func)

    def station_admin_member_removed(self, event):
        self._event.emit("station_admin_member_removed", event)

    def on_station_admin_machine_removed(self, func):
        self._event.on("station_admin_machine_removed", func)

    def station_admin_machine_removed(self, event):
        self._event.emit("station_admin_machine_removed", event)

    def on_station_member_member_removed(self, func):
        self._event.on("station_member_member_removed", func)

    def station_member_member_removed(self, event):
        self._event.emit("station_member_member_removed", event)

    def on_station_member_machine_removed(self, func):
        self._event.on("station_member_machine_removed", func)

    def station_member_machine_removed(self, event):
        self._event.emit("station_member_machine_removed", event)

    def on_station_user_withdrawn(self, func):
        self._event.on("station_user_withdrawn", func)

    def station_user_withdrawn(self, event):
        self._event.emit("station_user_withdrawn", event)

    def on_station_user_expelled(self, func):
        self._event.on("station_user_expelled", func)

    def station_user_expelled(self, event):
        self._event.emit("station_user_expelled", event)

    def on_station_admin_destroyed(self, func):
        self._event.on("station_admin_destroyed", func)

    def station_admin_destroyed(self, event):
        self._event.emit("station_admin_destroyed", event)

    def on_station_member_destroyed(self, func):
        self._event.on("station_member_destroyed", func)

    def station_member_destroyed(self, event):
        self._event.emit("station_member_destroyed", event)

    def on_station_user_invite_destroyed(self, func):
        self._event.on("station_user_invite_destroyed", func)

    def station_user_invite_destroyed(self, event):
        self._event.emit("station_user_invite_destroyed", event)

    def on_station_user_request_destroyed(self, func):
        self._event.on("station_user_request_destroyed", func)

    def station_user_request_destroyed(self, event):
        self._event.emit("station_user_request_destroyed", event)

    def on_station_admin_machine_added(self, func):
        self._event.on("station_admin_machine_added", func)

    def station_admin_machine_added(self, event):
        self._event.emit("station_admin_machine_added", event)

    def on_station_member_machine_added(self, func):
        self._event.on("station_member_machine_added", func)

    def station_member_machine_added(self, event):
        self._event.emit("station_member_machine_added", event)

    def on_station_admin_volume_added(self, func):
        self._event.on("station_admin_volume_added", func)

    def station_admin_volume_added(self, event):
        self._event.emit("station_admin_volume_added", event)

    def on_station_member_volume_added(self, func):
        self._event.on("station_member_volume_added", func)

    def station_member_volume_added(self, event):
        self._event.emit("station_member_volume_added", event)

    def on_station_admin_volume_host_path_added(self, func):
        self._event.on("station_admin_volume_host_path_added", func)

    def station_admin_volume_host_path_added(self, event):
        self._event.emit("station_admin_volume_host_path_added", event)

    def on_station_member_volume_host_path_added(self, func):
        self._event.on("station_member_volume_host_path_added", func)

    def station_member_volume_host_path_added(self, event):
        self._event.emit("station_member_volume_host_path_added", event)

    def on_station_admin_volume_host_path_removed(self, func):
        self._event.on("station_admin_volume_host_path_removed", func)

    def station_admin_volume_host_path_removed(self, event):
        self._event.emit("station_admin_volume_host_path_removed", event)

    def on_station_member_volume_host_path_removed(self, func):
        self._event.on("station_member_volume_host_path_removed", func)

    def station_member_volume_host_path_removed(self, event):
        self._event.emit("station_member_volume_host_path_removed", event)

    def on_station_admin_volume_removed(self, func):
        self._event.on("station_admin_volume_removed", func)

    def station_admin_volume_removed(self, event):
        self._event.emit("station_admin_volume_removed", event)

    def on_station_member_volume_removed(self, func):
        self._event.on("station_member_volume_removed", func)

    def station_member_volume_removed(self, event):
        self._event.emit("station_member_volume_removed", event)

    def on_station_admin_station_updated(self, func):
        self._event.on("station_admin_station_updated", func)

    def station_admin_station_updated(self, event):
        self._event.emit("station_admin_station_updated", event)

    def on_station_member_station_updated(self, func):
        self._event.on("station_member_station_updated", func)

    def station_member_station_updated(self, event):
        self._event.emit("station_admin_station_updated", event)
