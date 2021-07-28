from galileo_sdk.business.objects import (
    EStationUserRole,
    EVolumeAccess,
    PublicStation,
    Station,
    StationUser,
    Volume,
    VolumeHostPath,
    ResourcePolicy,
    StationRole,
    AutoscaleSettings,
)
from galileo_sdk.data.repositories import RequestsRepository


class StationsRepository(RequestsRepository):
    def __init__(
        self,
        settings_repository,
        auth_provider,
        namespace,
    ):
        """
        Stations Repository

        :param settings_repository: Settings repository
        :type settings_repository: SettingsRepository
        :param auth_provider: Authentication provider
        :type auth_provider: AuthProvider 
        :param namespace: URL namespace
        :type namespace: str
        """
        super(StationsRepository, self).__init__(
            settings_repository=settings_repository,
            auth_provider=auth_provider,
            namespace=namespace,
        )

    def list_stations(self, query):
        """
        List stations filtered by query

        :param query: Parameters to filter search by
        :type query: str
        :return: Filtered list of stations
        :rtype: List[Station]
        """
        response = self._get("/stations", query=query)
        json = response.json()
        stations = json["stations"]
        return [station_dict_to_station(station) for station in stations]

    def get_public_stations(self, query):
        """
        List public stations filtered by query
 
        :param query: Parameters to filter search by
        :type query: str
        :return: Filtered list of public stations
        :rtype: List[PublicStation]       
        
        """
        response = self._get("/stations/public", query=query)
        json = response.json()
        stations = json["stations"]
        return [
            public_station_dict_to_station(station) for station in stations
        ]

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
        response = self._post("/station", {
            "name": name,
            "user_ids": user_ids,
            "description": description
        })
        json = response.json()
        station = json["station"]
        return station_dict_to_station(station)

    def update_station(self, request):
        """
        Updates a station

        :param request: Update Station Request object
        :type request: UpdateStationRequest
        :return: Updated station
        :rtype: Station
        """
        response = self._put(
            "/station/{station_id}".format(station_id=request.station_id),
            {
                "name": request.name,
                "description": request.description,
                "public": request.public,
                "allow_auto_join": request.allow_auto_join
            },
        )
        json = response.json()
        station = json["station"]
        return station_dict_to_station(station)

    def delete_station(self, station_id):
        """
        Deletes a station

        :param station_id: Station ID of station to delete
        :type station_id: str
        :return: Success 
        :rtype: bool
        """
        response = self._delete(
            "/station/{station_id}".format(station_id=station_id))
        return response.json()  # Boolean

    def get_station_resource_policy(self, station_id):
        """
        Gets a station resource policy

        :param station_id: Station ID of the station to get policy from
        :type station_id: str
        :return: A ResourcePolicy object containing the station's resource policy
        :rtype: ResourcePolicy
        """
        response = self._get("/stations/{station_id}/resource_policy".format(
            station_id=station_id))
        response = response.json()
        policy = response["resource_policy"]
        return resource_policy_dict_to_resource_policy(policy)

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
        response = self._put(
            "/stations/{station_id}/resource_policy".format(
                station_id=station_id),
            resource_policy_request_to_dict(request),
        )
        response = response.json()
        policy = response["resource_policy"]
        return resource_policy_dict_to_resource_policy(policy)

    def delete_station_resource_policy(self, station_id):
        """
        Deletes a station's resource policy

        :param station_id: Station ID of the station to delete the resource policy from
        :type station_id: str
        :return: Success
        :rtype: bool
        """
        response = self._delete(
            "/stations/{station_id}/resource_policy".format(
                station_id=station_id))
        return response.json()  # Boolean

    def get_self_resource_limits(self, station_id):
        """
        Gets current user's resource limits in a station

        :param station_id: Station ID of the station to get from
        :type station_id: str
        :return: A ResourcePolicy object containing the current user's resource policy
        :rtype: ResourcePolicy
        """
        response = self._get("/stations/{station_id}/resource_limits".format(
            station_id=station_id))
        response = response.json()
        policy = response["resource_policy"]
        machine_id = response["machine_id"]
        return resource_policy_dict_to_resource_policy(policy), machine_id

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
        response = self._post(
            "/station/{station_id}/users/invite".format(station_id=station_id),
            {
                "userids": user_ids,
                "role_id": role_id
            },
        )
        return response.json()  # Boolean

    def accept_station_invite(self, station_id):
        """
        Accepts an incoming station invite and updates the user in that station

        :param station_id: Station ID of the station to accept invitation from
        :type station_id: str
        :return: Success
        :rtype: bool
        """
        response = self._put(
            "/station/{station_id}/users/accept".format(station_id=station_id))
        return response.json()  # Boolean

    def reject_station_invite(self, station_id):
        """
        Rejects an incoming station invite and updates the user in that station

        :param station_id: Station ID of the station to reject invitation from
        :type station_id: str
        :return: Success
        :rtype: bool
        """
        response = self._put(
            "/station/{station_id}/users/reject".format(station_id=station_id))
        return response.json()  # Boolean

    def request_to_join(self, station_id):
        """
        Sends a join request to a station

        :param station_id: Station ID of the station user is requesting to join
        :type station_id: str
        :return: Success
        :rtype: bool
        """
        response = self._post(
            "/station/{station_id}/requests".format(station_id=station_id))
        return response.json()  # Boolean

    def approve_request_to_join(self, station_id, user_ids):
        """
        Approves a station request to join from a user

        :param station_id: Station ID of the station to accept the request from
        :type station_id: str
        :param user_ids: List of user_ids to accept
        :type userids: List[str]
        :return: Success
        :rtype: bool
        """
        response = self._put(
            "/station/{station_id}/requests/approve".format(
                station_id=station_id),
            {"userids": user_ids},
        )
        return response.json()  # Boolean

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
        response = self._put(
            "/station/{station_id}/requests/reject".format(
                station_id=station_id),
            {"userids": user_ids},
        )
        return response.json()  # Boolean

    def leave_station(self, station_id):
        """
        Leave a station

        :param station_id: Station ID of the station the user wants to leave 
        :type station_id: str
        :return: Success
        :rtype: bool
        """
        response = self._put("/station/{station_id}/user/withdraw".format(
            station_id=station_id))
        return response.json()  # Boolean

    def update_station_member(self, station_id, user_id, role_id):
        """
        Updates a station member 

        :param station_id: Station ID of the station to update the member in 
        :type station_id: str
        :param user_id: User ID of the user to update
        :type userid: str
        :param role_id: Role ID of the role to update
        :type role_id: str
        :return: An updated StationUser object 
        :rtype: StationUser
        """
        response = self._put(
            "/station/{station_id}/user/{userid}".format(station_id=station_id,
                                                         userid=user_id),
            {"role_id": role_id},
        )
        response = response.json()
        user = response["station_user"]
        return user_dict_to_station_user(user)

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
        response = self._delete(
            "/station/{station_id}/user/{userid}/delete".format(
                station_id=station_id, userid=user_id))
        return response.json()  # Boolean

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
        response = self._get(
            "/stations/{station_id}/users/{user_id}/resource_policy".format(
                station_id=station_id, user_id=user_id))
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

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
        response = self._put(
            "/stations/{station_id}/users/{user_id}/resource_policy".format(
                station_id=station_id, user_id=user_id),
            resource_policy_request_to_dict(request),
        )
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

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
        response = self._delete(
            "/stations/{station_id}/users/{user_id}/resource_policy".format(
                station_id=station_id, user_id=user_id))

        return response.json()  # Boolean

    def get_station_roles(self, station_id, query):
        """
        Get station roles

        :param station_id: Station ID of the station to get the roles for
        :type station_id: str
        :param query: Query to filter the roles by
        :type query: str
        :return: Station roles
        :rtype: List[StationRole]
        """
        response = self._get(
            "/stations/{station_id}/roles".format(station_id=station_id),
            query=query)
        response = response.json()
        roles = response["roles"]
        return [role_dict_to_station_role(role) for role in roles]

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
        print(station_role_request_to_dict(request))
        response = self._post(
            "/stations/{station_id}/roles".format(station_id=station_id),
            station_role_request_to_dict(request),
        )
        response = response.json()
        role = response["role"]
        return role_dict_to_station_role(role)

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
        response = self._put(
            "/stations/{station_id}/roles/{role_id}".format(
                station_id=station_id, role_id=station_role_id),
            station_role_request_to_dict(request),
        )
        response = response.json()
        role = response["role"]
        return role_dict_to_station_role(role)

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
        response = self._delete(
            "/stations/{station_id}/roles/{role_id}".format(
                station_id=station_id, role_id=station_role_id))

        return response.json()  # Boolean

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
        response = self._get(
            "/stations/{station_id}/roles/{role_id}/resource_policy".format(
                station_id=station_id, role_id=role_id))
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

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
        response = self._put(
            "/stations/{station_id}/roles/{role_id}/resource_policy".format(
                station_id=station_id, role_id=role_id),
            resource_policy_request_to_dict(request),
        )
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

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
        response = self._delete(
            "/stations/{station_id}/roles/{role_id}/resource_policy".format(
                station_id=station_id, role_id=role_id))

        return response.json()  # Boolean

    def add_lzs_to_station(self, station_id, lz_ids):
        """
        Add LZs to a station

        :param station_id: Station ID of the station to add the LZs to
        :type station_id: str
        :param lz_ids: List of LZ IDs to add to the station
        :type lz_ids: List[str]
        :return: Success
        :rtype: bool
        """
        response = self._post(
            "/station/{station_id}/machines".format(station_id=station_id),
            {"mids": lz_ids},
        )
        return response.json()

    def remove_lzs_from_station(self, station_id, lz_ids):
        """
        Remove LZs from a station

        :param station_id: Station ID of the station to remove the LZs from
        :type station_id: str
        :param lz_ids: List of LZ IDs to remove from the station
        :type lz_ids: List[str]
        :return: Success    
        :rtype: bool
        """
        response = self._delete(
            "/station/{station_id}/machines".format(station_id=station_id),
            {"mids": lz_ids},
        )
        return response.json()

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
        response = self._get(
            "/stations/{station_id}/machines/{machine_id}/resource_policy".
            format(station_id=station_id, machine_id=lz_id))
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

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
        response = self._put(
            "/stations/{station_id}/machines/{machine_id}/resource_policy".
            format(station_id=station_id, machine_id=lz_id),
            resource_policy_request_to_dict(request),
        )
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

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
        response = self._delete(
            "/stations/{station_id}/machines/{machine_id}/resource_policy".
            format(station_id=station_id, machine_id=lz_id))

        return response.json()

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
        response = self._get(
            "/stations/{station_id}/machines/{machine_id}/resource_limits".
            format(station_id=station_id, machine_id=lz_id))
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

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
        response = self._post(
            "/station/{station_id}/volumes".format(station_id=station_id),
            {
                "name": name,
                "mount_point": mount_point,
                "access": access.value
            },
        )
        json = response.json()
        volume = json["volumes"]
        return volume_dict_to_volume(volume)

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
        response = self._post(
            "/station/{station_id}/volumes/{volume_id}/host_paths".format(
                station_id=station_id, volume_id=volume_id),
            {
                "mid": lz_id,
                "host_path": host_path
            },
        )
        json = response.json()
        volume = json["volume"]
        return volume_dict_to_volume(volume)

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
        response = self._delete(
            "/station/{station_id}/volumes/{volume_id}/host_paths/{host_path_id}"
            .format(station_id=station_id,
                    volume_id=volume_id,
                    host_path_id=host_path_id))
        return response.json()

    # TODO - Swagger outdated/wrong response
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
        response = self._delete(
            "/station/{station_id}/volumes/{volume_id}".format(
                station_id=station_id, volume_id=volume_id))
        return response.json()


