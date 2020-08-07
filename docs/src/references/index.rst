References
----------

Authentication
~~~~~~~~~~~~~~
.. autosummary::
    :toctree: Authentication

    ~galileo_sdk.sdk.auth.AuthSdk

API
****
.. autosummary::
    :toctree: Authentication API

     ~galileo_sdk.sdk.auth.AuthSdk.initialize
     ~galileo_sdk.sdk.auth.AuthSdk.device_flow


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
     ~galileo_sdk.sdk.jobs.JobsSdk.update_job
     ~galileo_sdk.sdk.jobs.JobsSdk.request_kill_job
     ~galileo_sdk.sdk.jobs.JobsSdk.download_and_extract_job_results


Objects
*******
.. autosummary::
    :toctree: Jobs Objects

    ~galileo_sdk.business.objects.jobs.Job
    ~galileo_sdk.business.objects.jobs.EJobStatus
    ~galileo_sdk.business.objects.jobs.EJobRunningStatus
    ~galileo_sdk.business.objects.jobs.EPaymentStatus
    ~galileo_sdk.business.objects.jobs.UpdateJobRequest
    ~galileo_sdk.business.objects.jobs.JobStatus
    ~galileo_sdk.business.objects.jobs.JobLauncherUpdatedEvent
    ~galileo_sdk.business.objects.jobs.JobLauncherSubmittedEvent
    ~galileo_sdk.business.objects.jobs.StationJobUpdatedEvent
    ~galileo_sdk.business.objects.jobs.StationJobUpdatedEvent
    ~galileo_sdk.business.objects.jobs.JobTopEvent
    ~galileo_sdk.business.objects.jobs.JobLogEvent

Events
******
.. autosummary::
    :toctree: Jobs Events

    ~galileo_sdk.sdk.jobs.JobsSdk.on_job_launcher_updated
    ~galileo_sdk.sdk.jobs.JobsSdk.on_job_launcher_submitted
    ~galileo_sdk.sdk.jobs.JobsSdk.on_station_job_updated
    ~galileo_sdk.sdk.jobs.JobsSdk.on_station_job_updated


Lz
~~~~~~~~
.. autosummary::
    :toctree: Lz

    ~galileo_sdk.sdk.lz.LzSdk

API
****
.. autosummary::
    :toctree: Lz API

    ~galileo_sdk.sdk.lz.LzSdk.get_lz_by_id
    ~galileo_sdk.sdk.lz.LzSdk.list_lz
    ~galileo_sdk.sdk.lz.LzSdk.update_lz

Objects
*******
.. autosummary::
    :toctree: Lz Objects

    ~galileo_sdk.business.objects.lz.Lz
    ~galileo_sdk.business.objects.lz.ELzStatus
    ~galileo_sdk.business.objects.lz.LzStatusUpdateEvent
    ~galileo_sdk.business.objects.lz.LzHardwareUpdateEvent
    ~galileo_sdk.business.objects.lz.LzRegisteredEvent
    ~galileo_sdk.business.objects.lz.UpdateLzRequest

Events
******
.. autosummary::
    :toctree: Landing Zone Events

    ~galileo_sdk.sdk.lz.LzSdk.on_lz_status_update
    ~galileo_sdk.sdk.lz.LzSdk.on_lz_hardware_update
    ~galileo_sdk.sdk.lz.LzSdk.on_lz_registered


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
*******
.. autosummary::
    :toctree: Profiles Objects

    ~galileo_sdk.business.objects.profiles.Profile
    ~galileo_sdk.business.objects.profiles.ProfileWallet
    ~galileo_sdk.business.objects.profiles.ProfileCard

Missions
~~~~~~~~
.. autosummary::
    :toctree: Missions

    ~galileo_sdk.sdk.missions.MissionsSdk

API
****
.. autosummary::
    :toctree: Missions API

    ~galileo_sdk.sdk.missions.MissionsSdk.list_missions
    ~galileo_sdk.sdk.missions.MissionsSdk.get_mission_by_id
    ~galileo_sdk.sdk.missions.MissionsSdk.create_mission
    ~galileo_sdk.sdk.missions.MissionsSdk.upload
    ~galileo_sdk.sdk.missions.MissionsSdk.run_job_on_station
    ~galileo_sdk.sdk.missions.MissionsSdk.run_job_on_lz
    ~galileo_sdk.sdk.missions.MissionsSdk.create_and_upload_mission
    ~galileo_sdk.sdk.missions.MissionsSdk.create_mission_and_run_job
    ~galileo_sdk.sdk.missions.MissionsSdk.get_mission_files
    ~galileo_sdk.sdk.missions.MissionsSdk.delete_file
    ~galileo_sdk.sdk.missions.MissionsSdk.update_mission
    ~galileo_sdk.sdk.missions.MissionsSdk.update_mission_args
    ~galileo_sdk.sdk.missions.MissionsSdk.list_mission_types
    ~galileo_sdk.sdk.missions.MissionsSdk.get_mission_type
    ~galileo_sdk.sdk.missions.MissionsSdk.get_mission_type_settings_info

