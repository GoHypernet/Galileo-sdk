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
    def __init__(
        self,
        stationuserid,
        userid,
        status=None,
        station_id=None,
        username=None,
        role_id=None,
        creation_timestamp=None,
        updated_timestamp=None,
    ):
        self.stationuserid = stationuserid
        self.userid = userid
        self.status = status
        self.station_id = station_id
        self.username = username
        self.role_id = role_id
        self.creation_timestamp = creation_timestamp
        self.updated_timestamp = updated_timestamp


class Station:
    def __init__(
        self,
        stationid,
        name,
        description,
        users,
        lz_ids=None,
        volumes=None,
        status=None,
        organization_id=None,
        creation_timestamp=None,
        updated_timestamp=None,
        autoscale_settings=None,
    ):
        """
        Station Object

        :param stationid: Optional[List[str]]: UUID of the Station
        :param name: Optional[List[str]]: Human readable name of the Station
        :param description: Optional[List[str]]: Optional description of the Station
        :param users: Optional[int]: List of users that belong to the Station
        :param lz_ids: Optional[int]: List of LZs that are accessible through the Station
        :param volumes: Optional[List[str]]: Volumes declared in the Station
        :param status: Optional[bool]: Station status (i.e. active or deactivated)
        :param organization_id: Orgainization the Station is associated with, default if the Hypernet Orginization. 
        :param creation_timestamp: Time the Station was created
        :param updated_timestamp: Time the Station was last updated
        :param autoscale_settings: Currently not used
        """
        self.stationid = stationid
        self.name = name
        self.description = description
        self.users = users
        self.lz_ids = lz_ids
        self.volumes = volumes
        self.status = status
        self.organization_id = organization_id
        self.creation_timestamp = creation_timestamp
        self.updated_timestamp = updated_timestamp
        self.autoscale_settings = autoscale_settings


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


class StationAdminLzRemovedEvent:
    def __init__(self, stationid, lz_ids):
        self.stationid = stationid
        self.lz_ids = lz_ids


class StationMemberMemberRemovedEvent:
    def __init__(self, stationid, userid):
        self.stationid = stationid
        self.userid = userid


class StationMemberLzRemovedEvent:
    def __init__(self, stationid, lz_ids):
        self.stationid = stationid
        self.lz_ids = lz_ids


class StationUserWithdrawnEvent:
    def __init__(self, stationid, lz_ids):
        self.stationid = stationid
        self.lz_ids = lz_ids


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


class StationAdminLzAddedEvent:
    def __init__(self, stationid, mids):
        self.stationid = stationid
        self.mids = mids


class StationMemberLzAddedEvent:
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


class ResourcePolicy:
    def __init__(
        self,
        id,
        max_cpu_per_job,
        max_memory_per_job,
        max_gpu_per_job,
        max_cpu_per_station,
        max_memory_per_station,
        max_gpu_per_station,
        max_cpu_global,
        max_memory_global,
        max_gpu_global,
        max_projects,
        max_users_in_station,
        max_stations,
        max_project_types,
        max_cloud_storage_space,
        max_spend_per_day,
        max_spend_per_week,
        max_spend_per_month,
        max_spend_per_year,
        cpu_credits_per_hour,
        memory_credits_per_hour,
        gpu_credits_per_hour,
        creation_timestamp,
        updated_timestamp,
    ):
        self.id = id
        self.max_cpu_per_job = max_cpu_per_job
        self.max_memory_per_job = max_memory_per_job
        self.max_gpu_per_job = max_gpu_per_job
        self.max_cpu_per_station = max_cpu_per_station
        self.max_memory_per_station = max_memory_per_station
        self.max_gpu_per_station = max_gpu_per_station
        self.max_cpu_global = max_cpu_global
        self.max_memory_global = max_memory_global
        self.max_gpu_global = max_gpu_global
        self.max_projects = max_projects
        self.max_users_in_station = max_users_in_station
        self.max_stations = max_stations
        self.max_project_types = max_project_types
        self.max_cloud_storage_space = max_cloud_storage_space
        self.max_spend_per_day = max_spend_per_day
        self.max_spend_per_week = max_spend_per_week
        self.max_spend_per_month = max_spend_per_month
        self.max_spend_per_year = max_spend_per_year
        self.cpu_credits_per_hour = cpu_credits_per_hour
        self.memory_credits_per_hour = memory_credits_per_hour
        self.gpu_credits_per_hour = gpu_credits_per_hour
        self.creation_timestamp = creation_timestamp
        self.updated_timestamp = updated_timestamp


