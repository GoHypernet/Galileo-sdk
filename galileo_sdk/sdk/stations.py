from .event import EventsSdk
from ..business.objects import (
    UpdateStationRequest,
    UpdateResourcePolicyRequest,
    CreateStationRoleRequest,
    UpdateStationRoleRequest,
)


class StationsSdk(EventsSdk):
    def __init__(self, stations_service, connector=None, events=None):
        self._stations_service = stations_service
        super(StationsSdk, self).__init__(
            connector=connector,
            events=events,
        )

    def on_new_station(self, func):
        """
        Callback will execute upon a creation of a new station

        :param func: Callable[[NewStationEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_new_station(func)

    def on_station_admin_invite_sent(self, func):
        """
        Callback will execute upon an invite sent
        Emitted to admin of a station

        :param func: Callable[[StationAdminInviteSentEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_invite_sent(func)

    def on_station_user_invite_received(self, func):
        """
        Callback will execute upon a user receiving an invite to a station
        Emitted to the user that receives the invite

        :param func: Callable[[StationUserInviteReceivedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_user_invite_received(func)

    def on_station_admin_invite_accepted(self, func):
        """
        Callback will execute upon an invite to a station being accepted
        Emitted to admin of station

        :param func: Callable[[StationAdminInviteAcceptedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_invite_accepted(func)

    def on_station_member_member_added(self, func):
        """
        Callback will execute upon a member has been added (request has been approved or invitation has been accepted)
        Emitted to all members of a station

        :param func: Callable[[StationMemberMemberEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_member_member_added(func)

    def on_station_user_invite_accepted(self, func):
        """
        Callback will execute upon a user accepting an invite to a station
        Emitted to user who has accepted the invitation

        :param func: Callable[[StationUserInviteAcceptedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_user_invite_accepted(func)

    def on_station_admin_invite_rejected(self, func):
        """
        Callback will execute when an invite to a station has been rejected
        Emitted to admin of station

        :param func: Callable[[StationAdminInviteRejectedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_invite_rejected(func)

    def on_station_user_invite_rejected(self, func):
        """
        Callback will execute when an invite to a station has been rejected
        Emitted to admin of station

        :param func: Callable[[StationUserInviteRejectedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_user_invite_rejected(func)

    def on_station_admin_request_received(self, func):
        """
        Callback will execute when a request to join the station has been received
        Emitted to admin of station

        :param func: Callable[[StationAdminRequestReceivedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_request_received(func)

    def on_station_user_request_sent(self, func):
        """
        Callback will execute when a request to join the station has been sent
        Emitted to user requesting to join the station

        :param func: Callable[[StationUserRequestSentEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_user_request_sent(func)

    def on_station_admin_request_accepted(self, func):
        """
        Callback will execute when a request to join a station has been accepted
        Emitted to admin of station

        :param func: Callable[[StationAdminRequestAcceptedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_request_accepted(func)

    def on_station_user_request_accepted(self, func):
        """
        Callback will execute when a request to join a station has been accepted
        Emitted to user who sent the request

        :param func: Callable[[StationUserRequestAcceptedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_user_request_accepted(func)

    def on_station_admin_request_rejected(
        self,
        func,
    ):
        """
        Callback will execute when a request to join a station has been rejected
        Emitted to admin of station

        :param func: Callable[[StationAdminRequestRejectedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_request_rejected(func)

    def on_station_user_request_rejected(
        self,
        func,
    ):
        """
        Callback will execute when a request to join a station has been rejected
        Emitted to user who sent the request

        :param func: Callable[[StationUserRequestRejectedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_user_request_rejected(func)

    def on_station_admin_member_removed(
        self,
        func,
    ):
        """
        Callback will execute when a member has been removed from a station
        Emitted to admin of station

        :param func: Callable[[StationAdminMemberRemovedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_member_removed(func)

    def on_station_admin_lz_removed(
        self,
        func,
    ):
        """
        Callback will execute when a machine has been removed from a station
        Emitted to admin of station

        :param func: Callable[[StationAdminLzRemovedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_machine_removed(func)

    def on_station_member_member_removed(
        self,
        func,
    ):
        """
        Callback will execute when a member has been removed from a station
        Emitted to members of a station

        :param func: Callable[[StationMemberMemberRemovedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_member_member_removed(func)

    def on_station_member_lz_removed(
        self,
        func,
    ):
        """
        Callback will execute when a lz has been removed from a station
        Emitted to members of a station

        :param func: Callable[[StationMemberLzRemovedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_member_lz_removed(func)

    def on_station_user_withdrawn(
        self,
        func,
    ):
        """
        Callback will execute when a user has withdrawn from the station
        Emitted to user that is withdrawing

        :param func: Callable[[StationUserWithdrawnEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_user_withdrawn(func)

    def on_station_user_expelled(
        self,
        func,
    ):
        """
        Callback will execute when a user has been expelled from the station
        Emitted to user that has been expelled

        :param func: Callable[[StationUserExpelledEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_user_expelled(func)

    def on_station_admin_destroyed(
        self,
        func,
    ):
        """
        Callback will execute when a station has been destroyed
        Emitted to admin of station

        :param func: Callable[[StationAdminDestroyedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_destroyed(func)

    def on_station_member_destroyed(
        self,
        func,
    ):
        """
        Callback will execute when a station has been destroyed
        Emitted to member of station

        :param func: Callable[[StationMemberDestroyedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_member_destroyed(func)

    def on_station_user_invite_destroyed(
        self,
        func,
    ):
        """
        Callback will execute when a station has been destroyed
        Emitted to anyone who received an invite to join the station

        :param func: Callable[[StationUserInviteDestroyedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_user_invite_destroyed(func)

    def on_station_user_request_destroyed(
        self,
        func,
    ):
        """
        Callback will execute when a station has been destroyed
        Emitted to anyone who sent a request to join to the station

        :param func: Callable[[StationUserRequestDestroyedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_user_request_destroyed(func)

    def on_station_admin_lz_added(
        self,
        func,
    ):
        """
        Callback will execute when a lz has been added to the station
        Emitted to admin of station

        :param func: Callable[[StationAdminLzAddedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_lz_added(func)

    def on_station_member_lz_added(
        self,
        func,
    ):
        """
        Callback will execute when a lz has been added to the station
        Emitted to members of station

        :param func: Callable[[StationMemberLzAddedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_member_lz_added(func)

    def on_station_admin_volume_added(self, func):
        """
        Callback will execute when a volume has been added to the station
        Emitted to admin of station

        :param func: Callable[[StationAdminVolumeAddedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_volume_added(func)

    def on_station_member_volume_added(
        self,
        func,
    ):
        """
        Callback will execute when a volume has been added to the station
        Emitted to members of station

        :param func: Callable[[StationMemberVolumeAddedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_member_volume_added(func)

    def on_station_admin_volume_host_path_added(
        self,
        func,
    ):
        """
        Callback will execute when a volume host path has been added
        Emitted to admin of station

        :param func: Callable[[StationAdminVolumeHostPathAddedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_volume_host_path_added(func)

    def on_station_member_volume_host_path_added(
        self,
        func,
    ):
        """
        Callback will execute when a volume host path has been added
        Emitted to members of station

        :param func: Callable[[StationMemberVolumeHostPathAddedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_member_volume_host_path_added(func)

    def on_station_admin_volume_host_path_removed(
        self,
        func,
    ):
        """
        Callback will execute when a volume host path has been removed
        Emitted to admin of station

        :param func: Callable[[StationAdminVolumeHostPathRemovedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_volume_host_path_removed(func)

    def on_station_member_volume_host_path_removed(
        self,
        func,
    ):
        """
        Callback will execute when a volume host path has been removed
        Emitted to members of station

        :param func: Callable[[StationMemberVolumeHostPathRemovedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_member_volume_host_path_removed(func)

    def on_station_admin_volume_removed(
        self,
        func,
    ):
        """
        Callback will execute when a volume has been removed
        Emitted to admin of station

        :param func: Callable[[StationAdminVolumeRemovedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_volume_removed(func)

    def on_station_member_volume_removed(
        self,
        func,
    ):
        """
        Callback will execute when a volume has been removed
        Emitted to members of station

        :param func: Callable[[StationMemberVolumeRemovedEvent], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_member_volume_removed(func)

    def on_station_admin_station_updated(
        self,
        func,
    ):
        """
        Callback will execute when a station has been updated
        Emitted to admin

        :param func: Callable[[StationAdminStationUpdated], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_admin_station_updated(func)

    def on_station_member_station_updated(
        self,
        func,
    ):
        """
        Callback will execute when a station has been updated
        Emitted to members of the station

        :param func: Callable[[StationMemberStationUpdated], None]
        :return: None
        """
        self._set_event_handler("stations")
        self._events.on_station_member_station_updated(func)

    def get_station_by_id(self, station_id):
        """
        Get station by id

        :param station_id: int
        :return: Station

        Example:
            >>> station_id = "my-station-id"
            >>> station = galileo.stations.get_station_by_id(station_id)

        """
        # Get first station with id = station_id, else return None
        return next(iter(self.list_stations(station_ids=[station_id])), None)

    def list_stations(
        self,
        station_ids=None,
        names=None,
        lz_ids=None,
        user_roles=None,
        volume_ids=None,
        descriptions=None,
        page=1,
        items=25,
        active="true",
        user_ids=None,
        partial_names=None,
        updated=None,
        lz_count_min=None,
        lz_count_max=None,
        lz_status=None,
    ):
        """
        Get a filtered list of Galileo Stations that are accessible in your account.
        
        :param station_ids: Optional[List[str]]: Filter based on station ids
        :param names: Optional[List[str]]: Filter based on names
        :param lz_ids: Optional[List[str]]: Filter based on landing zone ids
        :param user_roles: Optional[List[str]]: Filter based on user roles
        :param volume_ids: Optional[List[str]]: Filter based on volumeids
        :param descriptions: Optional[List[str]]: Filter based on descriptions
        :param page: Optional[int]: Page #
        :param items: Optional[int]: Items per page
        :param active: Optional[str]: Filter for all active stations ("true","false"). Default is 'true'.
        :param user_ids: Optional[List[str]]: Filter based on userid
        :param lz_status: Optional[List[str]]
        :param lz_count_max: Optional[int]
        :param lz_count_min: Optional[int]
        :param updated: Optional[str]
        :param partial_names: Optional[List[str]]
        :return: List[Station]

        Example:
            >>> stations = galileo.stations.list_stations()
            >>> for station in stations:
            >>>    print(station.name)
        """
        return self._stations_service.list_stations(
            station_ids=station_ids,
            names=names,
            lz_ids=lz_ids,
            user_roles=user_roles,
            volume_ids=volume_ids,
            descriptions=descriptions,
            page=page,
            items=items,
            active=active,
            user_ids=user_ids,
            partial_names=partial_names,
            updated=updated,
            lz_count_min=lz_count_min,
            lz_count_max=lz_count_max,
            lz_status=lz_status,
        )

    def list_public_stations(
        self,
        mission_types=[],
        mission_cpu_value=None,
        mission_gpu_value=None,
        mission_memory_value=None,
        min_cpu_per_job=None,
        min_gpu_per_job=None,
        min_memory_per_job=None,
        max_cpu_per_job=None,
        max_gpu_per_job=None,
        min_cpu_credits_per_hour=None,
        min_gpu_credits_per_hour=None,
        min_memory_credits_per_hour=None,
        max_cpu_credits_per_hour=None,
        max_gpu_credits_per_hour=None,
        max_memory_credits_per_hour=None,
        max_credits_per_hour=None,
        credits_cost_by_mission=None,
        page=None,
        items=None,
        allow_tunnels=None,
        auto_join_enabled=None,
    ):
        """
        Get a filtered list of public stations
        
        :param mission_types: Optional[List[str]]: Filter based on mission types
        :param mission_cpu_value: Optional[int]: Filter based on mission cpu value
        :param mission_gpu_value: Optional[int]: Filter based on mission gpu value
        :param mission_memory_value: Optional[int]: Filter based on mission memory value
        :param min_cpu_per_job: Optional[int]: Filter based on minimum cpu per job
        :param min_gpu_per_job: Optional[int]: Filter based on minimum gpu per job
        :param min_memory_per_job: Optional[int]: Filter based on minimum memory per job
        :param max_cpu_per_job: Optional[int]: Filter based on maximum cpu per job
        :param max_gpu_per_job: Optional[int]: Filter based on maximum gpu per job
        :param min_cpu_credits_per_hour: Optional[int]: Filter based on minimum cpu credits per hour
        :param min_gpu_credits_per_hour: Optional[int]: Filter based on minimum gpu credits per hour
        :param min_memory_credits_per_hour: Optional[int]: Filter based on minimum memory credits per hour
        :param max_cpu_credits_per_hour: Optional[int]: Filter based on maximum cpu credits per hour
        :param max_gpu_credits_per_hour: Optional[int]: Filter based on maximum gpu credits per hour
        :param max_memory_credits_per_hour: Optional[int]: Filter based on maximum memory credits per hour
        :param max_credits_per_hour: Optional[int]: Filter based on maximum credits per hour
        :param credits_cost_by_mission: Optional[int]: Filter based on credits cost by mission
        :param page: Optional[int]: Page #
        :param items: Optional[int]: Items per page
        :param allow_tunnels: Optional[bool]: Filter based on whether tunnels are allowed
        :param auto_join_enabled: Optional[bool]: Filter based on whether auto join is enabled
        :return: List[PublicStation]

        Example:
            >>> public_stations = galileo.stations.list_stations()
            >>> for station in public_stations:
            >>>    print(station.name)
        """
        return self._stations_service.get_public_stations(
            mission_types=mission_types,
            mission_cpu_value=mission_cpu_value,
            mission_gpu_value=mission_gpu_value,
            mission_memory_value=mission_memory_value,
            min_cpu_per_job=min_cpu_per_job,
            min_gpu_per_job=min_gpu_per_job,
            min_memory_per_job=min_memory_per_job,
            max_cpu_per_job=max_cpu_per_job,
            max_gpu_per_job=max_gpu_per_job,
            min_cpu_credits_per_hour=min_cpu_credits_per_hour,
            min_gpu_credits_per_hour=min_gpu_credits_per_hour,
            min_memory_credits_per_hour=min_memory_credits_per_hour,
            max_cpu_credits_per_hour=max_cpu_credits_per_hour,
            max_gpu_credits_per_hour=max_gpu_credits_per_hour,
            max_memory_credits_per_hour=max_memory_credits_per_hour,
            max_credits_per_hour=max_credits_per_hour,
            credits_cost_by_mission=credits_cost_by_mission,
            page=page,
            items=items,
            allow_tunnels=allow_tunnels,
            auto_join_enabled=auto_join_enabled)

    def create_station(self, name, description="", user_ids=None):
        """
        Create a new station

        :param name: str: name of station
        :param description: str: description of station
        :param user_ids: List[str]: list of members's user ids to invite
        :return: Station

        Example:
            >>> station = galileo.stations.create_station("My Station", description="My Description")
            >>> print(station.name)
        """
        return self._stations_service.create_station(name, description,
                                                     user_ids)

    def invite_to_station(self, station_id, user_ids, role_id):
        """
        Invite user(s) to a station

        :param station_id: str
        :param user_ids: List[str]: list of user's ids to invite
        :param role_id: str: role id to assign to user

        :return: boolean

        Example:
            >>> station_id = "my-station-id" 
            >>> user_ids = ["user-id-1", "user-id-2"] 
            >>> # Get the role id of the launcher role
            >>> role_id = galileo.stations.get_station_roles(station_id, names=["launcher"])[0].id 
            >>> galileo.stations.invite_to_station(station_id, user_ids=user_ids, role_id=role_id)
        """

        return self._stations_service.invite_to_station(
            station_id, user_ids, role_id)

    def accept_station_invite(self, station_id):
        """
        Accept an invitation to join a station

        :param station_id: str
        :return: boolean

        Example:
            >>> station_id = "invited-station-id"
            >>> galileo.stations.accept_station_invite(station_id)

        """
        return self._stations_service.accept_station_invite(station_id)

    def reject_station_invite(self, station_id):
        """
        Reject an invitation to join a station

        :param station_id: str
        :return: boolean

        Example:
            >>> station_id = "invited-station-id"
            >>> galileo.stations.reject_station_invite(station_id)

        """
        return self._stations_service.reject_station_invite(station_id)

    def request_to_join(self, station_id):
        """
        Request to join a station

        :param station_id: str
        :return: boolean

        Example:
            >>> station_id = "desired-station-id"
            >>> galileo.stations.request_to_join(station_id)

        """
        return self._stations_service.request_to_join(station_id)

    def approve_request_to_join(self, station_id, user_ids):
        """
        Admins and owners can approve members to join a station

        :param station_id: str
        :param user_ids: List[str]: list of user ids that will be approved
        :return: boolean

        Example:
            >>> station_id = "my-station-id"
            >>> applicant_ids = ["user-id-1", "user-id-2"]
            >>> galileo.stations.approve_request_to_join(station_id, applicant_ids)

        """
        return self._stations_service.approve_request_to_join(
            station_id, user_ids)

    def reject_request_to_join(self, station_id, user_ids):
        """
        Admins and owners can reject members that want to join a station

        :param station_id: str
        :param user_ids: List[str]: list of user ids that will be rejected
        :return: boolean

        Example:
            >>> station_id = "my-station-id"
            >>> applicant_ids = ["user-id-1", "user-id-2"]
            >>> galileo.stations.reject_request_to_join(station_id, applicant_ids)

        """
        return self._stations_service.reject_request_to_join(
            station_id, user_ids)

    def leave_station(self, station_id):
        """
        Leave a station as a member

        :param station_id: str
        :return: boolean

        Example:
            >>> station_id = "current-station-id"
            >>> galileo.stations.leave_station(station_id)

        """
        return self._stations_service.leave_station(station_id)

    def remove_member_from_station(self, station_id, user_id):
        """
        Remove a member from a station

        :param station_id: str
        :param userid: List[str]: the id of the user you want to remove
        :return: boolean

        Example:
            >>> station_id = "my-station-id"
            >>> user_id = "user-id-1"
            >>> galileo.stations.remove_member_from_station(station_id, user_id)

        """
        return self._stations_service.remove_member_from_station(
            station_id, user_id)

    def delete_station(self, station_id):
        """
        Permanently delete a station

        :param station_id: str
        :return: boolean

        Example:
            >>> station_id = "my-station-id"
            >>> galileo.stations.delete_station(station_id)

        """
        return self._stations_service.delete_station(station_id)

    def add_lz_to_station(self, station_id, lz_ids):
        """
        Add landing zones to a station

        :param station_id: str
        :param lz_ids: List[str]: list of landing zone ids that will be added
        :return: boolean

        Example:
            >>> station_id = "my-station-id"
            >>> lz_ids = ["lz-id-1", "lz-id-2"]
            >>> galileo.stations.add_lz_to_station(station_id, lz_ids)

        """
        return self._stations_service.add_lz_to_station(station_id, lz_ids)

    def remove_lz_from_station(self, station_id, lz_ids):
        """
        Remove landing zones from a station

        :param station_id: str
        :param lz_ids: List[str]: list of landing zone ids that will be added
        :return: boolean

        Example:
            >>> station_id = "my-station-id"
            >>> lz_ids = ["lz-id-1", "lz-id-2"]
            >>> galileo.stations.remove_lz_from_station(station_id, lz_ids)

        """
        return self._stations_service.remove_lz_from_station(
            station_id, lz_ids)

    def add_volume_to_station(self, station_id, name, mount_point, access):
        """
        Add volume to a station

        :param station_id: str
        :param name: str: volume name
        :param mount_point: str: directory path from inside the container
        :param access: EVolumeAccess: read/write access: either 'r' or 'rw'
        :return: Volume

        Example:
            >>> station_id = "my-station-id"
            >>> name = "my-volume-name"
            >>> mount_point = "/mnt/my-volume-name"
            >>> access = EVolumeAccess.READ_WRITE
            >>> volume = galileo.stations.add_volume_to_station(station_id, name, mount_point, access)
            >>> print(volume.name)
        """
        return self._stations_service.add_volume_to_station(
            station_id, name, mount_point, access)

    def add_host_path_to_volume(self, station_id, volume_id, lz_id, host_path):
        """
        Add host path to volume before running a job
        Host path is where the landing zone will store the results of a job

        :param station_id: str
        :param volume_id: tr
        :param lz_id: str: landing zone id
        :param host_path: str: directory path for landing zone
        :return: Volume

        Example:
            >>> station_id = "my-station-id"
            >>> volume_id = "my-volume-id"
            >>> lz_id = "my-lz-id"
            >>> host_path = "/mnt/my-lz-path"
            >>> updated_volume = galileo.stations.add_host_path_to_volume(station_id, volume_id, lz_id, host_path)
            >>> print(updated_volume.host_paths)

        """
        return self._stations_service.add_host_path_to_volume(
            station_id, volume_id, lz_id, host_path)

    def delete_host_path_from_volume(self, station_id, volume_id,
                                     host_path_id):
        """
        Remove a host path
        Host path is where the landing zone will store the results of a job

        :param station_id: str
        :param volume_id: srt
        :param host_path_id: str
        :return: boolean

        Example:
            >>> station_id = "my-station-id"
            >>> volume_id = "my-volume-id"
            >>> lz_id = "my-lz-id"
            >>> host_path = "/mnt/my-lz-path"
            >>> galileo.stations.delete_host_path_from_volume(station_id, volume_id, host_path)

        """
        return self._stations_service.delete_host_path_from_volume(
            station_id, volume_id, host_path_id)

    def remove_volume_from_station(self, station_id, volume_id):
        """
        Remove a volume from station

        :param station_id: str
        :param volume_id: str
        :return: boolean

        Example:
            >>> station_id = "my-station-id"
            >>> volume_id = "my-volume-id"  
            >>> galileo.stations.remove_volume_from_station(station_id, volume_id)

        """
        return self._stations_service.remove_volume_from_station(
            station_id, volume_id)

    def update_station(self,
                       station_id,
                       name=None,
                       description=None,
                       public=None,
                       allow_auto_join=None):
        """
        Update a station

        :param station_id: str
        :param name: str
        :param description: str
        :param public: boolean
        :param allow_auto_join: boolean

        :return: Station

        Example:
            >>> station_id = "my-station-id"
            >>> current_station = galileo.stations.get_station(station_id)
            >>> current_name = current_station.name
            >>> new_name = current_name + "_updated"
            >>> updated_station = galileo.stations.update_station(station_id, name=new_name)
            >>> print(updated_station.name)

        """
        request = UpdateStationRequest(station_id=station_id,
                                       name=name,
                                       description=description,
                                       public=public,
                                       allow_auto_join=allow_auto_join)
        return self._stations_service.update_station(request)

    def get_station_resource_policy(self, station_id):
        """
        Gets the resource policy for a station

        :param station_id: str
        :return: ResourcePolicy

        Example:
            >>> station_id = "my-station-id"
            >>> resource_policy = galileo.stations.get_station_resource_policy(station_id)
            >>> print(resource_policy.max_cpu_per_job)

        """
        return self._stations_service.get_station_resource_policy(station_id)

    def update_station_resource_policy(
        self,
        station_id,
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
        """
        Updates an the resource policy attached to the station. Creates the policy if it does not exist.

        :param station_id: str
        :param max_cpu_per_job: int
        :param max_memory_per_job: int
        :param max_gpu_per_job: int
        :param max_cpu_per_station: int
        :param max_memory_per_station: int
        :param max_gpu_per_station: int
        :param max_cpu_global: int
        :param max_memory_global: int
        :param max_gpu_global: int
        :param max_projects: int
        :param max_users_in_station: int
        :param max_stations: int
        :param max_project_types: int
        :param max_cloud_storage_space: int
        :param max_spend_per_day: int
        :param max_spend_per_week: int
        :param max_spend_per_month: int
        :param max_spend_per_year: int
        :param cpu_credits_per_hour: int
        :param memory_credits_per_hour: int

        :return: ResourcePolicy

        Example:
            >>> station_id = "my-station-id"
            >>> resource_policy = galileo.stations.get_station_resource_policy(station_id)
            >>> new_max_cpu_per_job = resource_policy.max_cpu_per_job + 1
            >>> updated_resource_policy = galileo.stations.update_station_resource_policy(station_id, max_cpu_per_job=new_max_cpu_per_job)
            >>> print(updated_resource_policy.max_cpu_per_job)
        """
        request = UpdateResourcePolicyRequest(
            max_cpu_per_job=max_cpu_per_job,
            max_memory_per_job=max_memory_per_job,
            max_gpu_per_job=max_gpu_per_job,
            max_cpu_per_station=max_cpu_per_station,
            max_memory_per_station=max_memory_per_station,
            max_gpu_per_station=max_gpu_per_station,
            max_cpu_global=max_cpu_global,
            max_memory_global=max_memory_global,
            max_gpu_global=max_gpu_global,
            max_missions=max_projects,
            max_users_in_station=max_users_in_station,
            max_stations=max_stations,
            max_mission_types=max_project_types,
            max_cloud_storage_space=max_cloud_storage_space,
            max_spend_per_day=max_spend_per_day,
            max_spend_per_week=max_spend_per_week,
            max_spend_per_month=max_spend_per_month,
            max_spend_per_year=max_spend_per_year,
            cpu_credits_per_hour=cpu_credits_per_hour,
            memory_credits_per_hour=memory_credits_per_hour,
            gpu_credits_per_hour=gpu_credits_per_hour,
        )
        return self._stations_service.update_station_resource_policy(
            station_id, request)

    def delete_station_resource_policy(self, station_id):
        """
        Deletes the resource policy associated with the station.

        :param station_id: str
        :return: boolean

        Example:
            >>> station_id = "my-station-id"
            >>> galileo.stations.delete_station_resource_policy(station_id)
        """
        return self._stations_service.delete_station_resource_policy(
            station_id)

    def get_self_station_resource_limits(self, station_id):
        """
        Returns the user's calculated (or effective) resource policy in the station.

        :param station_id: str
        :return: Tuple(ResourcePolicy, lz_id)

        Example:
            >>> station_id = "my-station-id"
            >>> resource_policy, lz_id = galileo.stations.get_self_station_resource_limits(station_id)
        """
        return self._stations_service.get_self_resource_limits(station_id)

    def update_station_member(self, station_id, user_id, role_id):
        """
        Updates a user in a station.

        :param station_id: str
        :param user_id: str
        :param role_id: str

        :return: StationUser

        Example:
            >>> station_id = "my-station-id"
            >>> user_id = "my-user-id"
            >>> role_id = galileo.stations.get_station_roles(station_id, names=["admin"])[0].id 
            >>> updated_station_user = galileo.stations.update_station_member(station_id, user_id, role_id)
            >>> print(updated_station_user.role_id)
        """
        return self._stations_service.update_station_member(
            station_id, user_id, role_id)

    def get_station_user_resource_policy(self, station_id, user_id):
        """
        Gets the resource policy for a station user.

        :param station_id: str
        :param user_id: str
        :return: ResourcePolicy

        Example:
            >>> station_id = "my-station-id"
            >>> user_id = "my-user-id"
            >>> resource_policy = galileo.stations.get_station_user_resource_policy(station_id, user_id)
        """
        return self._stations_service.get_station_user_resource_policy(
            station_id, user_id)

    def update_station_user_resource_policy(
        self,
        station_id,
        user_id,
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
        """
        Updates an the resource policy attached to the station user. Creates the policy if it does not exist.

        :param station_id: str
        :param user_id: str
        :param max_cpu_per_job: int
        :param max_memory_per_job: int
        :param max_gpu_per_job: int
        :param max_cpu_per_station: int
        :param max_memory_per_station: int
        :param max_gpu_per_station: int
        :param max_cpu_global: int
        :param max_memory_global: int
        :param max_gpu_global: int
        :param max_projects: int
        :param max_users_in_station: int
        :param max_stations: int
        :param max_project_types: int
        :param max_cloud_storage_space: int
        :param max_spend_per_day: int
        :param max_spend_per_week: int
        :param max_spend_per_month: int
        :param max_spend_per_year: int
        :param cpu_credits_per_hour: int
        :param memory_credits_per_hour: int
        :param gpu_credits_per_hour: int

        :return: ResourcePolicy

        Example:
            >>> station_id = "my-station-id"
            >>> user_id = "my-user-id"
            >>> max_cpu_per_job = 100
            >>> updated_policy = galileo.stations.update_station_user_resource_policy(station_id, user_id, max_cpu_per_job=max_cpu_per_job)
        """
        request = UpdateResourcePolicyRequest(
            max_cpu_per_job=max_cpu_per_job,
            max_memory_per_job=max_memory_per_job,
            max_gpu_per_job=max_gpu_per_job,
            max_cpu_per_station=max_cpu_per_station,
            max_memory_per_station=max_memory_per_station,
            max_gpu_per_station=max_gpu_per_station,
            max_cpu_global=max_cpu_global,
            max_memory_global=max_memory_global,
            max_gpu_global=max_gpu_global,
            max_missions=max_projects,
            max_users_in_station=max_users_in_station,
            max_stations=max_stations,
            max_mission_types=max_project_types,
            max_cloud_storage_space=max_cloud_storage_space,
            max_spend_per_day=max_spend_per_day,
            max_spend_per_week=max_spend_per_week,
            max_spend_per_month=max_spend_per_month,
            max_spend_per_year=max_spend_per_year,
            cpu_credits_per_hour=cpu_credits_per_hour,
            memory_credits_per_hour=memory_credits_per_hour,
            gpu_credits_per_hour=gpu_credits_per_hour,
        )
        return self._stations_service.update_station_user_resource_policy(
            station_id, user_id, request)

    def delete_station_user_resource_policy(self, station_id, user_id):
        """
        Deletes the resource policy associated with the station user.

        :param station_id: str
        :param user_id: str
        :return: boolean

        Example:
            >>> station_id = "my-station-id"
            >>> user_id = "my-user-id"
            >>> galileo.stations.delete_station_user_resource_policy(station_id, user_id)
        """
        return self._stations_service.delete_station_user_resource_policy(
            station_id, user_id)

    def get_station_roles(
        self,
        station_id,
        page=None,
        items=None,
        names=None,
        role_ids=None,
        user_ids=None,
        description=None,
    ):
        """
        Returns a list of StationRole objects that match the query string

        :param station_id:
        :param user_ids:
        :param description:
        :param page: number
        :param items: number
        :param names: str
        :param role_ids: List[str]
        :return: List[StationRole]

        Example:
            >>> station_id = "my-station-id"
            >>> # get admin and launcher roles
            >>> admin_and_launcher_roles = galileo.stations.get_station_roles(station_id, names=["admin", "launcher"])
            >>> # print admin and launcher role ids
            >>> print([role.id for role in admin_and_launcher_roles]) 
        """
        return self._stations_service.get_station_roles(
            station_id, page, items, names, role_ids, user_ids, description)

    def create_station_role(
        self,
        station_id,
        name,
        description="",
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
        view_complete_activity=0,
        edit_station_policy=0,
        edit_own_lz_policy=0,
        edit_lz_policy=0,
        edit_user_policy=0,
        edit_job_resource_limits=0,
        manage_volumes=0,
        reject_user_requests=0,
    ):
        """
        Creates a new role in the station

        :param station_id:
        :param name: str
        :param description: str
        :param protected_role: bool
        :param edit_station_roles: bool
        :param assign_user_roles: bool
        :param assign_protected_user_roles: bool
        :param launch_jobs: bool
        :param invite_users: bool
        :param remove_all_users: bool
        :param remove_invited_users: bool
        :param view_all_users: bool
        :param edit_metadata: bool
        :param add_lz: bool
        :param remove_any_lz: bool
        :param view_all_jobs: bool
        :param control_all_jobs: bool
        :param view_jobs_on_own_lzs: bool
        :param control_jobs_on_own_lzs: bool
        :param view_own_jobs: bool
        :param control_own_jobs: bool
        :param view_complete_activity: bool
        :param edit_station_policy: bool
        :param edit_own_lz_policy: bool
        :param edit_lz_policy: bool
        :param edit_user_policy: bool
        :param edit_job_resource_limits: bool
        :param manage_volumes: bool
        :param reject_user_requests: bool
        :return: StationRole

        Example:
            >>> station_id = "my-station-id"
            >>> name = "my-new-role-name"
            >>> description = "my-role-description"
            >>> manage_volumes = True
            >>> new_role = galileo.stations.create_station_role(station_id, name, description=description, manage_volumes=manage_volumes)
            >>> print(new_role.name)
        """
        request = CreateStationRoleRequest(
            name,
            description=description,
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
            control_own_jobs=control_own_jobs,
            view_complete_activity=view_complete_activity,
            edit_station_policy=edit_station_policy,
            edit_own_lz_policy=edit_own_lz_policy,
            edit_lz_policy=edit_lz_policy,
            edit_user_policy=edit_user_policy,
            edit_job_resource_limits=edit_job_resource_limits,
            manage_volumes=manage_volumes,
            reject_user_requests=reject_user_requests,
        )
        return self._stations_service.create_station_role(station_id, request)

    def update_station_role(self,
                            station_id,
                            station_role_id,
                            name=None,
                            description=None,
                            protected_role=None,
                            edit_station_roles=None,
                            assign_user_roles=None,
                            assign_protected_user_roles=None,
                            launch_jobs=None,
                            invite_users=None,
                            remove_all_users=None,
                            remove_invited_users=None,
                            view_all_users=None,
                            edit_metadata=None,
                            add_lz=None,
                            remove_any_lz=None,
                            view_all_jobs=None,
                            control_all_jobs=None,
                            view_jobs_on_own_lzs=None,
                            control_jobs_on_own_lzs=None,
                            view_own_jobs=None,
                            control_own_jobs=None,
                            view_complete_activity=None,
                            edit_station_policy=None,
                            edit_own_lz_policy=None,
                            edit_lz_policy=None,
                            edit_user_policy=None,
                            edit_job_resource_limits=None,
                            manage_volumes=None,
                            reject_user_requests=None,
                            create_tunnels=None,
                            allowed_mission_types=None):
        """
        Updates an existing role

        :param station_id: str
        :param station_role_id: str
        :param name: str
        :param description: str
        :param protected_role: bool
        :param edit_station_roles: bool
        :param assign_user_roles: bool
        :param assign_protected_user_roles: bool
        :param launch_jobs: bool
        :param invite_users: bool
        :param remove_all_users: bool
        :param remove_invited_users: bool
        :param view_all_users: bool
        :param edit_metadata: bool
        :param add_lz: bool
        :param remove_any_lz: bool
        :param view_all_jobs: bool
        :param control_all_jobs: bool
        :param view_jobs_on_own_lzs: bool
        :param control_jobs_on_own_lzs: bool
        :param view_own_jobs: bool
        :param control_own_jobs: bool
        :param view_complete_activity: bool
        :param edit_station_policy: bool
        :param edit_own_lz_policy: bool
        :param edit_lz_policy: bool
        :param edit_user_policy: bool
        :param edit_job_resource_limits: bool
        :param manage_volumes: bool
        :param reject_user_requests: bool
        :param create_tunnels: bool
        :param allowed_mission_types: list(str)
        :return: StationRole

        Example:
            >>> station_id = "my-station-id"
            >>> station_role_id = "my-station-role-id"
            >>> name = "my-new-role-name"
            >>> updated_role = galileo.stations.update_station_role(station_id, station_role_id, name=name)
            >>> print(updated_role.name)
        """
        request = UpdateStationRoleRequest(
            name=name,
            description=description,
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
            control_own_jobs=control_own_jobs,
            view_complete_activity=view_complete_activity,
            edit_station_policy=edit_station_policy,
            edit_own_lz_policy=edit_own_lz_policy,
            edit_lz_policy=edit_lz_policy,
            edit_user_policy=edit_user_policy,
            edit_job_resource_limits=edit_job_resource_limits,
            manage_volumes=manage_volumes,
            reject_user_requests=reject_user_requests,
            create_tunnels=create_tunnels,
            allowed_mission_types=allowed_mission_types,
        )
        return self._stations_service.update_station_role(
            station_id, station_role_id, request)

    def delete_station_role(self, station_id, role_id):
        """
        Deletes an existing role. All users that have this role will automatically be given the Launcher role.

        :param role_id: str
        :param station_id: str
        :return: boolean

        Example:
            >>> station_id = "my-station-id"
            >>> role_id = "my-role-id"
            >>> galileo.stations.delete_station_role(station_id, role_id)
        """
        return self._stations_service.delete_station_role(station_id, role_id)

    def get_station_role_resource_policy(self, station_id, role_id):
        """
        Gets the resource policy for a station role.

        :param station_id: str
        :param role_id: str
        :return: ResourcePolicy

        Example:
            >>> station_id = "my-station-id"
            >>> role_id = "my-role-id"
            >>> role_resource_policy = galileo.stations.get_station_role_resource_policy(station_id, role_id)
        """
        return self._stations_service.get_station_role_resource_policy(
            station_id, role_id)

    def update_station_role_resource_policy(
        self,
        station_id,
        role_id,
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
        """
        Updates an the resource policy attached to the station role. Creates the policy if it does not exist.

        :param station_id:
        :param role_id:
        :param max_cpu_per_job:
        :param max_memory_per_job:
        :param max_gpu_per_job:
        :param max_cpu_per_station:
        :param max_memory_per_station:
        :param max_gpu_per_station:
        :param max_cpu_global:
        :param max_memory_global:
        :param max_gpu_global:
        :param max_projects:
        :param max_users_in_station:
        :param max_stations:
        :param max_project_types:
        :param max_cloud_storage_space:
        :param max_spend_per_day:
        :param max_spend_per_week:
        :param max_spend_per_month:
        :param max_spend_per_year:
        :param cpu_credits_per_hour:
        :param memory_credits_per_hour:
        :param gpu_credits_per_hour:
        :return: ResourcePolicy

        Example:
            >>> station_id = "my-station-id"
            >>> role_id = "my-role-id"
            >>> max_cpu_per_job = 2
            >>> updated_role_policy = galileo.stations.update_station_role_resource_policy(station_id, role_id, max_cpu_per_job=max_cpu_per_job)
        """
        request = UpdateResourcePolicyRequest(
            max_cpu_per_job=max_cpu_per_job,
            max_memory_per_job=max_memory_per_job,
            max_gpu_per_job=max_gpu_per_job,
            max_cpu_per_station=max_cpu_per_station,
            max_memory_per_station=max_memory_per_station,
            max_gpu_per_station=max_gpu_per_station,
            max_cpu_global=max_cpu_global,
            max_memory_global=max_memory_global,
            max_gpu_global=max_gpu_global,
            max_missions=max_projects,
            max_users_in_station=max_users_in_station,
            max_stations=max_stations,
            max_mission_types=max_project_types,
            max_cloud_storage_space=max_cloud_storage_space,
            max_spend_per_day=max_spend_per_day,
            max_spend_per_week=max_spend_per_week,
            max_spend_per_month=max_spend_per_month,
            max_spend_per_year=max_spend_per_year,
            cpu_credits_per_hour=cpu_credits_per_hour,
            memory_credits_per_hour=memory_credits_per_hour,
            gpu_credits_per_hour=gpu_credits_per_hour,
        )
        return self._stations_service.update_station_role_resource_policy(
            station_id, role_id, request)

    def delete_station_role_resource_policy(self, station_id, role_id):
        """
        Deletes the resource policy associated with the station role.

        :param station_id: str
        :param role_id: str
        :return: bool

        Example:
            >>> station_id = "my-station-id"
            >>> role_id = "my-role-id"
            >>> galileo.stations.delete_station_role_resource_policy(station_id, role_id)
        """
        return self._stations_service.delete_station_role_resource_policy(
            station_id, role_id)

    def get_station_lz_resource_policy(self, station_id, lz_id):
        """
        Gets the resource policy for a station lz.

        :param station_id: str
        :param lz_id: str
        :return: ResourcePolicy

        Example:
            >>> station_id = "my-station-id"
            >>> lz_id = "my-lz-id"
            >>> resource_policy = galileo.stations.get_station_lz_resource_policy(station_id, lz_id)

        """
        return self._stations_service.get_station_lz_resource_policy(
            station_id, lz_id)

    def update_station_lz_resource_policy(
        self,
        station_id,
        lz_id,
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
        """
        Updates an the resource policy attached to the station lz. Creates the policy if it does not exist.

        :param station_id: str
        :param lz_id: str
        :param max_cpu_per_job: int
        :param max_memory_per_job: int
        :param max_gpu_per_job: int
        :param max_cpu_per_station: int
        :param max_memory_per_station: int
        :param max_gpu_per_station: int
        :param max_cpu_global: int
        :param max_memory_global: int
        :param max_gpu_global: int
        :param max_projects: int
        :param max_users_in_station: int
        :param max_stations: int
        :param max_project_types: int
        :param max_cloud_storage_space: int
        :param max_spend_per_day: int
        :param max_spend_per_week: int
        :param max_spend_per_month: int
        :param max_spend_per_year: int
        :param cpu_credits_per_hour: int
        :param memory_credits_per_hour: int
        :param gpu_credits_per_hour: int
        :return: ResourcePolicy

        Example:
            >>> station_id = "my-station-id"
            >>> lz_id = "my-lz-id"
            >>> gpu_credits_per_hour = 100
            >>> lz_policy = galileo.stations.update_station_lz_resource_policy(station_id, lz_id, gpu_credits_per_hour=gpu_credits_per_hour)
        """
        request = UpdateResourcePolicyRequest(
            max_cpu_per_job=max_cpu_per_job,
            max_memory_per_job=max_memory_per_job,
            max_gpu_per_job=max_gpu_per_job,
            max_cpu_per_station=max_cpu_per_station,
            max_memory_per_station=max_memory_per_station,
            max_gpu_per_station=max_gpu_per_station,
            max_cpu_global=max_cpu_global,
            max_memory_global=max_memory_global,
            max_gpu_global=max_gpu_global,
            max_missions=max_projects,
            max_users_in_station=max_users_in_station,
            max_stations=max_stations,
            max_mission_types=max_project_types,
            max_cloud_storage_space=max_cloud_storage_space,
            max_spend_per_day=max_spend_per_day,
            max_spend_per_week=max_spend_per_week,
            max_spend_per_month=max_spend_per_month,
            max_spend_per_year=max_spend_per_year,
            cpu_credits_per_hour=cpu_credits_per_hour,
            memory_credits_per_hour=memory_credits_per_hour,
            gpu_credits_per_hour=gpu_credits_per_hour,
        )
        return self._stations_service.update_station_lz_resource_policy(
            station_id, lz_id, request)

    def delete_station_lz_resource_policy(self, station_id, lz_id):
        """
        Deletes the resource policy associated with the station lz.

        :param station_id: str
        :param lz_id: str
        :return: bool

        Example:
            >>> station_id = "my-station-id"
            >>> lz_id = "my-lz-id"
            >>> galileo.stations.delete_station_lz_resource_policy(station_id, lz_id)
        """
        return self._stations_service.delete_station_lz_resource_policy(
            station_id, lz_id)

    def get_station_lz_resource_limits(self, station_id, lz_id):
        """
        Returns the user's calculated (or effective) resource policy for this particular lz in a station

        :param station_id: str
        :param lz_id: str
        :return: ResourcePolicy

        Example:
            >>> station_id = "my-station-id"
            >>> lz_id = "my-lz-id"
            >>> resource_limits = galileo.stations.get_station_lz_resource_limits(station_id, lz_id)
        """
        return self._stations_service.get_station_lz_resource_limits(
            station_id, lz_id)
