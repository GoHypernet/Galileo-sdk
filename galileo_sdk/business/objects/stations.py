import enum

from ...business.objects.event import EventEmitter


class UpdateStationRequest:
    def __init__(
        self,
        station_id,
        name=None,
        description=None,
        public=None,
        allow_auto_join=None,
    ):
        self.station_id = station_id
        self.name = name
        self.description = description
        self.public = public
        self.allow_auto_join = allow_auto_join


class EVolumeAccess(enum.Enum):
    READ = "r"
    READWRITE = "rw"


class VolumeHostPath:
    def __init__(self, volume_hostpath_id, lz_id, host_path):
        self.volume_hostpath_id = volume_hostpath_id
        self.lz_id = lz_id
        self.host_path = host_path


class Volume:
    def __init__(
        self,
        station_id,
        name,
        mount_point,
        access,
        host_paths,
        volume_id,
    ):
        self.volume_id = volume_id
        self.station_id = station_id
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
        stationuser_id,
        user_id,
        status=None,
        station_id=None,
        username=None,
        role_id=None,
        creation_timestamp=None,
        updated_timestamp=None,
    ):
        self.stationuser_id = stationuser_id
        self.user_id = user_id
        self.status = status
        self.station_id = station_id
        self.username = username
        self.role_id = role_id
        self.creation_timestamp = creation_timestamp
        self.updated_timestamp = updated_timestamp


class PublicStation:
    def __init__(
        self,
        name,
        station_id,
        description=None,
        creation_timestamp=None,
        updated_timestamp=None,
        public=True,
        allowed_mission_types=None,
        allow_auto_join=None,
        jobs_in_queue_count=None,
        member_count=None,
        lz_id_count=None,
        resource_policy=None,
        user_count=None,
        user_status=None,
        volume_count=None,
    ):
        """
        Public Station Object

        :param name: str: Human readable name of the Station
        :param station_id: str: UUID of the Station
        :param description: Optional[str]: Optional description of the Station
        :param creation_timestamp: Optional[str]: Time the Station was created
        :param updated_timestamp: Optional[str]: Time the Station was last updated
        :param allow_auto_join: Optional[bool] Station automatically accepts user requests to join
        :param public: Optional[bool]: Is station public or not (should always be public)
        :param allowed_mission_types: Mission types allowed for this station
        :param job_in_queue_count: [int]: Number of jobs in the queue
        :param member_count: [int]: Number of members in the station
        :param mid_count: [int]: Number of mids in the station
        :param resource_policy: Resource policies for the station
        :param user_count: [int]: Number of users in the station
        :param user_status: Status of the user in the station
        :param volume_count: Number of volumes in the station
        """
        self.station_id = station_id
        self.name = name
        self.description = description

        self.creation_timestamp = creation_timestamp
        self.updated_timestamp = updated_timestamp
        self.public = public
        self.allow_auto_join = allow_auto_join
        self.allowed_mission_types = allowed_mission_types
        self.jobs_in_queue_count = jobs_in_queue_count
        self.member_count = member_count
        self.lz_id_count = lz_id_count
        self.resource_policy = resource_policy
        self.user_count = user_count
        self.user_status = user_status
        self.volume_count = volume_count

    def __str__(self):
        return "Public Station: {name} (autojoin:{allow_auto_join})".format(
            name=self.name, allow_auto_join=self.allow_auto_join)

    def __repr__(self):
        return self.__str__()