class UpdateResourcePolicyRequest:
    def __init__(
        self,
        max_cpu_per_job=None,
        max_memory_per_job=None,
        max_gpu_per_job=None,
        max_cpu_per_station=None,
        max_memory_per_station=None,
        max_gpu_per_station=None,
        max_cpu_global=None,
        max_memory_global=None,
        max_gpu_global=None,
        max_projects=None,
        max_users_in_station=None,
        max_stations=None,
        max_project_types=None,
        max_cloud_storage_space=None,
        max_spend_per_day=None,
        max_spend_per_week=None,
        max_spend_per_month=None,
        max_spend_per_year=None,
        cpu_credits_per_hour=None,
        memory_credits_per_hour=None,
        gpu_credits_per_hour=None,
    ):
        self.max_cpu_per_job = max_cpu_per_job
        self.max_memory_per_job = max_memory_per_job
        self.max_gpu_per_job = max_gpu_per_job
        self.max_cpu_per_station = max_cpu_per_station
        self.max_memory_per_station = max_memory_per_station
        self.max_gpu_per_station = max_gpu_per_station
        self.max_cpu_global = max_cpu_global
        self.max_memory_global = max_memory_global
        self.max_gpu_global = max_gpu_global
        self.max_projects = max_projects
        self.max_users_in_station = max_users_in_station
        self.max_stations = max_stations
        self.max_project_types = max_project_types
        self.max_cloud_storage_space = max_cloud_storage_space
        self.max_spend_per_day = max_spend_per_day
        self.max_spend_per_week = max_spend_per_week
        self.max_spend_per_month = max_spend_per_month
        self.max_spend_per_year = max_spend_per_year
        self.cpu_credits_per_hour = cpu_credits_per_hour
        self.memory_credits_per_hour = memory_credits_per_hour
        self.gpu_credits_per_hour = gpu_credits_per_hour


class CreateStationRoleRequest:
    def __init__(
        self,
        name,
        description,
        role_type=None,
        protected_role=0,
        edit_station_roles=0,
        assign_user_roles=0,
        assign_protected_user_roles=0,
        launch_jobs=0,
        invite_users=0,
        remove_all_users=0,
        remove_invited_users=0,
        view_all_users=0,
        edit_metadata=0,
        add_machine=0,
        remove_any_machine=0,
        view_all_jobs=0,
        control_all_jobs=0,
        view_jobs_on_own_machines=0,
        control_jobs_on_own_machines=0,
        view_own_jobs=0,
        control_own_jobs=0,
        view_complete_activity=0,
        edit_station_policy=0,
        edit_own_machine_policy=0,
        edit_machine_policy=0,
        edit_user_policy=0,
        edit_job_resource_limits=0,
        add_autoscale=0,
        edit_autoscale=0,
        remove_autoscale=0,
        manage_volumes=0,
        reject_user_requests=0,
    ):
        self.name = name
        self.description = description
        self.role_type = role_type
        self.protected_role = protected_role
        self.edit_station_roles = edit_station_roles
        self.assign_user_roles = assign_user_roles
        self.assign_protected_user_roles = assign_protected_user_roles
        self.launch_jobs = launch_jobs
        self.invite_users = invite_users
        self.remove_all_users = remove_all_users
        self.remove_invited_users = remove_invited_users
        self.view_all_users = view_all_users
        self.edit_metadata = edit_metadata
        self.add_machine = add_machine
        self.remove_any_machine = remove_any_machine
        self.view_all_jobs = view_all_jobs
        self.control_all_jobs = control_all_jobs
        self.view_jobs_on_own_machines = view_jobs_on_own_machines
        self.control_jobs_on_own_machines = control_jobs_on_own_machines
        self.view_own_jobs = view_own_jobs
        self.control_own_jobs = control_own_jobs
        self.view_complete_activity = view_complete_activity
        self.edit_station_policy = edit_station_policy
        self.edit_own_machine_policy = edit_own_machine_policy
        self.edit_machine_policy = edit_machine_policy
        self.edit_user_policy = edit_user_policy
        self.edit_job_resource_limits = edit_job_resource_limits
        self.add_autoscale = add_autoscale
        self.edit_autoscale = edit_autoscale
        self.remove_autoscale = remove_autoscale
        self.manage_volumes = manage_volumes
        self.reject_user_requests = reject_user_requests


