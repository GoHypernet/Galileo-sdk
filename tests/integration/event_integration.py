from galileo_sdk import GalileoSdk
from galileo_sdk.business.objects import JobLauncherUpdatedEvent
from galileo_sdk.business.objects.jobs import (JobLauncherSubmittedEvent,
                                               StationJobUpdatedEvent)
from galileo_sdk.business.objects.machines import (MachineHardwareUpdateEvent,
                                                   MachineRegisteredEvent,
                                                   MachineStatusUpdateEvent)
from galileo_sdk.business.objects.stations import (
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
    StationUserExpelledEvent, StationUserInviteAcceptedEvent,
    StationUserInviteDestroyedEvent, StationUserInviteReceivedEvent,
    StationUserInviteRejectedEvent, StationUserRequestAcceptedEvent,
    StationUserRequestDestroyedEvent, StationUserRequestRejectedEvent,
    StationUserRequestSentEvent, StationUserWithdrawnEvent)

CONFIG = "development"
galileo = GalileoSdk(config=CONFIG)


# Machines
def on_machine_status_update(event: MachineStatusUpdateEvent):
    print(f"\non_machine_status_update - ", event.mid, event.status)


def on_hardware_update(event: MachineHardwareUpdateEvent):
    print("\non_hardware_update - ", vars(event.machine))


def on_machine_registered(event: MachineRegisteredEvent):
    print("\non_machine_registered_event - ", vars(event.machine))


# Jobs
def on_job_launcher_updated(event: JobLauncherUpdatedEvent):
    print("\non_job_launcher_updated - ", vars(event.job))


def on_job_launcher_submitted(event: JobLauncherSubmittedEvent):
    print("\non_job_launcher_submitted - ", vars(event.job))


def on_station_job_updated(event: StationJobUpdatedEvent):
    print("\non_station_job_updated - ", vars(event.job))


# Station
def on_new_station(event: NewStationEvent):
    print("\non_new_station - ", vars(event.station))


def on_station_admin_invite_sent(event: StationAdminInviteSentEvent):
    print("\non_station_admin_invite_sent - ", event.stationid, event.userids)


def on_station_user_invite_received(event: StationUserInviteReceivedEvent):
    print("\non_station_user_invite_received - ", vars(event.station))


def on_station_admin_invite_accepted(event: StationAdminInviteAcceptedEvent):
    print("\non_station_admin_invite_accepted - ", event.stationid, event.userid)


def on_station_member_member_added(event: StationMemberMemberEvent):
    print("\non_station_member_member_added - ", event.stationid, event.userid)


def on_station_user_invite_accepted(event: StationUserInviteAcceptedEvent):
    print("\non_station_user_invite_accepted - ", event.stationid, event.userid)


def on_station_admin_invite_rejected(event: StationAdminInviteRejectedEvent):
    print("\non_station_admin_invite_rejected - ", event.stationid, event.userids)


def on_station_user_invite_rejected(event: StationUserInviteRejectedEvent):
    print("\non_station_user_invite_rejected - ", event.stationid, event.userids)


def on_station_admin_request_received(event: StationAdminRequestReceivedEvent):
    print("\non_station_admin_request_received - ", event.stationid, event.userid)


def on_station_user_request_sent(event: StationUserRequestSentEvent):
    print("\non_station_user_request_sent - ", event.stationid, event.userid)


def on_station_admin_request_accepted(event: StationAdminRequestAcceptedEvent):
    print("\non_station_admin_request_accepted - ", event.stationid, event.userid)


def on_station_user_request_accepted(event: StationUserRequestAcceptedEvent):
    print("\non_station_user_request_accepted - ", event.stationid)


def on_station_admin_request_rejected(event: StationAdminRequestRejectedEvent):
    print("\non_station_admin_request_rejected - ", event.stationid, event.userid)


def on_station_user_request_rejected(event: StationUserRequestRejectedEvent):
    print("\non_station_user_request_rejected - ", event.stationid)


def on_station_admin_member_removed(event: StationAdminMemberRemovedEvent):
    print("\non_station_admin_member_removed - ", event.stationid, event.userids)


def on_station_admin_machine_removed(event: StationAdminMachineRemovedEvent):
    print("\non_station_admin_machine_removed - ", event.stationid, event.mids)


def on_station_member_member_removed(event: StationMemberMemberRemovedEvent):
    print("\non_station_member_member_removed", event.stationid, event.userid)


def on_station_member_machine_removed(event: StationMemberMachineRemovedEvent):
    print("\non_station_member_machine_removed", event.stationid, event.mids)


def on_station_user_withdrawn(event: StationUserWithdrawnEvent):
    print("\non_station_user_withdrawn", event.stationid, event.mids)


def on_station_user_expelled(event: StationUserExpelledEvent):
    print("\non_station_user_expelled", event.stationid)


def on_station_admin_destroyed(event: StationAdminDestroyedEvent):
    print("\non_station_admin_destroyed", event.stationid)


def on_station_member_destroyed(event: StationMemberDestroyedEvent):
    print("\non_station_member_destroyed", event.stationid)


def on_station_user_invite_destroyed(event: StationUserInviteDestroyedEvent):
    print("\non_station_user_invite_destroyed", event.stationid)


def on_station_user_request_destroyed(event: StationUserRequestDestroyedEvent):
    print("\non_station_user_request_destroyed", event.stationid)


def on_station_admin_machine_added(event: StationAdminMachineAddedEvent):
    print("\non_station_admin_machine_added", event.stationid, event.mids)


