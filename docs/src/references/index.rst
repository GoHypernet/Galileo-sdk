References
----------

Jobs
~~~~
.. autosummary::
    :toctree: Jobs

    ~galileo_sdk.sdk.jobs.JobsSdk
API
****
.. autosummary::
    :toctree: Jobs API

     ~galileo_sdk.sdk.jobs.JobsSdk.request_stop_job
     ~galileo_sdk.sdk.jobs.JobsSdk.request_pause_job
     ~galileo_sdk.sdk.jobs.JobsSdk.request_start_job
     ~galileo_sdk.sdk.jobs.JobsSdk.request_top_from_job
     ~galileo_sdk.sdk.jobs.JobsSdk.request_logs_from_job
     ~galileo_sdk.sdk.jobs.JobsSdk.list_jobs
     ~galileo_sdk.sdk.jobs.JobsSdk.download_job_results
Objects
*******
.. autosummary::
    :toctree: Jobs Objects

    ~galileo_sdk.business.objects.jobs.Job
    ~galileo_sdk.business.objects.jobs.EJobStatus
    ~galileo_sdk.business.objects.jobs.EJobRunningStatus
    ~galileo_sdk.business.objects.jobs.EPaymentStatus
    ~galileo_sdk.business.objects.jobs.JobLauncherUpdatedEvent
    ~galileo_sdk.business.objects.jobs.JobLauncherResultsDownloadedEvent
    ~galileo_sdk.business.objects.jobs.StationJobUpdatedEvent
    ~galileo_sdk.business.objects.jobs.JobTopEvent
    ~galileo_sdk.business.objects.jobs.JobLogEvent
Events
******
.. autosummary::
    :toctree: Jobs Events

    ~galileo_sdk.sdk.jobs.JobsSdk.on_job_launcher_updated
    ~galileo_sdk.sdk.jobs.JobsSdk.on_job_launcher_results_downloaded
    ~galileo_sdk.sdk.jobs.JobsSdk.on_station_job_updated
    ~galileo_sdk.sdk.jobs.JobsSdk.on_job_top
    ~galileo_sdk.sdk.jobs.JobsSdk.on_job_log



Machines
~~~~~~~~
.. autosummary::
    :toctree: Machines

    ~galileo_sdk.sdk.machines.MachinesSdk
API
****
.. autosummary::
    :toctree: Machine API

    ~galileo_sdk.sdk.machines.MachinesSdk.get_machines_by_id
    ~galileo_sdk.sdk.machines.MachinesSdk.list_machines
    ~galileo_sdk.sdk.machines.MachinesSdk.update_concurrent_max_jobs
Objects
*******
.. autosummary::
    :toctree: Machine Objects

    ~galileo_sdk.business.objects.machines.Machine
    ~galileo_sdk.business.objects.machines.EMachineStatus
    ~galileo_sdk.business.objects.machines.MachineStatusUpdateEvent
Events
*****
.. autosummary::
    :toctree: Machine Events

    ~galileo_sdk.sdk.machines.MachinesSdk.on_machine_status_update



Profiles
~~~~~~~~
.. autosummary::
    :toctree: Profiles

    ~galileo_sdk.sdk.profiles.ProfilesSdk
API
****
.. autosummary::
    :toctree: Profiles API

    ~galileo_sdk.sdk.profiles.ProfilesSdk.self
    ~galileo_sdk.sdk.profiles.ProfilesSdk.list_station_invites
    ~galileo_sdk.sdk.profiles.ProfilesSdk.list_users
Objects
****
.. autosummary::
    :toctree: Profiles Objects

    ~galileo_sdk.business.objects.profiles.Profile
    ~galileo_sdk.business.objects.profiles.ProfileWallet

Projects
~~~~~~~~
.. autosummary::
    :toctree: Projects

    ~galileo_sdk.sdk.projects.ProjectsSdk
API
****
.. autosummary::
    :toctree: Projects API

    ~galileo_sdk.sdk.projects.ProjectsSdk.create_project
    ~galileo_sdk.sdk.projects.ProjectsSdk.upload
    ~galileo_sdk.sdk.projects.ProjectsSdk.run_job_on_station
    ~galileo_sdk.sdk.projects.ProjectsSdk.run_job_on_machine


Stations
~~~~~~~~
.. autosummary::
    :toctree: Station

    ~galileo_sdk.sdk.stations.StationsSdk