def station_role_request_to_dict(request):
    """
    Convert a StationRoleRequest to a dict.

    :param request: StationRoleRequest to convert to a HTTP Body
    :type request: StationRoleRequest
    :return: Dict representation of the StationRoleRequest
    :rtype: Dict 
    """
    return {
        "name": request.name,
        "description": request.description,
        "role_type": request.role_type,
        "protected_role": request.protected_role,
        "edit_station_roles": request.edit_station_roles,
        "assign_user_roles": request.assign_user_roles,
        "assign_protected_user_roles": request.assign_protected_user_roles,
        "launch_jobs": request.launch_jobs,
        "invite_users": request.invite_users,
        "remove_all_users": request.remove_all_users,
        "remove_invited_users": request.remove_invited_users,
        "view_all_users": request.view_all_users,
        "edit_metadata": request.edit_metadata,
        "add_machine": request.add_lz,
        "remove_any_machine": request.remove_any_lz,
        "view_all_jobs": request.view_all_jobs,
        "control_all_jobs": request.control_all_jobs,
        "view_jobs_on_own_machines": request.view_jobs_on_own_lzs,
        "control_jobs_on_own_machines": request.control_jobs_on_own_lzs,
        "view_own_jobs": request.view_own_jobs,
        "control_own_jobs": request.control_own_jobs,
        "view_complete_activity": request.view_complete_activity,
        "edit_station_policy": request.edit_station_policy,
        "edit_own_machine_policy": request.edit_own_lz_policy,
        "edit_machine_policy": request.edit_lz_policy,
        "edit_user_policy": request.edit_user_policy,
        "edit_job_resource_limits": request.edit_job_resource_limits,
        "add_autoscale": request.add_autoscale,
        "edit_autoscale": request.edit_autoscale,
        "remove_autoscale": request.remove_autoscale,
        "manage_volumes": request.manage_volumes,
        "reject_user_requests": request.reject_user_requests,
        "create_tunnels": request.create_tunnels,
    }


