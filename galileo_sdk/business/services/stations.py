from ..utils.generate_query_str import generate_query_str


class StationsService:
    def __init__(self, stations_repo):
        """
        Station service 

        :param stations_repo: Station repository
        :type stations_repo: StationsRepository
        """
        self._stations_repo = stations_repo

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
        active=True,
        user_ids=None,
        partial_names=None,
        updated=None,
        lz_count_min=None,
        lz_count_max=None,
        lz_status=None,
    ):
        """
        Gets a list of stations filtered by the query parameters

        :param station_ids: Station ids to filter by, default None
        :type station_ids: List[str], optional
        :param names: Station names to filter by
        :type names: List[str], optional
        :param lz_ids: Landing Zone ids to filter by
        :type lz_ids: List[str], optional
        :param user_roles: User roles to filter by
        :type user_roles: List[str], optional
        :param volume_ids: Volume ids to filter by
        :type volume_ids: List[str], optional
        :param descriptions: Descriptions to filter by
        :type descriptions: List[str], optional
        :param page: Page to get
        :type page: int, optional
        :param items: Items per page
        :type items: int, optional
        :param active: Filter by active stations, defaults to True
        :type active: bool, optional
        :param user_ids: User ids to filter by
        :type user_ids: List[str], optional
        :param partial_names: Partial station names to filter by
        :type partial_names: List[str], optional
        :param updated: Filter by updated stations, defaults to None
        :type updated: str, optional
        :param lz_count_min: Filter by stations with at least this many landing zones, defaults to None
        :type lz_count_min: int, optional

        :param lz_count_max: Filter by stations with at most this many landing zones, defaults to None
        :type lz_count_max: int, optional
        :param lz_status: Filter by stations with this landing zone status, defaults to None
        :type lz_status: str, optional
        :return: List of stations
        :rtype: List[Station]

        """
        query = generate_query_str({
            "page": page,
            "items": items,
            "stationids": station_ids,
            "names": names,
            "mids": lz_ids,
            "user_roles": user_roles,
            "volumeids": volume_ids,
            "descriptions": descriptions,
            "active": active,
            "userids": user_ids,
            "partial_names": partial_names,
            "updated": updated,
            "machine_count_min": lz_count_min,
            "machine_count_max": lz_count_max,
            "machine_status": lz_status,
        })

        return self._stations_repo.list_stations(query)

    def get_public_stations(self,
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
                            auto_join_enabled=None):
        """
        Gets a list of public stations filtered by the query parameters

        :param mission_types: Filter by mission_type, defaults to []
        :type mission_types: List[str], optional
        :param mission_cpu_value: Mission cpu value, defaults to None
        :type mission_cpu_value: number, optional
        :param mission_gpu_value: Mission gpu value, defaults to None
        :type mission_gpu_value: number, optional
        :param mission_memory_value: Mission memory value, defaults to None
        :type mission_memory_value: number, optional
        :param min_cpu_per_job: Minimum cpu value, defaults to None
        :type min_cpu_per_job: number, optional
        :param min_gpu_per_job: Minimum gpu per job, defaults to None
        :type min_gpu_per_job: number, optional
        :param min_memory_per_job: Minimum amount of memory per job, defaults to None
        :type min_memory_per_job: number, optional
        :param max_cpu_per_job: Maximum amount of cpu per job, defaults to None
        :type max_cpu_per_job: number, optional
        :param max_gpu_per_job: Maximum amount of GPU per job, defaults to None
        :type max_gpu_per_job: number, optional
        :param min_cpu_credits_per_hour: Minimum amount of cpu credits per hour, defaults to None
        :type min_cpu_credits_per_hour: number, optional
        :param min_gpu_credits_per_hour: Minimum amount of gpu credits per hour, defaults to None
        :type min_gpu_credits_per_hour: number, optional
        :param min_memory_credits_per_hour: Minimum amount of memory credits per hour, defaults to None
        :type min_memory_credits_per_hour: number, optional
        :param max_cpu_credits_per_hour: Maximum amount of cpu credits per hour, defaults to None
        :type max_cpu_credits_per_hour: number, optional
        :param max_gpu_credits_per_hour: Max amount of gpu credits per hour, defaults to None
        :type max_gpu_credits_per_hour: number, optional
        :param max_memory_credits_per_hour: Max memory credits per hour, defaults to None
        :type max_memory_credits_per_hour: number, optional
        :param max_credits_per_hour: Max credits per hour, defaults to None
        :type max_credits_per_hour: number, optional
        :param credits_cost_by_mission: Credits cost by mission, defaults to None
        :type credits_cost_by_mission: number, optional
        :param page: Page of request, defaults to None
        :type page: int, optional
        :param items: Items per page, defaults to None
        :type items: int, optional
        :param allow_tunnels: Filter by stations who allow launchers to create tunnel , defaults to None
        :type allow_tunnels: boolean, optional
        :param auto_join_enabled: Filter stations by auto_join_enabled, defaults to None
        :type auto_join_enabled: bool, optional
        :return: List of public stations
        :rtype: List[PublicStation]
        """
        query = generate_query_str({
            "mission_types": mission_types,
            "mission_cpu_value": mission_cpu_value,
            "mission_gpu_value": mission_gpu_value,
            "mission_memory_per_job": mission_memory_value,
            "min_cput_per_job": min_cpu_per_job,
            "min_gpu_per_job": min_gpu_per_job,
            "min_memory_per_job": min_memory_per_job,
            "max_cpu_per_job": max_cpu_per_job,
            "max_gpu_per_job": max_gpu_per_job,
            "min_cpu_credits_per_hour": min_cpu_credits_per_hour,
            "min_gpu_credits_per_hour": min_gpu_credits_per_hour,
            "min_memory_credits_per_hour": min_memory_credits_per_hour,
            "max_cpu_credits_per_hour": max_cpu_credits_per_hour,
            "max_gpu_credits_per_hour": max_gpu_credits_per_hour,
            "max_memory_credits_per_hour": max_memory_credits_per_hour,
            "max_credits_per_hour": max_credits_per_hour,
            "credits_cost_by_mission": credits_cost_by_mission,
            "page": page,
            "items": items,
            "allow_tunnels": allow_tunnels,
            "auto_join_enabled": auto_join_enabled
        })

        return self._stations_repo.get_public_stations(query)

    def create_station(self, name, description, user_ids=None):
        """
        Creates a new station

        :param name: Name of the station
        :type name: str
        :param description: Short description of the station
        :type description: str
        :param user_ids: List of users invited to station, defaults to None
        :type user_ids: List[str], optional
        :return: Newly created station
        :rtype: Station
        """
        return self._stations_repo.create_station(name, description, user_ids)

    def update_station(self, request):
        """
        Updates a station

        :param request: Update Station Request object
        :type request: UpdateStationRequest
        :return: Updated station
        :rtype: Station
        """
        return self._stations_repo.update_station(request)

    def delete_station(self, station_id):
        """
        Deletes a station

        :param station_id: Station ID of station to delete
        :type station_id: str
        :return: Success 
        :rtype: bool
        """
        return self._stations_repo.delete_station(station_id)

    def get_station_resource_policy(self, station_id):
        """
        Gets a station resource policy

        :param station_id: Station ID of the station to get policy from
        :type station_id: str
        :return: A ResourcePolicy object containing the station's resource policy
        :rtype: ResourcePolicy
        """
        return self._stations_repo.get_station_resource_policy(station_id)

    def update_station_resource_policy(self, station_id, request):
        """
        Updates a station's resource policy

        :param station_id: Station ID of the station to update
        :type station_id: str
        :param request: The new station resource policy
        :type request: str
        :return: A ResourcePolicy object containing the updated station resource policy
        :rtype: ResourcePolicy
        """
        return self._stations_repo.update_station_resource_policy(
            station_id, request)

    def delete_station_resource_policy(self, station_id):
        """
        Deletes a station's resource policy

        :param station_id: Station ID of the station to delete the resource policy from
        :type station_id: str
        :return: Success
        :rtype: bool
        """
        return self._stations_repo.delete_station_resource_policy(station_id)

    def get_self_resource_limits(self, station_id):
        """
        Gets current user's resource limits in a station

        :param station_id: Station ID of the station to get from
        :type station_id: str
        :return: A resource policy object containing the station's resource limits
        :rtype: ResourcePolicy
        """
        return self._stations_repo.get_self_resource_limits(station_id)

    def invite_to_station(self, station_id, user_ids, role_id):
        """
        Invites users to a station

        :param station_id: station ID of the station to invite users to
        :type station_id: str
        :param user_ids: User ids of users to invite
        :type user_ids: List[str]
        :param role_id: Role ID of the role to assign to the users
        :type role_id: str
        :return: Success
        :rtype: bool
        """
        return self._stations_repo.invite_to_station(station_id, user_ids,
                                                     role_id)

    def accept_station_invite(self, station_id):
        """
        Accepts an incoming station invite and updates the user in that station

        :param station_id: Station ID of the station to accept invitation from
        :type station_id: str
        :return: Success
        :rtype: bool
        """
        return self._stations_repo.accept_station_invite(station_id)

    def reject_station_invite(self, station_id):
        """
        Rejects an incoming station invite and updates the user in that station

        :param station_id: Station ID of the station to reject invitation from
        :type station_id: str
        :return: Success
        :rtype: bool
        """
        return self._stations_repo.reject_station_invite(station_id)

    def request_to_join(self, station_id):
        """
        Sends a join request to a station

        :param station_id: Station ID of the station user is requesting to join
        :type station_id: str
        :return: Success
        :rtype: bool
        """
        return self._stations_repo.request_to_join(station_id)

    def approve_request_to_join(self, station_id, user_ids):
        """
        Approves a station request to join from a user

        :param station_id: Station ID of the station to accept the request from
        :type station_id: str
        :param user_ids: List of user_ids to accept
        :type user_ids: List[str]
        :return: Success
        :rtype: bool
        """

        return self._stations_repo.approve_request_to_join(
            station_id, user_ids)

    def reject_request_to_join(self, station_id, user_ids):
        """
        Rejects a station request to join from a user

        :param station_id: Station ID of the station to reject the request from
        :type station_id: str
        :param user_ids: User ids to reject
        :type user_ids: List[str]
        :return: Success
        :rtype: bool
        """
        return self._stations_repo.reject_request_to_join(station_id, user_ids)

    def leave_station(self, station_id):
        """
        Leave a station

        :param station_id: Station ID of the station the user wants to leave 
        :type station_id: str
        :return: Success
        :rtype: bool
        """

        return self._stations_repo.leave_station(station_id)

    def update_station_member(self, station_id, user_id, role_id):
        """
        Updates a station member 

        :param station_id: Station ID of the station to update the member in 
        :type station_id: str
        :param user_id: User ID of the user to update
        :type user_id: str
        :param role_id: Role ID of the role to update
        :type role_id: str
        :return: An updated StationUser object 
        :rtype: StationUser
        """

        return self._stations_repo.update_station_member(
            station_id, user_id, role_id)

    def get_station_user_resource_policy(self, station_id, user_id):
        """
        Gets a users resource policy in a station

        :param station_id: Station ID of the station to get the resource policy for
        :type station_id: str
        :param user_id: User ID of the user to get the resource policy for
        :type user_id: str
        :return: Station user resource policy
        :rtype: ResourcePolicy
        """

        return self._stations_repo.get_station_user_resource_policy(
            station_id, user_id)

    def update_station_user_resource_policy(self, station_id, user_id,
                                            request):
        """
        Update a station user resource policy

        :param station_id: Station ID of the station to update the resource policy for
        :type station_id: str
        :param user_id: User ID of the user to update the resource policy for
        :type user_id: 
        :param request: Resource Policy Request  
        :type request: ResourcePolicyRequest
        :return: Updated Station user resource policy
        :rtype: ResourcePolicy
        """
        return self._stations_repo.update_station_user_resource_policy(
            station_id, user_id, request)

    def delete_station_user_resource_policy(self, station_id, user_id):
        """
        Delete a station user resource policy

        :param station_id: Station ID of the station to delete the resource policy for
        :type station_id: str
        :param user_id: User ID of the user to delete the resource policy for
        :type user_id: str
        :return: Success
        :rtype: bool
        """
        return self._stations_repo.delete_station_user_resource_policy(
            station_id, user_id)

    def get_station_roles(self, station_id, page, items, names, role_ids,
                          user_ids, description):
        """
        Get station roles

        :param station_id: Station ID of the station to get the roles for
        :type station_id: str
        :param query: Query to filter the roles by
        :type query: str
        :return: Station roles
        :rtype: List[StationRole]
        """
        query = generate_query_str({
            "page": page,
            "items": items,
            "names": names,
            "role_ids": role_ids,
            "user_ids": user_ids,
            "description": description,
        })

        return self._stations_repo.get_station_roles(station_id, query)

    def create_station_role(self, station_id, request):
        """
        Create a station role

        :param station_id: Station ID of the station to create the role for
        :type station_id: str
        :param request: Create Station Role Request
        :type request: CreateStationRoleRequest
        :return: New Station Role
        :rtype: StationRole
        """

        return self._stations_repo.create_station_role(station_id, request)

    def update_station_role(self, station_id, station_role_id, request):
        """
        Update a station role

        :param station_id: Station ID of the station to update the role for
        :type station_id: str
        :param station_role_id: Station Role ID of the station role to update
        :type station_role_id: str
        :param request: Update Station Role Request
        :type request: UpdateStationRoleRequest
        :return: The updated Station Role
        :rtype: StationRole
        """
        return self._stations_repo.update_station_role(station_id,
                                                       station_role_id,
                                                       request)

    def get_station_role_resource_policy(self, station_id, role_id):
        """
        Get a station role resource policy

        :param station_id: Station ID of the station to get the resource policy for
        :type station_id: str
        :param role_id: ID of the station role to get the resource policy for
        :type role_id: str
        :return: Station role resource policy
        :rtype: ResourcePolicy 
        """
        return self._stations_repo.get_station_role_resource_policy(
            station_id, role_id)

    def update_station_role_resource_policy(self, station_id, role_id,
                                            request):
        """
        Update a station role resource policy

        :param station_id: Station ID of the station to update the resource policy for
        :type station_id: str
        :param role_id: ID of the station role to update
        :type role_id: str
        :param request: Update Station Role Resource Policy Request
        :type request: ResourcePolicyRequest
        :return: Updated Station Role Resource Policy
        :rtype: ResourcePolicy
        """

        return self._stations_repo.update_station_role_resource_policy(
            station_id, role_id, request)

    def delete_station_role_resource_policy(self, station_id, role_id):
        """
        Delete a station role resource policy

        :param station_id: Station ID of the station to delete the resource policy for
        :type station_id: str
        :param role_id: Role ID of the station role to delete
        :type role_id: str 
        :return: Success
        :rtype: bool
        """
        return self._stations_repo.delete_station_role_resource_policy(
            station_id, role_id)

    def delete_station_role(self, station_id, station_role_id):
        """
        Delete a station role

        :param station_id: Station ID of the station to delete the role for
        :type station_id: str
        :param station_role_id: Station Role ID of the station role to delete
        :type station_role_id: str
        :return: Success
        :rtype: bool
        """

        return self._stations_repo.delete_station_role(station_id,
                                                       station_role_id)

    def remove_member_from_station(self, station_id, user_id):
        """
        Removes a member from a station

        :param station_id: Station Id of the station to remove the member from
        :type station_id: str
        :param user_id: User ID of the user to remove
        :type user_id: str
        :return: Success
        :rtype: bool
        """
        return self._stations_repo.remove_member_from_station(
            station_id, user_id)

    def add_lz_to_station(self, station_id, lz_ids):
        """
        Add LZs to a station

        :param station_id: Station ID of the station to add the LZs to
        :type station_id: str
        :param lz_ids: List of LZ IDs to add to the station
        :type lz_ids: List[str]
        :return: Success
        :rtype: bool
        """
        return self._stations_repo.add_lzs_to_station(station_id, lz_ids)

    def remove_lz_from_station(self, station_id, lz_ids):
        """
        Remove LZs from a station

        :param station_id: Station ID of the station to remove the LZs from
        :type station_id: str
        :param lz_ids: List of LZ IDs to remove from the station
        :type lz_ids: List[str]
        :return: Succss
        :rtype: bool
        """
        return self._stations_repo.remove_lzs_from_station(station_id, lz_ids)

    def get_station_lz_resource_policy(self, station_id, lz_id):
        """
        Get a station LZ resource policy
        :param station_id: Station ID of the station to get the "Z's resource policy for
        :type station_id: str
        :param lz_id: LZ ID of the station LZ to get the resource policy for
        :type lz_id: str
        :return: Resource policy of the station LZ
        :rtype: ResourcePolicy
        """
        return self._stations_repo.get_station_lz_resource_policy(
            station_id, lz_id)

    def update_station_lz_resource_policy(self, station_id, lz_id, request):
        """
        Update a station LZ resource policy

        :param station_id: Station ID of the station to update the resource policy for
        :type station_id: str
        :param lz_id: LZ ID of the station LZ to update resource policy for
        :type lz_id: str
        :param request: Update Station LZ Resource Policy Request
        :type request: ResourcePolicyRequest 
        :return: Updated LZ resource policy
        :rtype: ResourcePolicy
        """
        return self._stations_repo.update_station_lz_resource_policy(
            station_id, lz_id, request)

    def delete_station_lz_resource_policy(self, station_id, lz_id):
        """
        Delete a station LZ resource policy

        :param station_id: Station ID of the station to delete the resource policy for
        :type station_id: str
        :param lz_id: LZ ID of the station LZ to delete resource policy for
        :type lz_id: str
        :return: Success
        :rtype: bool
        """
        return self._stations_repo.delete_station_lz_resource_policy(
            station_id, lz_id)

    def get_station_lz_resource_limits(self, station_id, lz_id):
        """
        Get a station LZ resource limits

        :param station_id: Station ID of the station to get the resource limits for
        :type station_id: str
        :param lz_id: station LZ ID of the station LZ to get the resource limits for
        :type lz_id: str
        :return: Resource limits of the station LZ
        :rtype: ResourcePolicy
        """
        return self._stations_repo.get_station_lz_resource_limits(
            station_id, lz_id)

    def add_volume_to_station(self, station_id, name, mount_point, access):
        """
        Add a volume to a station

        :param station_id: Station ID of the station to add the volume to
        :type station_id: str
        :param name: name of the volume to add
        :type name: str
        :param mount_point: Mount point of the volume to add
        :type mount_point: str
        :param access: Access mode of the volume to add
        :type access: str
        :return: Volume
        :rtype: Volume
        """
        return self._stations_repo.add_volume_to_station(
            station_id, name, mount_point, access)

    def add_host_path_to_volume(self, station_id, volume_id, lz_id, host_path):
        """
        Add a host path to a volume

        :param station_id: Station ID of the station to add the host path to
        :type station_id: str
        :param volume_id: Volume ID of the volume to add the host path to
        :type volume_id: str
        :param lz_id: LZ ID of the LZ to add the host path to
        :type lz_id: str
        :param host_path: Host path of the host path to add
        :type host_path: str
        :return: Host Path to Volume
        :rtype: Volume
        """
        return self._stations_repo.add_host_path_to_volume(
            station_id, volume_id, lz_id, host_path)

    def delete_host_path_from_volume(self, station_id, volume_id,
                                     host_path_id):
        """
        Delete a host path from a volume

        :param station_id: Station ID of the station to delete the host path from
        :type station_id: str 
        :param volume_id: Volume ID of the volume to delete the host path from
        :type volume_id: str
        :param host_path_id: Host path id of the host path to delete
        :type host_path_id: str
        :return: Success
        :rtype: bool
        """
        return self._stations_repo.delete_host_path_from_volume(
            station_id, volume_id, host_path_id)

    def remove_volume_from_station(self, station_id, volume_id):
        """
        Remove a volume from a station

        :param station_id: Station ID of the station to remove the volume from
        :type station_id: str
        :param volume_id: Volume ID of the volume to remove
        :type volume_id: str
        :return: Success
        :rtype: bool
        """
        return self._stations_repo.remove_volume_from_station(
            station_id, volume_id)