API
****
.. autosummary::
    :toctree: Stations API

    ~galileo_sdk.sdk.stations.StationsSdk.list_stations
    ~galileo_sdk.sdk.stations.StationsSdk.create_station
    ~galileo_sdk.sdk.stations.StationsSdk.invite_to_station
    ~galileo_sdk.sdk.stations.StationsSdk.accept_station_invite
    ~galileo_sdk.sdk.stations.StationsSdk.reject_station_invite
    ~galileo_sdk.sdk.stations.StationsSdk.request_to_join
    ~galileo_sdk.sdk.stations.StationsSdk.approve_request_to_join
    ~galileo_sdk.sdk.stations.StationsSdk.reject_request_to_join
    ~galileo_sdk.sdk.stations.StationsSdk.leave_station
    ~galileo_sdk.sdk.stations.StationsSdk.remove_member_from_station
    ~galileo_sdk.sdk.stations.StationsSdk.delete_station
    ~galileo_sdk.sdk.stations.StationsSdk.add_machines_to_station
    ~galileo_sdk.sdk.stations.StationsSdk.remove_machines_from_station
    ~galileo_sdk.sdk.stations.StationsSdk.add_volumes_to_station
    ~galileo_sdk.sdk.stations.StationsSdk.add_host_path_to_volume
    ~galileo_sdk.sdk.stations.StationsSdk.delete_host_path_from_volume
    ~galileo_sdk.sdk.stations.StationsSdk.remove_volume_from_station
Objects
*******
.. autosummary::
    :toctree: Stations Objects

    ~galileo_sdk.business.objects.stations.Station
    ~galileo_sdk.business.objects.stations.StationUser
    ~galileo_sdk.business.objects.stations.Volume
    ~galileo_sdk.business.objects.stations.VolumeHostPath
    ~galileo_sdk.business.objects.stations.EStationUserRole
    ~galileo_sdk.business.objects.stations.EVolumeAccess
    ~galileo_sdk.business.objects.stations.NewStationEvent
    ~galileo_sdk.business.objects.stations.StationAdminInviteSentEvent
    ~galileo_sdk.business.objects.stations.StationUserInviteReceivedEvent
    ~galileo_sdk.business.objects.stations.StationAdminInviteAcceptedEvent
    ~galileo_sdk.business.objects.stations.StationMemberMemberEvent
    ~galileo_sdk.business.objects.stations.StationUserInviteAcceptedEvent
    ~galileo_sdk.business.objects.stations.StationUserInviteRejectedEvent
    ~galileo_sdk.business.objects.stations.StationAdminRequestReceivedEvent
    ~galileo_sdk.business.objects.stations.StationUserRequestSentEvent
    ~galileo_sdk.business.objects.stations.StationAdminRequestAcceptedEvent
    ~galileo_sdk.business.objects.stations.StationUserRequestAcceptedEvent
    ~galileo_sdk.business.objects.stations.StationAdminRequestRejectedEvent
    ~galileo_sdk.business.objects.stations.StationUserRequestRejectedEvent
    ~galileo_sdk.business.objects.stations.StationAdminMemberRemovedEvent
    ~galileo_sdk.business.objects.stations.StationAdminMachineRemovedEvent
    ~galileo_sdk.business.objects.stations.StationMemberMemberRemovedEvent
    ~galileo_sdk.business.objects.stations.StationMemberMachineRemovedEvent
    ~galileo_sdk.business.objects.stations.StationUserWithdrawnEvent
    ~galileo_sdk.business.objects.stations.StationUserExpelledEvent
    ~galileo_sdk.business.objects.stations.StationAdminDestroyedEvent
    ~galileo_sdk.business.objects.stations.StationMemberDestroyedEvent
    ~galileo_sdk.business.objects.stations.StationUserInviteDestroyedEvent
    ~galileo_sdk.business.objects.stations.StationUserRequestDestroyedEvent
    ~galileo_sdk.business.objects.stations.StationAdminMachineAddedEvent
    ~galileo_sdk.business.objects.stations.StationMemberMachineAddedEvent
    ~galileo_sdk.business.objects.stations.StationAdminVolumeAddedEvent
    ~galileo_sdk.business.objects.stations.StationMemberVolumeAddedEvent
    ~galileo_sdk.business.objects.stations.StationAdminVolumeHostPathAddedEvent
    ~galileo_sdk.business.objects.stations.StationMemberVolumeHostPathAddedEvent
    ~galileo_sdk.business.objects.stations.StationAdminVolumeHostPathRemovedEvent
    ~galileo_sdk.business.objects.stations.StationMemberVolumeHostPathRemovedEvent
    ~galileo_sdk.business.objects.stations.StationAdminVolumeRemovedEvent
    ~galileo_sdk.business.objects.stations.StationMemberVolumeRemovedEvent

Events
******
.. autosummary::
    :toctree: Station Events

    ~galileo_sdk.sdk.stations.StationsSdk.on_new_station
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_invite_sent
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_user_invite_received
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_invite_accepted
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_member_added
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_user_invite_accepted
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_invite_rejected
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_request_received
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_user_request_sent
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_request_accepted
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_user_request_accepted
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_request_rejected
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_user_request_rejected
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_member_removed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_machine_removed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_member_removed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_machine_removed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_user_withdrawn
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_user_expelled
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_destroyed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_destroyed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_user_invite_destroyed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_user_request_destroyed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_machine_added
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_machine_added
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_volume_added
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_volume_added
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_volume_host_path_added
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_volume_host_path_added
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_volume_host_path_removed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_volume_host_path_removed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_volume_removed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_volume_removed