def role_dict_to_station_role(role):
    """
    Convert a dict to a StationRole object

    :param role: Station role dict response returned by the API
    :type role: Dict
    :return: Station role object
    :rtype: StationRole
    """
    return StationRole(
        id=role["id"],
        station_id=role["station_id"],
        creation_timestamp=role["creation_timestamp"],
        updated_timestamp=role["updated_timestamp"],
        name=role["name"],
        description=role["description"],
        role_type=role["role_type"],
        protected_role=role["protected_role"],
        edit_station_roles=role["edit_station_roles"],
        assign_user_roles=role["assign_user_roles"],
        assign_protected_user_roles=role["assign_protected_user_roles"],
        launch_jobs=role["launch_jobs"],
        invite_users=role["invite_users"],
        remove_all_users=role["remove_all_users"],
        remove_invited_users=role["remove_invited_users"],
        view_all_users=role["view_all_users"],
        edit_metadata=role["edit_metadata"],
        add_lz=role["add_machine"],
        remove_any_lz=role["remove_any_machine"],
        view_all_jobs=role["view_all_jobs"],
        control_all_jobs=role["control_all_jobs"],
        view_jobs_on_own_lzs=role["view_jobs_on_own_machines"],
        control_jobs_on_own_lzs=role["control_jobs_on_own_machines"],
        view_own_jobs=role["view_own_jobs"],
        control_own_jobs=role["control_own_jobs"],
        view_complete_activity=role["view_complete_activity"],
        edit_station_policy=role["edit_station_policy"],
        edit_own_lz_policy=role["edit_own_machine_policy"],
        edit_lz_policy=role["edit_machine_policy"],
        edit_user_policy=role["edit_user_policy"],
        edit_job_resource_limits=role["edit_job_resource_limits"],
        manage_volumes=role["manage_volumes"],
        reject_user_requests=role["reject_user_requests"],
        create_tunnels=role["create_tunnels"],
        allowed_mission_types=["allowed_mission_types"],
    )


