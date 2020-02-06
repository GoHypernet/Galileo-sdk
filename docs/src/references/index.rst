References
----------

Jobs
~~~~
API
****
.. autosummary::
    ~src.sdk.jobs.JobsSdk.on_job_launcher_updated
    ~src.sdk.jobs.JobsSdk.on_job_launcher_results_downloaded
    ~src.sdk.jobs.JobsSdk.on_station_job_updated
    ~src.sdk.jobs.JobsSdk.on_job_top
    ~src.sdk.jobs.JobsSdk.on_job_log
    ~src.sdk.jobs.JobsSdk.request_stop_job
    ~src.sdk.jobs.JobsSdk.request_pause_job
    ~src.sdk.jobs.JobsSdk.request_start_job
    ~src.sdk.jobs.JobsSdk.request_top_from_job
    ~src.sdk.jobs.JobsSdk.request_logs_from_job
    ~src.sdk.jobs.JobsSdk.list_jobs
    ~src.sdk.jobs.JobsSdk.download_job_results
Objects
*******
.. autosummary::
    ~src.business.objects.jobs.Job
    ~src.business.objects.jobs.EJobStatus
    ~src.business.objects.jobs.EJobRunningStatus
    ~src.business.objects.jobs.EPaymentStatus
Events
******
.. autosummary::
    ~src.business.objects.jobs.JobLauncherUpdatedEvent
    ~src.business.objects.jobs.JobLauncherResultsDownloadedEvent
    ~src.business.objects.jobs.StationJobUpdatedEvent
    ~src.business.objects.jobs.JobTopEvent
    ~src.business.objects.jobs.JobLogEvent


Machines
~~~~~~~~
API
****
.. autosummary::
    ~src.sdk.machines.MachinesSdk.on_machine_status_update
    ~src.sdk.machines.MachinesSdk.get_machines_by_id
    ~src.sdk.machines.MachinesSdk.list_machines
    ~src.sdk.machines.MachinesSdk.update_concurrent_max_jobs
Objects
*******
.. autosummary::
    ~src.business.objects.machines.Machine
    ~src.business.objects.machines.EMachineStatus
Events
*****
.. autosummary::
    ~src.business.objects.machines.MachineStatusUpdateEvent


Profiles
~~~~~~~~
API
****
.. autosummary::
    ~src.sdk.profiles.ProfilesSdk.self
    ~src.sdk.profiles.ProfilesSdk.list_station_invites
    ~src.sdk.profiles.ProfilesSdk.list_users
Objects
****
.. autosummary::
    ~src.business.objects.profiles.Profile
    ~src.business.objects.profiles.ProfileWallet

Projects
~~~~~~~~
API
****
.. autosummary::
    ~src.sdk.projects.ProjectsSdk.create_project
    ~src.sdk.projects.ProjectsSdk.upload_single_file
    ~src.sdk.projects.ProjectsSdk.run_job_on_station
    ~src.sdk.projects.ProjectsSdk.run_job_on_machine


