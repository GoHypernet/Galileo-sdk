from galileo_sdk import GalileoSdk

CONFIG = "development"
galileo = GalileoSdk(config=CONFIG)


# Machines
def on_machine_status_update(event):
    print("\non_machine_status_update - ", event.mid, event.status)


def on_hardware_update(event):
    print("\non_hardware_update - ", vars(event.machine))


def on_machine_registered(event):
    print("\non_machine_registered_event - ", vars(event.machine))


# Jobs
def on_job_launcher_updated(event):
    print("\non_job_launcher_updated - ", vars(event.job))


def on_job_launcher_submitted(event):
    print("\non_job_launcher_submitted - ", vars(event.job))


def on_station_job_updated(event):
    print("\non_station_job_updated - ", vars(event.job))


# Station
def on_new_station(event):
    print("\non_new_station - ", vars(event.station))


def on_station_admin_invite_sent(event):
    print("\non_station_admin_invite_sent - ", event.stationid, event.userids)


def on_station_user_invite_received(event):
    print("\non_station_user_invite_received - ", vars(event.station))


def on_station_admin_invite_accepted(event):
    print("\non_station_admin_invite_accepted - ", event.stationid, event.userid)


def on_station_member_member_added(event):
    print("\non_station_member_member_added - ", event.stationid, event.userid)


def on_station_user_invite_accepted(event):
    print("\non_station_user_invite_accepted - ", event.stationid, event.userid)


def on_station_admin_invite_rejected(event):
    print("\non_station_admin_invite_rejected - ", event.stationid, event.userids)


def on_station_user_invite_rejected(event):
    print("\non_station_user_invite_rejected - ", event.stationid, event.userids)


def on_station_admin_request_received(event):
    print("\non_station_admin_request_received - ", event.stationid, event.userid)


def on_station_user_request_sent(event):
    print("\non_station_user_request_sent - ", event.stationid, event.userid)


def on_station_admin_request_accepted(event):
    print("\non_station_admin_request_accepted - ", event.stationid, event.userid)


def on_station_user_request_accepted(event):
    print("\non_station_user_request_accepted - ", event.stationid)


def on_station_admin_request_rejected(event):
    print("\non_station_admin_request_rejected - ", event.stationid, event.userid)


def on_station_user_request_rejected(event):
    print("\non_station_user_request_rejected - ", event.stationid)


def on_station_admin_member_removed(event):
    print("\non_station_admin_member_removed - ", event.stationid, event.userids)


def on_station_admin_machine_removed(event):
    print("\non_station_admin_machine_removed - ", event.stationid, event.mids)


def on_station_member_member_removed(event):
    print("\non_station_member_member_removed", event.stationid, event.userid)


def on_station_member_machine_removed(event):
    print("\non_station_member_machine_removed", event.stationid, event.mids)


def on_station_user_withdrawn(event):
    print("\non_station_user_withdrawn", event.stationid, event.mids)


def on_station_user_expelled(event):
    print("\non_station_user_expelled", event.stationid)


def on_station_admin_destroyed(event):
    print("\non_station_admin_destroyed", event.stationid)


def on_station_member_destroyed(event):
    print("\non_station_member_destroyed", event.stationid)


def on_station_user_invite_destroyed(event):
    print("\non_station_user_invite_destroyed", event.stationid)


def on_station_user_request_destroyed(event):
    print("\non_station_user_request_destroyed", event.stationid)


def on_station_admin_machine_added(event):
    print("\non_station_admin_machine_added", event.stationid, event.mids)


def on_station_member_machine_added(event):
    print("\non_station_member_machine_added", event.stationid, event.mids)


def on_station_admin_volume_added(event):
    print(
        "\non_station_admin_volume_added",
        event.stationid,
        [vars(volume) for volume in event.volumes],
    )


def on_station_member_volume_added(event):
    print(
        "\non_station_member_volume_added",
        event.stationid,
        [vars(volume) for volume in event.volumes],
    )


def on_station_admin_volume_host_path_added(event):
    print(
        "\non_station_admin_volume_host_path_added",
        event.stationid,
        [vars(volume) for volume in event.volumes],
    )


def on_station_member_volume_host_path_added(event):
    print(
        "\non_station_member_volume_host_path_added",
        event.stationid,
        [vars(volume) for volume in event.volumes],
    )


def on_station_admin_volume_host_path_removed(event):
    print(
        "\non_station_admin_volume_host_path_removed",
        event.stationid,
        [vars(volume) for volume in event.volumes],
    )


def on_station_member_volume_host_path_removed(event):
    print(
        "\non_station_member_volume_host_path_removed",
        event.stationid,
        [vars(volume) for volume in event.volumes],
    )


def on_station_admin_volume_removed(event):
    print("\non_station_admin_volume_removed", event.stationid, event.volume_names)


def on_station_member_volume_removed(event):
    print("\non_station_member_volume_removed", event.stationid, event.volume_names)


def on_station_admin_station_updated(event):
    print("\non_station_admin_station_updated", vars(event.station))


def on_station_member_station_updated(event):
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