class Station:
    def __init__(
        self,
        station_id,
        name,
        description,
        users,
        allow_auto_join=None,
        public=None,
        lz_ids=None,
        crew_ids=None,
        machine_summaries=None,
        volumes=None,
        status=None,
        universe_id=None,
        creation_timestamp=None,
        updated_timestamp=None,
        autoscale_settings=None,
    ):
        """
        Station Object

        :param station_id: Optional[List[str]]: UUID of the Station
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
        self.station_id = station_id
        self.name = name
        self.description = description
        self.users = users
        self.lz_ids = lz_ids
        self.crew_ids = crew_ids
        self.volumes = volumes
        self.status = status
        self.universe_id = universe_id
        self.creation_timestamp = creation_timestamp
        self.updated_timestamp = updated_timestamp
        self.autoscale_settings = autoscale_settings
        self.machine_summaries = machine_summaries,
        self.allow_auto_join = allow_auto_join
        self.public = public

    def __str__(self):
        return "Station: {name} (autojoin:{allow_auto_join})".format(
            name=self.name, allow_auto_join=self.allow_auto_join)

    def __repr__(self):
        return self.__str__()


class NewStationEvent:
    def __init__(self, station):
        self.station = station


class StationAdminInviteSentEvent:
    def __init__(self, station_id, user_ids):
        self.station_id = station_id
        self.user_ids = user_ids


class StationUserInviteReceivedEvent:
    def __init__(self, station):
        self.station = station


class StationAdminInviteAcceptedEvent:
    def __init__(self, station_id, user_id):
        self.station_id = station_id
        self.user_id = user_id


class StationMemberMemberEvent:
    def __init__(self, station_id, user_id):
        self.stationid = station_id
        self.user_id = user_id


class StationUserInviteAcceptedEvent:
    def __init__(self, station_id, user_id):
        self.stationid = station_id
        self.user_id = user_id


class StationAdminInviteRejectedEvent:
    def __init__(self, station_id, user_ids):
        self.station_id = station_id
        self.user_ids = user_ids


class StationUserInviteRejectedEvent:
    def __init__(self, station_id, user_ids):
        self.stationid = station_id
        self.user_ids = user_ids


class StationAdminRequestReceivedEvent:
    def __init__(self, station_id, user_id):
        self.station_id = station_id
        self.user_id = user_id


class StationUserRequestSentEvent:
    def __init__(self, station_id, user_id):
        self.station_id = station_id
        self.user_id = user_id


class StationAdminRequestAcceptedEvent:
    def __init__(self, station_id, user_id):
        self.station_id = station_id
        self.user_id = user_id


class StationUserRequestAcceptedEvent:
    def __init__(self, station_id):
        self.station_id = station_id


class StationAdminRequestRejectedEvent:
    def __init__(self, station_id, user_id):
        self.station_id = station_id
        self.user_id = user_id


class StationUserRequestRejectedEvent:
    def __init__(self, station_id):
        self.station_id = station_id


class StationAdminMemberRemovedEvent:
    def __init__(self, station_id, user_ids):
        self.station_id = station_id
        self.user_ids = user_ids


class StationAdminLzRemovedEvent:
    def __init__(self, station_id, lz_ids):
        self.station_id = station_id
        self.lz_ids = lz_ids


class StationMemberMemberRemovedEvent:
    def __init__(self, station_id, user_id):
        self.station_id = station_id
        self.user_id = user_id


class StationMemberLzRemovedEvent:
    def __init__(self, station_id, lz_ids):
        self.station_id = station_id
        self.lz_ids = lz_ids


class StationUserWithdrawnEvent:
    def __init__(self, station_id, lz_ids):
        self.stationid = station_id
        self.lz_ids = lz_ids


class StationUserExpelledEvent:
    def __init__(self, stationid):
        self.stationid = stationid


class StationAdminDestroyedEvent:
    def __init__(self, station_id):
        self.station_id = station_id


class StationMemberDestroyedEvent:
    def __init__(self, station_id):
        self.station_id = station_id


class StationUserInviteDestroyedEvent:
    def __init__(self, station_id):
        self.station_id = station_id


class StationUserRequestDestroyedEvent:
    def __init__(self, station_id):
        self.station_id = station_id


class StationAdminLzAddedEvent:
    def __init__(self, station_id, mids):
        self.station_id = station_id
        self.mids = mids


class StationMemberLzAddedEvent:
    def __init__(self, station_id, mids):
        self.station_id = station_id
        self.mids = mids


class StationAdminVolumeAddedEvent:
    def __init__(self, station_id, volumes):
        self.station_id = station_id
        self.volumes = volumes


class StationMemberVolumeAddedEvent:
    def __init__(self, station_id, volumes):
        self.station_id = station_id
        self.volumes = volumes


class StationAdminVolumeHostPathAddedEvent:
    def __init__(self, station_id, volumes):
        self.station_id = station_id
        self.volumes = volumes


class StationMemberVolumeHostPathAddedEvent:
    def __init__(self, station_id, volumes):
        self.station_id = station_id
        self.volumes = volumes


class StationAdminVolumeHostPathRemovedEvent:
    def __init__(self, station_id, volumes):
        self.station_id = station_id
        self.volumes = volumes


class StationMemberVolumeHostPathRemovedEvent:
    def __init__(self, station_id, volumes):
        self.station_id = station_id
        self.volumes = volumes


class StationAdminVolumeRemovedEvent:
    def __init__(self, station_id, volume_names):
        self.station_id = station_id
        self.volume_names = volume_names


class StationMemberVolumeRemovedEvent:
    def __init__(self, station_id, volume_names):
        self.station_id = station_id
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
        max_missions,
        max_users_in_station,
        max_stations,
        max_mission_types,
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
        """
        Resource Policy is a collection of the resource limits for a given role or station

        :param id: UUID of the resource policy
        :type id: str
        :param max_cpu_per_job: Max cpu used per job
        :type max_cpu_per_job: int
        :param max_memory_per_job: Max memory used per job
        :type max_memory_per_job: int
        :param max_gpu_per_job: Max gpu used per job
        :type max_gpu_per_job: int
        :param max_cpu_per_station: Max cpu used per station
        :type max_cpu_per_station: int
        :param max_memory_per_station: Max memory used per station
        :type max_memory_per_station: int
        :param max_gpu_per_station: Max gpu usable per station
        :type max_gpu_per_station: int
        :param max_cpu_global: Max cpu used globally
        :type max_cpu_global: int
        :param max_memory_global: Max memory used globally 
        :type max_memory_global: int
        :param max_gpu_global: Max gpu used globally
        :type max_gpu_global: int
        :param max_missions: Max number of missions allowed
        :type max_missions: int
        :param max_users_in_station: Max number of users in a station 
        :type max_users_in_station: int
        :param max_stations: Max number of stations allowed
        :type max_stations: int
        :param max_mission_types: Max number of mission types allowed
        :type max_mission_types: int
        :param max_cloud_storage_space: Max amount of cloud storage space allowed
        :type max_cloud_storage_space: int
        :param max_spend_per_day: Max amount of credits spent per day
        :type max_spend_per_day: number
        :param max_spend_per_week: Max amount of credits spent per week
        :type max_spend_per_week: number 
        :param max_spend_per_month: Max amount of credits spent per month
        :type max_spend_per_month: number
        :param max_spend_per_year: Max amount of credits spent per year
        :type max_spend_per_year: number 
        :param cpu_credits_per_hour:  cpu credits per hour
        :type cpu_credits_per_hour: number 
        :param memory_credits_per_hour: memory credits per hour
        :type memory_credits_per_hour: number
        :param gpu_credits_per_hour:  gpu credits per hour
        :type gpu_credits_per_hour: number
        :param creation_timestamp: Creation timestamp of the resource policy
        :type creation_timestamp: str
        :param updated_timestamp: Updated timestamp of the resource policy
        :type updated_timestamp: str 
        """
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
        self.max_missions = max_missions
        self.max_users_in_station = max_users_in_station
        self.max_stations = max_stations
        self.max_mission_types = max_mission_types
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
        max_missions=None,
        max_users_in_station=None,
        max_stations=None,
        max_mission_types=None,
        max_cloud_storage_space=None,
        max_spend_per_day=None,
        max_spend_per_week=None,
        max_spend_per_month=None,
        max_spend_per_year=None,
        cpu_credits_per_hour=None,
        memory_credits_per_hour=None,
        gpu_credits_per_hour=None,
    ):
        """
        Update resource policy request

        :param max_cpu_per_job: Max cpu used per job, defaults to None
        :type max_cpu_per_job: int, optional
        :param max_memory_per_job: Max memory used per job, defaults to None
        :type max_memory_per_job: int, optional
        :param max_gpu_per_job: Max gpu used per job, defaults to None
        :type max_gpu_per_job: int, optional
        :param max_cpu_per_station: Max cpu used per station, defaults to None
        :type max_cpu_per_station: int, optional
        :param max_memory_per_station: Max memory used per station, defaults to None
        :type max_memory_per_station: int, optional
        :param max_gpu_per_station: Max gpu usable per station, defaults to None
        :type max_gpu_per_station: int, optional
        :param max_cpu_global: Max cpu used globally, defaults to None
        :type max_cpu_global: int, optional
        :param max_memory_global: Max memory used globally , defaults to None
        :type max_memory_global: int, optional
        :param max_gpu_global: Max gpu used globally, defaults to None
        :type max_gpu_global: int, optional
        :param max_missions: Max number of missions allowed, defaults to None
        :type max_missions: int, optional
        :param max_users_in_station: Max number of users in a station, defaults to None
        :type max_users_in_station: int, optional
        :param max_stations: Max number of stations allowed, defaults to None
        :type max_stations: int, optional
        :param max_mission_types: Max number of mission types allowed, defaults to None
        :type max_mission_types: int, optional
        :param max_cloud_storage_space: Max amount of cloud storage space allowed, defaults to None
        :type max_cloud_storage_space: int, optional
        :param max_spend_per_day: Max amount of credits spent per day, defaults to None
        :type max_spend_per_day: number, optional
        :param max_spend_per_week: Max amount of credits spent per week, defaults to None
        :type max_spend_per_week: number , optional
        :param max_spend_per_month: Max amount of credits spent per month, defaults to None
        :type max_spend_per_month: number, optional
        :param max_spend_per_year: Max amount of credits spent per year, defaults to None
        :type max_spend_per_year: number , optional
        :param cpu_credits_per_hour:  cpu credits per hour, defaults to None
        :type cpu_credits_per_hour: number , optional
        :param memory_credits_per_hour: memory credits per hour, defaults to None
        :type memory_credits_per_hour: number, optional
        :param gpu_credits_per_hour:  gpu credits per hour, defaults to None
        :type gpu_credits_per_hour: number, optional
        """
        self.max_cpu_per_job = max_cpu_per_job
        self.max_memory_per_job = max_memory_per_job
        self.max_gpu_per_job = max_gpu_per_job
        self.max_cpu_per_station = max_cpu_per_station
        self.max_memory_per_station = max_memory_per_station
        self.max_gpu_per_station = max_gpu_per_station
        self.max_cpu_global = max_cpu_global
        self.max_memory_global = max_memory_global
        self.max_gpu_global = max_gpu_global
        self.max_missions = max_missions
        self.max_users_in_station = max_users_in_station
        self.max_stations = max_stations
        self.max_mission_types = max_mission_types
        self.max_cloud_storage_space = max_cloud_storage_space
        self.max_spend_per_day = max_spend_per_day
        self.max_spend_per_week = max_spend_per_week
        self.max_spend_per_month = max_spend_per_month
        self.max_spend_per_year = max_spend_per_year
        self.cpu_credits_per_hour = cpu_credits_per_hour
        self.memory_credits_per_hour = memory_credits_per_hour
        self.gpu_credits_per_hour = gpu_credits_per_hour

    def __str__(self):
        # Return a string of all the non None attributes
        return "Update Resource Policy Request: " + ", ".join([
            "{}={}".format(k, v)
            for k, v in self.__dict__.items() if v is not None
        ])


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
        add_lz=0,
        remove_any_lz=0,
        view_all_jobs=0,
        control_all_jobs=0,
        view_jobs_on_own_lzs=0,
        control_jobs_on_own_lzs=0,
        view_own_jobs=0,
        control_own_jobs=0,
        create_tunnels=None,
        view_complete_activity=0,
        edit_station_policy=0,
        edit_own_lz_policy=0,
        edit_lz_policy=0,
        edit_user_policy=0,
        edit_job_resource_limits=0,
        add_autoscale=0,
        edit_autoscale=0,
        remove_autoscale=0,
        manage_volumes=0,
        reject_user_requests=0,
        allowed_mission_types=None,
    ):
        """
        Create a station role request

        :param name: Name of the role
        :type name: [type]
        :param description: [description]
        :type description: [type]
        :param role_type: [description], defaults to None
        :type role_type: [type], optional
        :param protected_role: [description], defaults to 0
        :type protected_role: int, optional
        :param edit_station_roles: [description], defaults to 0
        :type edit_station_roles: int, optional
        :param assign_user_roles: [description], defaults to 0
        :type assign_user_roles: int, optional
        :param assign_protected_user_roles: [description], defaults to 0
        :type assign_protected_user_roles: int, optional
        :param launch_jobs: [description], defaults to 0
        :type launch_jobs: int, optional
        :param invite_users: [description], defaults to 0
        :type invite_users: int, optional
        :param remove_all_users: [description], defaults to 0
        :type remove_all_users: int, optional
        :param remove_invited_users: [description], defaults to 0
        :type remove_invited_users: int, optional
        :param view_all_users: [description], defaults to 0
        :type view_all_users: int, optional
        :param edit_metadata: [description], defaults to 0
        :type edit_metadata: int, optional
        :param add_lz: [description], defaults to 0
        :type add_lz: int, optional
        :param remove_any_lz: [description], defaults to 0
        :type remove_any_lz: int, optional
        :param view_all_jobs: [description], defaults to 0
        :type view_all_jobs: int, optional
        :param control_all_jobs: [description], defaults to 0
        :type control_all_jobs: int, optional
        :param view_jobs_on_own_lzs: [description], defaults to 0
        :type view_jobs_on_own_lzs: int, optional
        :param control_jobs_on_own_lzs: [description], defaults to 0
        :type control_jobs_on_own_lzs: int, optional
        :param view_own_jobs: [description], defaults to 0
        :type view_own_jobs: int, optional
        :param control_own_jobs: [description], defaults to 0
        :type control_own_jobs: int, optional
        :param create_tunnels: [description], defaults to None
        :type create_tunnels: [type], optional
        :param view_complete_activity: [description], defaults to 0
        :type view_complete_activity: int, optional
        :param edit_station_policy: [description], defaults to 0
        :type edit_station_policy: int, optional
        :param edit_own_lz_policy: [description], defaults to 0
        :type edit_own_lz_policy: int, optional
        :param edit_lz_policy: [description], defaults to 0
        :type edit_lz_policy: int, optional
        :param edit_user_policy: [description], defaults to 0
        :type edit_user_policy: int, optional
        :param edit_job_resource_limits: [description], defaults to 0
        :type edit_job_resource_limits: int, optional
        :param add_autoscale: [description], defaults to 0
        :type add_autoscale: int, optional
        :param edit_autoscale: [description], defaults to 0
        :type edit_autoscale: int, optional
        :param remove_autoscale: [description], defaults to 0
        :type remove_autoscale: int, optional
        :param manage_volumes: [description], defaults to 0
        :type manage_volumes: int, optional
        :param reject_user_requests: [description], defaults to 0
        :type reject_user_requests: int, optional
        :param allowed_mission_types: [description], defaults to None
        :type allowed_mission_types: [type], optional
        """
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
        self.add_lz = add_lz
        self.remove_any_lz = remove_any_lz
        self.view_all_jobs = view_all_jobs
        self.control_all_jobs = control_all_jobs
        self.view_jobs_on_own_lzs = view_jobs_on_own_lzs
        self.control_jobs_on_own_lzs = control_jobs_on_own_lzs
        self.view_own_jobs = view_own_jobs
        self.control_own_jobs = control_own_jobs
        self.view_complete_activity = view_complete_activity
        self.edit_station_policy = edit_station_policy
        self.edit_own_lz_policy = edit_own_lz_policy
        self.edit_lz_policy = edit_lz_policy
        self.edit_user_policy = edit_user_policy
        self.edit_job_resource_limits = edit_job_resource_limits
        self.add_autoscale = add_autoscale
        self.edit_autoscale = edit_autoscale
        self.remove_autoscale = remove_autoscale
        self.manage_volumes = manage_volumes
        self.reject_user_requests = reject_user_requests
        self.create_tunnels = create_tunnels
        self.allowed_mission_types = allowed_mission_types

    def __str__(self):
        return "Create Station Role Request: Name={name}".format(
            name=self.name)


class UpdateStationRoleRequest(CreateStationRoleRequest, object):
    def __init__(
        self,
        name=None,
        description=None,
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
        add_lz=0,
        remove_any_lz=0,
        view_all_jobs=0,
        control_all_jobs=0,
        view_jobs_on_own_lzs=0,
        control_jobs_on_own_lzs=0,
        view_own_jobs=0,
        control_own_jobs=0,
        create_tunnels=None,
        view_complete_activity=0,
        edit_station_policy=0,
        edit_own_lz_policy=0,
        edit_lz_policy=0,
        edit_user_policy=0,
        edit_job_resource_limits=0,
        add_autoscale=0,
        edit_autoscale=0,
        remove_autoscale=0,
        manage_volumes=0,
        reject_user_requests=0,
        allowed_mission_types=None,
    ):
        """
        Update a station role request
        """
        super(UpdateStationRoleRequest, self).__init__(
            name=name,
            description=description,
            role_type=role_type,
            protected_role=protected_role,
            edit_station_roles=edit_station_roles,
            assign_user_roles=assign_user_roles,
            assign_protected_user_roles=assign_protected_user_roles,
            launch_jobs=launch_jobs,
            invite_users=invite_users,
            remove_all_users=remove_all_users,
            remove_invited_users=remove_invited_users,
            view_all_users=view_all_users,
            edit_metadata=edit_metadata,
            add_lz=add_lz,
            remove_any_lz=remove_any_lz,
            view_all_jobs=view_all_jobs,
            control_all_jobs=control_all_jobs,
            view_jobs_on_own_lzs=view_jobs_on_own_lzs,
            control_jobs_on_own_lzs=control_jobs_on_own_lzs,
            view_own_jobs=view_own_jobs,
            create_tunnels=create_tunnels,
            control_own_jobs=control_own_jobs,
            view_complete_activity=view_complete_activity,
            edit_station_policy=edit_station_policy,
            edit_own_lz_policy=edit_own_lz_policy,
            edit_lz_policy=edit_lz_policy,
            edit_user_policy=edit_user_policy,
            edit_job_resource_limits=edit_job_resource_limits,
            add_autoscale=add_autoscale,
            edit_autoscale=edit_autoscale,
            remove_autoscale=remove_autoscale,
            manage_volumes=manage_volumes,
            reject_user_requests=reject_user_requests,
            allowed_mission_types=allowed_mission_types,
        )

    def __str__(self):
        # Return a string of all the non None attributes
        return "Update Station Request: " + ", ".join([
            "{}={}".format(k, v)
            for k, v in self.__dict__.items() if v is not None
        ])


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
        """
        Autoscale settings

        :param id: ID of the autoscale settings
        :type id: str
        :param station_id:  ID of the station
        :type station_id: str
        :param creation_timestamp: The time the autoscale settings was created
        :type creation_timestamp: str
        :param updated_timestamp: Timestamp of the last update
        :type updated_timestamp: str 
        :param increment_amount: Segment increment amount
        :type increment_amount: number
        :param name_prefix: Prefix for the autoscale names
        :type name_prefix: str
        :param computer_provider_id: Computer provider ID
        :type computer_provider_id: str
        :param provision_count: Provision count
        :type provision_count: number
        :param provision_count_min: Minimum provision count 
        :type provision_count_min: number
        :param provision_count_max: Maximum provision count
        :type provision_count_max: number
        :param usage_threshold_up: Usage threshold up
        :type usage_threshold_up: number 
        :param usage_threshold_down: Usage threshold down
        :type usage_threshold_down: number
        :param status: Status of the autoscale settings
        :type status: str 
        """
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
        add_lz,
        remove_any_lz,
        view_all_jobs,
        control_all_jobs,
        view_jobs_on_own_lzs,
        control_jobs_on_own_lzs,
        view_own_jobs,
        control_own_jobs,
        view_complete_activity,
        edit_station_policy,
        edit_own_lz_policy,
        edit_lz_policy,
        edit_user_policy,
        edit_job_resource_limits,
        manage_volumes,
        reject_user_requests,
        create_tunnels,
        allowed_mission_types,
    ):
        """
        Station role object

        :param id: UUID of the station role
        :type id: str
        :param station_id: ID of the station
        :type station_id: str
        :param creation_timestamp: Timestamp of the creation of the station role
        :type creation_timestamp: str
        :param updated_timestamp: Timestamp of the last update of the station role
        :type updated_timestamp: str 
        :param name: Name of the station role
        :type name: str
        :param description: Description of the station role
        :type description: str
        :param role_type: Role type of the station role
        :type role_type: str
        :param protected_role: Protected role of the station role
        :type protected_role: bool
        :param edit_station_roles: Ability to edit station roles 
        :type edit_station_roles: bool
        :param assign_user_roles: Ability to assign user roles
        :type assign_user_roles: bool 
        :param assign_protected_user_roles: Ability to assign protected user roles
        :type assign_protected_user_roles: bool
        :param launch_jobs: Ability to launch jobs
        :type launch_jobs: bool
        :param invite_users: Permission to invite users
        :type invite_users: bool 
        :param remove_all_users: Permission to remove all users
        :type remove_all_users: bool 
        :param remove_invited_users: Permission to remove invited users
        :type remove_invited_users: bool
        :param view_all_users: Permission to view all users
        :type view_all_users: bool
        :param edit_metadata: Ability to edit metadata
        :type edit_metadata: bool
        :param add_lz: Permission to add LZs
        :type add_lz: bool
        :param remove_any_lz: Permission to remove any LZ
        :type remove_any_lz: bool
        :param view_all_jobs: Permission to view all jobs
        :type view_all_jobs: bool
        :param control_all_jobs: Permission to control all jobs
        :type control_all_jobs: bool
        :param view_jobs_on_own_lzs: Permission to view jobs on own LZs
        :type view_jobs_on_own_lzs: bool
        :param control_jobs_on_own_lzs: Permission to control jobs on own LZs
        :type control_jobs_on_own_lzs: bool
        :param view_own_jobs: Permission to view own jobs
        :type view_own_jobs: bool
        :param control_own_jobs: Permission to control own jobs
        :type control_own_jobs: bool 
        :param view_complete_activity: Permission to view complete activity
        :type view_complete_activity: bool
        :param edit_station_policy:  Permission to edit station policy
        :type edit_station_policy: bool
        :param edit_own_lz_policy: Permission to edit own LZ policy
        :type edit_own_lz_policy:bool 
        :param edit_lz_policy: Permission to edit LZ policy
        :type edit_lz_policy: bool
        :param edit_user_policy: Permission to edit user policy
        :type edit_user_policy: bool
        :param edit_job_resource_limits: Permission to edit job resource limits
        :type edit_job_resource_limits: bool
        :param manage_volumes: Permission to manage volumes
        :type manage_volumes: bool
        :param reject_user_requests: Ability to reject user requests
        :type reject_user_requests: bool
        :param create_tunnels: Permission to create tunnels
        :type create_tunnels: bool 
        :param allowed_mission_types: List of allowed mission types
        :type allowed_mission_types: list
        """ """"""
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
        self.add_lz = add_lz
        self.remove_any_lz = remove_any_lz
        self.view_all_jobs = view_all_jobs
        self.control_all_jobs = control_all_jobs
        self.view_jobs_on_own_lzs = view_jobs_on_own_lzs
        self.control_jobs_on_own_lzs = control_jobs_on_own_lzs
        self.view_own_jobs = view_own_jobs
        self.control_own_jobs = control_own_jobs
        self.view_complete_activity = view_complete_activity
        self.edit_station_policy = edit_station_policy
        self.edit_own_lz_policy = edit_own_lz_policy
        self.edit_lz_policy = edit_lz_policy
        self.edit_user_policy = edit_user_policy
        self.edit_job_resource_limits = edit_job_resource_limits
        self.manage_volumes = manage_volumes
        self.reject_user_requests = reject_user_requests
        self.create_tunnels = create_tunnels
        self.allowed_mission_types = allowed_mission_types

    def __str__(self):
        return "{name} role for Station {station_id}".format(
            name=self.name, station_id=self.station_id)

    def __repr__(self):
        return "Role {name}".format(name=self.name)


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