class UpdateStationRoleRequest:
    def __init__(
        self,
        name=None,
        description=None,
        protected_role=None,
        edit_station_role=None,
        assign_user_roles=None,
        assign_protected_user_roles=None,
        launch_jobs=None,
        invite_users=None,
        remove_all_users=None,
        remove_invited_users=None,
        view_all_users=None,
        edit_metadata=None,
        add_machine=None,
        remove_any_machine=None,
        view_all_jobs=None,
        control_all_jobs=None,
        view_jobs_on_own_machines=None,
        control_jobs_on_own_machines=None,
        view_own_jobs=None,
        control_own_jobs=None,
        view_complete_activity=None,
        edit_station_policy=None,
        edit_own_machine_policy=None,
        edit_machine_policy=None,
        edit_user_policy=None,
        edit_job_resource_limits=None,
        manage_volumes=None,
        reject_user_requests=None,
    ):
        self.name = name
        self.description = description
        self.protected_role = protected_role
        self.edit_station_role = edit_station_role
        self.assign_user_roles = assign_user_roles
        self.assign_protected_user_roles = assign_protected_user_roles
        self.launch_jobs = launch_jobs
        self.invite_users = invite_users
        self.remove_all_users = remove_all_users
        self.remove_invited_users = remove_invited_users
        self.view_all_users = view_all_users
        self.edit_metadata = edit_metadata
        self.add_machine = add_machine
        self.remove_any_machine = remove_any_machine
        self.view_all_jobs = view_all_jobs
        self.control_all_jobs = control_all_jobs
        self.view_jobs_on_own_machines = view_jobs_on_own_machines
        self.control_jobs_on_own_machines = control_jobs_on_own_machines
        self.view_own_jobs = view_own_jobs
        self.control_own_jobs = control_own_jobs
        self.view_complete_activity = view_complete_activity
        self.edit_station_policy = edit_station_policy
        self.edit_own_machine_policy = edit_own_machine_policy
        self.edit_machine_policy = edit_machine_policy
        self.edit_user_policy = edit_user_policy
        self.edit_job_resource_limits = edit_job_resource_limits
        self.manage_volumes = manage_volumes
        self.reject_user_requests = reject_user_requests


class AutoscaleSettings:
    def __init__(
        self,
        id,
        station_id,
        creation_timestamp,
        updated_timestamp,
        increment_amount,
        name_prefix,
        computer_provider_id,
        provision_count,
        provision_count_min,
        provision_count_max,
        usage_threshold_up,
        usage_threshold_down,
        status,
    ):
        self.id = id
        self.station_id = station_id
        self.creation_timestamp = creation_timestamp
        self.updated_timestamp = updated_timestamp
        self.increment_amount = increment_amount
        self.name_prefix = name_prefix
        self.computer_provider_id = computer_provider_id
        self.provision_count = provision_count
        self.provision_count_min = provision_count_min
        self.provision_count_max = provision_count_max
        self.usage_threshold_up = usage_threshold_up
        self.usage_threshold_down = usage_threshold_down
        self.status = status


class StationRole:
    def __init__(
        self,
        id,
        station_id,
        creation_timestamp,
        updated_timestamp,
        name,
        description,
        role_type,
        protected_role,
        edit_station_roles,
        assign_user_roles,
        assign_protected_user_roles,
        launch_jobs,
        invite_users,
        remove_all_users,
        remove_invited_users,
        view_all_users,
        edit_metadata,
        add_machine,
        remove_any_machine,
        view_all_jobs,
        control_all_jobs,
        view_jobs_on_own_machines,
        control_jobs_on_own_machines,
        view_own_jobs,
        control_own_jobs,
        view_complete_activity,
        edit_station_policy,
        edit_own_machine_policy,
        edit_machine_policy,
        edit_user_policy,
        edit_job_resource_limits,
        manage_volumes,
        reject_user_requests,
    ):
        self.id = id
        self.station_id = station_id
        self.creation_timestamp = creation_timestamp
        self.updated_timestamp = updated_timestamp
        self.name = name
        self.description = description
        self.role_type = role_type
        self.protected_role = protected_role
        self.edit_station_roles = edit_station_roles
        self.assign_user_roles = assign_user_roles
        self.assign_protected_user_roles = assign_protected_user_roles
        self.launch_jobs = launch_jobs
        self.invite_users = invite_users
        self.remove_all_users = remove_all_users
        self.remove_invited_users = remove_invited_users
        self.view_all_users = view_all_users
        self.edit_metadata = edit_metadata
        self.add_machine = add_machine
        self.remove_any_machine = remove_any_machine
        self.view_all_jobs = view_all_jobs
        self.control_all_jobs = control_all_jobs
        self.view_jobs_on_own_machines = view_jobs_on_own_machines
        self.control_jobs_on_own_machines = control_jobs_on_own_machines
        self.view_own_jobs = view_own_jobs
        self.control_own_jobs = control_own_jobs
        self.view_complete_activity = view_complete_activity
        self.edit_station_policy = edit_station_policy
        self.edit_own_machine_policy = edit_own_machine_policy
        self.edit_machine_policy = edit_machine_policy
        self.edit_user_policy = edit_user_policy
        self.edit_job_resource_limits = edit_job_resource_limits
        self.manage_volumes = manage_volumes
        self.reject_user_requests = reject_user_requests


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