def on_station_member_machine_added(event: StationMemberMachineAddedEvent):
    print("\non_station_member_machine_added", event.stationid, event.mids)


def on_station_admin_volume_added(event: StationAdminVolumeAddedEvent):
    print(
        "\non_station_admin_volume_added",
        event.stationid,
        [vars(volume) for volume in event.volumes],
    )


def on_station_member_volume_added(event: StationMemberVolumeAddedEvent):
    print(
        "\non_station_member_volume_added",
        event.stationid,
        [vars(volume) for volume in event.volumes],
    )


def on_station_admin_volume_host_path_added(
    event: StationAdminVolumeHostPathAddedEvent,
):
    print(
        "\non_station_admin_volume_host_path_added",
        event.stationid,
        [vars(volume) for volume in event.volumes],
    )


def on_station_member_volume_host_path_added(
    event: StationMemberVolumeHostPathAddedEvent,
):
    print(
        "\non_station_member_volume_host_path_added",
        event.stationid,
        [vars(volume) for volume in event.volumes],
    )


def on_station_admin_volume_host_path_removed(
    event: StationAdminVolumeHostPathRemovedEvent,
):
    print(
        "\non_station_admin_volume_host_path_removed",
        event.stationid,
        [vars(volume) for volume in event.volumes],
    )


def on_station_member_volume_host_path_removed(
    event: StationMemberVolumeHostPathRemovedEvent,
):
    print(
        "\non_station_member_volume_host_path_removed",
        event.stationid,
        [vars(volume) for volume in event.volumes],
    )


def on_station_admin_volume_removed(event: StationAdminVolumeRemovedEvent):
    print("\non_station_admin_volume_removed", event.stationid, event.volume_names)


def on_station_member_volume_removed(event: StationMemberVolumeRemovedEvent):
    print("\non_station_member_volume_removed", event.stationid, event.volume_names)


def on_station_admin_station_updated(event: StationAdminStationUpdated):
    print("\non_station_admin_station_updated", vars(event.station))


def on_station_member_station_updated(event: StationMemberStationUpdated):
    print("\non_station_member_station_updated", vars(event.station))


galileo.machines.on_machine_status_update(on_machine_status_update)
galileo.machines.on_machine_hardware_update(on_hardware_update)
galileo.machines.on_machine_registered(on_machine_registered)
galileo.jobs.on_job_launcher_updated(on_job_launcher_updated)
galileo.jobs.on_job_launcher_submitted(on_job_launcher_submitted)
galileo.jobs.on_station_job_updated(on_station_job_updated)
galileo.stations.on_new_station(on_new_station)
galileo.stations.on_station_admin_invite_sent(on_station_admin_invite_sent)
galileo.stations.on_station_user_invite_received(on_station_user_invite_received)
galileo.stations.on_station_admin_invite_accepted(on_station_admin_invite_accepted)
galileo.stations.on_station_member_member_added(on_station_member_member_added)
galileo.stations.on_station_user_invite_accepted(on_station_user_invite_accepted)
galileo.stations.on_station_admin_invite_rejected(on_station_admin_invite_rejected)
galileo.stations.on_station_user_invite_rejected(on_station_user_invite_rejected)
galileo.stations.on_station_admin_request_received(on_station_admin_request_received)
galileo.stations.on_station_user_request_sent(on_station_user_request_sent)
galileo.stations.on_station_admin_request_accepted(on_station_admin_request_accepted)
galileo.stations.on_station_user_request_accepted(on_station_user_request_accepted)
galileo.stations.on_station_admin_request_rejected(on_station_admin_request_rejected)
galileo.stations.on_station_user_request_rejected(on_station_user_request_rejected)
galileo.stations.on_station_admin_member_removed(on_station_admin_member_removed)
galileo.stations.on_station_admin_machine_removed(on_station_admin_machine_removed)
galileo.stations.on_station_member_member_removed(on_station_member_member_removed)
galileo.stations.on_station_member_machine_removed(on_station_member_machine_removed)
galileo.stations.on_station_member_station_updated(on_station_member_station_updated)
galileo.stations.on_station_user_withdrawn(on_station_user_withdrawn)
galileo.stations.on_station_user_expelled(on_station_user_expelled)
galileo.stations.on_station_admin_destroyed(on_station_admin_destroyed)
galileo.stations.on_station_member_destroyed(on_station_member_destroyed)
galileo.stations.on_station_user_invite_destroyed(on_station_user_invite_destroyed)
galileo.stations.on_station_user_request_destroyed(on_station_user_request_destroyed)
galileo.stations.on_station_admin_machine_added(on_station_admin_machine_added)
galileo.stations.on_station_member_machine_added(on_station_member_machine_added)
galileo.stations.on_station_admin_volume_added(on_station_admin_volume_added)
galileo.stations.on_station_member_volume_added(on_station_member_volume_added)
galileo.stations.on_station_admin_volume_host_path_added(
    on_station_admin_volume_host_path_added
)
galileo.stations.on_station_member_volume_host_path_added(
    on_station_member_volume_host_path_added
)
galileo.stations.on_station_admin_volume_host_path_removed(
    on_station_admin_volume_host_path_removed
)
galileo.stations.on_station_member_volume_host_path_removed(
    on_station_member_volume_host_path_removed
)
galileo.stations.on_station_admin_volume_removed(on_station_admin_volume_removed)
galileo.stations.on_station_member_volume_removed(on_station_member_volume_removed)
galileo.stations.on_station_admin_station_updated(on_station_admin_station_updated)
galileo.stations.on_station_member_station_updated(on_station_member_station_updated)

galileo.disconnect()