def host_path_dict_to_host_path(hostpath):
    """
    Convert a host path from the API to a ``VolumeHostPath`` object.

    :param hostpath: A dictionary of host path attributes.
    :type hostpath: Dict
    :return: VolumeHostPath object
    :rtype: VolumeHostPath
    """
    return VolumeHostPath(
        volume_hostpath_id=hostpath["volumehostpathid"],
        lz_id=hostpath["mid"],
        host_path=hostpath["host_path"],
    )


def volume_dict_to_volume(volume):
    """
    Convert a volume dict to a Volume object.

    :param volume: Volume dict response from the API.
    :type volume: Dict
    :return: Volume object.
    :rtype: Volume
    """
    return Volume(
        volume_id=volume["volumeid"],
        name=volume["name"],
        mount_point=volume["mount_point"],
        station_id=volume["stationid"],
        access=EVolumeAccess(volume["access"]),
        host_paths=[
            host_path_dict_to_host_path(host_path)
            for host_path in volume["host_paths"]
        ],
    )


def autoscale_settings_dict_to_autoscale_settings(settings):
    """
    Converts a dictionary of autoscale settings into a AutoscaleSettings object.

    :param settings: settings dictionary
    :type settings: Dict
    :return: AutoScaleSettings object
    :rtype: AutoScaleSettings
    """
    return AutoscaleSettings(
        id=settings["id"],
        station_id=settings["station_id"],
        creation_timestamp=settings["creation_timestamp"],
        updated_timestamp=settings["updated_timestamp"],
        increment_amount=settings["increment_amount"],
        name_prefix=settings["name_prefix"],
        computer_provider_id=settings["computer_provider_id"],
        provision_count=settings["provision_count"],
        provision_count_min=settings["provision_count_min"],
        provision_count_max=settings["provision_count_max"],
        usage_threshold_up=settings["usage_threshold_up"],
        usage_threshold_down=settings["usage_threshold_down"],
        status=settings["status"],
    )