Stations
~~~~~~~~
API
****
.. autosummary::
    ~src.sdk.stations.StationsSdk.on_new_station
    ~src.sdk.stations.StationsSdk.on_station_admin_invite_sent
    ~src.sdk.stations.StationsSdk.on_station_user_invite_received
    ~src.sdk.stations.StationsSdk.on_station_admin_invite_accepted
    ~src.sdk.stations.StationsSdk.on_station_member_member_added
    ~src.sdk.stations.StationsSdk.on_station_user_invite_accepted
    ~src.sdk.stations.StationsSdk.on_station_admin_invite_rejected
    ~src.sdk.stations.StationsSdk.on_station_admin_request_received
    ~src.sdk.stations.StationsSdk.on_station_user_request_sent
    ~src.sdk.stations.StationsSdk.on_station_admin_request_accepted
    ~src.sdk.stations.StationsSdk.on_station_user_request_accepted
    ~src.sdk.stations.StationsSdk.on_station_admin_request_rejected
    ~src.sdk.stations.StationsSdk.on_station_user_request_rejected
    ~src.sdk.stations.StationsSdk.on_station_admin_member_removed
    ~src.sdk.stations.StationsSdk.on_station_admin_machine_removed
    ~src.sdk.stations.StationsSdk.on_station_member_member_removed
    ~src.sdk.stations.StationsSdk.on_station_member_machine_removed
    ~src.sdk.stations.StationsSdk.on_station_user_withdrawn
    ~src.sdk.stations.StationsSdk.on_station_user_expelled
    ~src.sdk.stations.StationsSdk.on_station_admin_destroyed
    ~src.sdk.stations.StationsSdk.on_station_member_destroyed
    ~src.sdk.stations.StationsSdk.on_station_user_invite_destroyed
    ~src.sdk.stations.StationsSdk.on_station_user_request_destroyed
    ~src.sdk.stations.StationsSdk.on_station_admin_machine_added
    ~src.sdk.stations.StationsSdk.on_station_member_machine_added
    ~src.sdk.stations.StationsSdk.on_station_admin_volume_added
    ~src.sdk.stations.StationsSdk.on_station_member_volume_added
    ~src.sdk.stations.StationsSdk.on_station_admin_volume_host_path_added
    ~src.sdk.stations.StationsSdk.on_station_member_volume_host_path_added
    ~src.sdk.stations.StationsSdk.on_station_admin_volume_host_path_removed
    ~src.sdk.stations.StationsSdk.on_station_member_volume_host_path_removed
    ~src.sdk.stations.StationsSdk.on_station_admin_volume_removed
    ~src.sdk.stations.StationsSdk.on_station_member_volume_removed
    ~src.sdk.stations.StationsSdk.list_stations
    ~src.sdk.stations.StationsSdk.create_station
    ~src.sdk.stations.StationsSdk.invite_to_station
    ~src.sdk.stations.StationsSdk.accept_station_invite
    ~src.sdk.stations.StationsSdk.reject_station_invite
    ~src.sdk.stations.StationsSdk.request_to_join
    ~src.sdk.stations.StationsSdk.approve_request_to_join
    ~src.sdk.stations.StationsSdk.reject_request_to_join
    ~src.sdk.stations.StationsSdk.leave_station
    ~src.sdk.stations.StationsSdk.remove_member_from_station
    ~src.sdk.stations.StationsSdk.delete_station
    ~src.sdk.stations.StationsSdk.add_machines_to_station
    ~src.sdk.stations.StationsSdk.remove_machines_from_station
    ~src.sdk.stations.StationsSdk.add_volumes_to_station
    ~src.sdk.stations.StationsSdk.add_host_path_to_volume
    ~src.sdk.stations.StationsSdk.delete_host_path_from_volume
    ~src.sdk.stations.StationsSdk.remove_volume_from_station
Objects
*******
.. autosummary::
    ~src.business.objects.stations.Station
    ~src.business.objects.stations.StationUser
    ~src.business.objects.stations.Volume
    ~src.business.objects.stations.VolumeHostPath
    ~src.business.objects.stations.EStationUserRole
    ~src.business.objects.stations.EVolumeAccess
Events
******
.. autosummary::
    ~src.business.objects.stations.NewStationEvent
    ~src.business.objects.stations.StationAdminInviteSentEvent
    ~src.business.objects.stations.StationUserInviteReceivedEvent
    ~src.business.objects.stations.StationAdminInviteAcceptedEvent
    ~src.business.objects.stations.StationMemberMemberEvent
    ~src.business.objects.stations.StationUserInviteAcceptedEvent
    ~src.business.objects.stations.StationUserInviteRejectedEvent
    ~src.business.objects.stations.StationAdminRequestReceivedEvent
    ~src.business.objects.stations.StationUserRequestSentEvent
    ~src.business.objects.stations.StationAdminRequestAcceptedEvent
    ~src.business.objects.stations.StationUserRequestAcceptedEvent
    ~src.business.objects.stations.StationAdminRequestRejectedEvent
    ~src.business.objects.stations.StationUserRequestRejectedEvent
    ~src.business.objects.stations.StationAdminMemberRemovedEvent
    ~src.business.objects.stations.StationAdminMachineRemovedEvent
    ~src.business.objects.stations.StationMemberMemberRemovedEvent
    ~src.business.objects.stations.StationMemberMachineRemovedEvent
    ~src.business.objects.stations.StationUserWithdrawnEvent
    ~src.business.objects.stations.StationUserExpelledEvent
    ~src.business.objects.stations.StationAdminDestroyedEvent
    ~src.business.objects.stations.StationMemberDestroyedEvent
    ~src.business.objects.stations.StationUserInviteDestroyedEvent
    ~src.business.objects.stations.StationUserRequestDestroyedEvent
    ~src.business.objects.stations.StationAdminMachineAddedEvent
    ~src.business.objects.stations.StationMemberMachineAddedEvent
    ~src.business.objects.stations.StationAdminVolumeAddedEvent
    ~src.business.objects.stations.StationMemberVolumeAddedEvent
    ~src.business.objects.stations.StationAdminVolumeHostPathAddedEvent
    ~src.business.objects.stations.StationMemberVolumeHostPathAddedEvent
    ~src.business.objects.stations.StationAdminVolumeHostPathRemovedEvent
    ~src.business.objects.stations.StationMemberVolumeHostPathRemovedEvent
    ~src.business.objects.stations.StationAdminVolumeRemovedEvent
    ~src.business.objects.stations.StationMemberVolumeRemovedEvent