Objects
*******
.. autosummary::
    :toctree: Missions Objects

    ~galileo_sdk.business.objects.Mission
    ~galileo_sdk.business.objects.MissionType
    ~galileo_sdk.business.objects.CreateMissionRequest
    ~galileo_sdk.business.objects.UpdateMissionRequest
    ~galileo_sdk.business.objects.FileListing
    ~galileo_sdk.business.objects.DirectoryListing


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
    ~galileo_sdk.sdk.stations.StationsSdk.add_lz_to_station
    ~galileo_sdk.sdk.stations.StationsSdk.remove_lz_from_station
    ~galileo_sdk.sdk.stations.StationsSdk.add_volumes_to_station
    ~galileo_sdk.sdk.stations.StationsSdk.add_host_path_to_volume
    ~galileo_sdk.sdk.stations.StationsSdk.delete_host_path_from_volume
    ~galileo_sdk.sdk.stations.StationsSdk.remove_volume_from_station
    ~galileo_sdk.sdk.stations.StationsSdk.update_station
    ~galileo_sdk.sdk.stations.StationsSdk.get_station_resource_policy
    ~galileo_sdk.sdk.stations.StationsSdk.update_station_resource_policy
    ~galileo_sdk.sdk.stations.StationsSdk.delete_station_resource_policy
    ~galileo_sdk.sdk.stations.StationsSdk.get_self_station_resource_limits
    ~galileo_sdk.sdk.stations.StationsSdk.update_station_member
    ~galileo_sdk.sdk.stations.StationsSdk.get_station_user_resource_policy
    ~galileo_sdk.sdk.stations.StationsSdk.update_station_user_resource_policy
    ~galileo_sdk.sdk.stations.StationsSdk.delete_station_user_resource_policy
    ~galileo_sdk.sdk.stations.StationsSdk.update_station_role
    ~galileo_sdk.sdk.stations.StationsSdk.delete_station_role
    ~galileo_sdk.sdk.stations.StationsSdk.get_station_role_resource_policy
    ~galileo_sdk.sdk.stations.StationsSdk.update_station_role_resource_policy
    ~galileo_sdk.sdk.stations.StationsSdk.delete_station_role_resource_policy
    ~galileo_sdk.sdk.stations.StationsSdk.get_station_lz_resource_policy
    ~galileo_sdk.sdk.stations.StationsSdk.update_station_lz_resource_policy
    ~galileo_sdk.sdk.stations.StationsSdk.delete_station_lz_resource_policy
    ~galileo_sdk.sdk.stations.StationsSdk.get_station_lz_resource_limits

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
    ~galileo_sdk.business.objects.stations.StationAdminLzRemovedEvent
    ~galileo_sdk.business.objects.stations.StationMemberMemberRemovedEvent
    ~galileo_sdk.business.objects.stations.StationMemberLzRemovedEvent
    ~galileo_sdk.business.objects.stations.StationUserWithdrawnEvent
    ~galileo_sdk.business.objects.stations.StationUserExpelledEvent
    ~galileo_sdk.business.objects.stations.StationAdminDestroyedEvent
    ~galileo_sdk.business.objects.stations.StationMemberDestroyedEvent
    ~galileo_sdk.business.objects.stations.StationUserInviteDestroyedEvent
    ~galileo_sdk.business.objects.stations.StationUserRequestDestroyedEvent
    ~galileo_sdk.business.objects.stations.StationAdminLzAddedEvent
    ~galileo_sdk.business.objects.stations.StationMemberLzAddedEvent
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
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_lz_removed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_member_removed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_lz_removed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_user_withdrawn
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_user_expelled
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_destroyed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_destroyed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_user_invite_destroyed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_user_request_destroyed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_lz_added
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_lz_added
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_volume_added
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_volume_added
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_volume_host_path_added
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_volume_host_path_added
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_volume_host_path_removed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_volume_host_path_removed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_admin_volume_removed
    ~galileo_sdk.sdk.stations.StationsSdk.on_station_member_volume_removed