def station_dict_to_station(station):
    """
    Convert a station dict to a Station object.

    :param station: Station Response dict
    :type station: Dict
    :return: Station object
    :rtype: Station
    """
    autoscale_settings = station.get("autoscale_settings", None)
    if autoscale_settings is not None:
        autoscale_settings = [
            autoscale_settings_dict_to_autoscale_settings(settings)
            for settings in autoscale_settings
        ]
    return Station(
        station_id=station["stationid"],
        name=station["name"],
        description=station["description"],
        users=[user_dict_to_station_user(user) for user in station["users"]],
        lz_ids=station["mids"],
        volumes=[
            volume_dict_to_volume(volume) for volume in station["volumes"]
        ],
        status=station.get("status", None),
        machine_summaries=station.get("machine_summaries", None),
        universe_id=station.get("organization_id", None),
        creation_timestamp=station.get("creation_timestamp", None),
        updated_timestamp=station.get("updated_timestamp", None),
        allow_auto_join=station.get("allow_auto_join", None),
        public=station.get("public", None),
        autoscale_settings=station.get("autoscale_settings", None),
        crew_ids=station.get("crew_ids", None),
    )


def public_station_dict_to_station(station):
    """
    Convert a public station dict to a Station object.

    :param station: Public Station Response dict
    :type station: Dict
    :return: Public Station object
    :rtype: PublicStation
    """
    return PublicStation(
        station_id=station["stationid"],
        name=station["name"],
        description=station["description"],
        allow_auto_join=station["allow_auto_join"],
        creation_timestamp=station.get("creation_timestamp", None),
        updated_timestamp=station.get("updated_timestamp", None),
        allowed_mission_types=station.get("allowed_mission_types", None),
        jobs_in_queue_count=station.get("jobs_in_queue", None),
        member_count=station.get("member_count", None),
        lz_id_count=station.get("mid_count", None),
        resource_policy=station.get("resource_policy", None),
        user_count=station.get("user_count", None),
        user_status=station.get("user_status", None),
        volume_count=station.get("volume_count", None))


def user_dict_to_station_user(user):
    """
    Convert a user dict to a StationUser

    :param user: Station user response
    :type user: Dict
    :return: StationUser object
    :rtype: StationUser
    """
    return StationUser(
        stationuser_id=user["stationuserid"],
        user_id=user["userid"],
        status=EStationUserRole[user["status"]],
        station_id=user.get("station_id", None),
        role_id=user.get("role_id", None),
        creation_timestamp=user.get("creation_timestamp", None),
        updated_timestamp=user.get("updated_timestamp", None),
    )


def resource_policy_dict_to_resource_policy(policy):
    """
    Convert a resource policy dict to a ResourcePolicy object.

    :param policy: Policy Dict Response
    :type policy: Dict 
    :return: Resource Policy Object
    :rtype: ResourcePolicy
    """
    return ResourcePolicy(
        id=policy.get("id", None),
        max_cpu_per_job=policy["max_cpu_per_job"],
        max_memory_per_job=policy["max_memory_per_job"],
        max_gpu_per_job=policy["max_gpu_per_job"],
        max_cpu_per_station=policy["max_cpu_per_station"],
        max_memory_per_station=policy["max_memory_per_station"],
        max_gpu_per_station=policy["max_gpu_per_station"],
        max_cpu_global=policy["max_cpu_global"],
        max_memory_global=policy["max_memory_global"],
        max_gpu_global=policy["max_gpu_global"],
        max_missions=policy["max_projects"],
        max_users_in_station=policy["max_users_in_station"],
        max_stations=policy["max_stations"],
        max_mission_types=policy["max_project_types"],
        max_cloud_storage_space=policy["max_cloud_storage_space"],
        max_spend_per_day=policy.get("max_spend_per_day", None),
        max_spend_per_week=policy.get("max_spend_per_week", None),
        max_spend_per_month=policy.get("max_spend_per_month", None),
        max_spend_per_year=policy.get("max_spend_per_year", None),
        cpu_credits_per_hour=policy.get("cpu_credits_per_hour", None),
        memory_credits_per_hour=policy.get("memory_credits_per_hour", None),
        gpu_credits_per_hour=policy.get("gpu_credits_per_hour", None),
        creation_timestamp=policy.get("creation_timestamp", None),
        updated_timestamp=policy.get("updated_timestamp", None),
    )


def resource_policy_request_to_dict(request):
    """
    Converts a ResourcePolicyRequest to a dict.

    :param request: Resource Policy Request
    :type request: ResourcePolicyRequest
    :return: A dict representation of the Resource Policy Request for an HTTP Request
    :rtype: Dict
    """
    return {
        "max_cpu_per_job": request.max_cpu_per_job,
        "max_memory_per_job": request.max_memory_per_job,
        "max_gpu_per_job": request.max_gpu_per_job,
        "max_cpu_per_station": request.max_cpu_per_station,
        "max_memory_per_station": request.max_memory_per_station,
        "max_gpu_per_station": request.max_gpu_per_station,
        "max_cpu_global": request.max_cpu_global,
        "max_memory_global": request.max_memory_global,
        "max_gpu_global": request.max_gpu_global,
        "max_projects": request.max_missions,
        "max_users_in_station": request.max_users_in_station,
        "max_stations": request.max_stations,
        "max_project_types": request.max_mission_types,
        "max_cloud_storage_space": request.max_cloud_storage_space,
        "max_spend_per_day": request.max_spend_per_day,
        "max_spend_per_week": request.max_spend_per_week,
        "max_spend_per_month": request.max_spend_per_month,
        "max_spend_per_year": request.max_spend_per_year,
        "cpu_credits_per_hour": request.cpu_credits_per_hour,
        "memory_credits_per_hour": request.memory_credits_per_hour,
        "gpu_credits_per_hour": request.gpu_credits_per_hour,
    }