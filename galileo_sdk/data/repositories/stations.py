from galileo_sdk.business.objects import (
    EStationUserRole,
    EVolumeAccess,
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
        self, settings_repository, auth_provider, namespace,
    ):
        super(StationsRepository, self).__init__(
            settings_repository=settings_repository,
            auth_provider=auth_provider,
            namespace=namespace,
        )

    def list_stations(self, query):
        response = self._get("/stations", query=query)
        json = response.json()
        stations = json["stations"]
        return [station_dict_to_station(station) for station in stations]

    def create_station(self, name, description, userids=None):
        response = self._post(
            "/station", {"name": name, "user_ids": userids, "description": description}
        )
        json = response.json()
        station = json["station"]
        return station_dict_to_station(station)

    def update_station(self, request):
        response = self._put(
            "/station/{station_id}".format(station_id=request.station_id),
            {
                "name": request.name,
                "description": request.description,
                "user_ids": request.user_ids,
            },
        )
        json = response.json()
        station = json["station"]
        return station_dict_to_station(station)

    def delete_station(self, station_id):
        response = self._delete("/station/{station_id}".format(station_id=station_id))
        return response.json()  # Boolean

    def get_station_resource_policy(self, station_id):
        response = self._get(
            "/stations/{station_id}/resource_policy".format(station_id=station_id)
        )
        response = response.json()
        policy = response["resource_policy"]
        return resource_policy_dict_to_resource_policy(policy)

    def update_station_resource_policy(self, station_id, request):
        response = self._put(
            "/stations/{station_id}/resource_policy".format(station_id=station_id),
            resource_policy_request_to_dict(request),
        )
        response = response.json()
        policy = response["resource_policy"]
        return resource_policy_dict_to_resource_policy(policy)

    def delete_station_resource_policy(self, station_id):
        response = self._delete(
            "/stations/{station_id}/resource_policy".format(station_id=station_id)
        )
        return response.json()  # Boolean

    def get_self_resource_limits(self, station_id):
        response = self._get(
            "/stations/{station_id}/resource_limits".format(station_id=station_id)
        )
        response = response.json()
        policy = response["resource_policy"]
        machine_id = response["machine_id"]
        return resource_policy_dict_to_resource_policy(policy), machine_id

    def invite_to_station(self, station_id, userids, role_id):
        response = self._post(
            "/station/{station_id}/users/invite".format(station_id=station_id),
            {"userids": userids, "role_id": role_id},
        )
        return response.json()  # Boolean

    def accept_station_invite(self, station_id):
        response = self._put(
            "/station/{station_id}/users/accept".format(station_id=station_id)
        )
        return response.json()  # Boolean

    def reject_station_invite(self, station_id):
        response = self._put(
            "/station/{station_id}/users/reject".format(station_id=station_id)
        )
        return response.json()  # Boolean

    def request_to_join(self, station_id):
        response = self._post(
            "/station/{station_id}/requests".format(station_id=station_id)
        )
        return response.json()  # Boolean

    def approve_request_to_join(self, station_id, userids):
        response = self._put(
            "/station/{station_id}/requests/approve".format(station_id=station_id),
            {"userids": userids},
        )
        return response.json()  # Boolean

    def reject_request_to_join(self, station_id, userids):
        response = self._put(
            "/station/{station_id}/requests/reject".format(station_id=station_id),
            {"userids": userids},
        )
        return response.json()  # Boolean

    def leave_station(self, station_id):
        response = self._put(
            "/station/{station_id}/user/withdraw".format(station_id=station_id)
        )
        return response.json()  # Boolean

    def update_station_member(self, station_id, userid, role_id):
        response = self._put(
            "/station/{station_id}/user/{userid}".format(
                station_id=station_id, userid=userid
            ),
            {"role_id": role_id},
        )
        response = response.json()
        user = response["station_user"]
        return user_dict_to_station_user(user)

    def remove_member_from_station(self, station_id, userid):
        response = self._delete(
            "/station/{station_id}/user/{userid}".format(
                station_id=station_id, userid=userid
            )
        )
        return response.json()  # Boolean

    def get_station_user_resource_policy(self, station_id, userid):
        response = self._get(
            "/stations/{station_id}/users/{user_id}/resource_policy".format(
                station_id=station_id, user_id=userid
            )
        )
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

    def update_station_user_resource_policy(self, station_id, user_id, request):
        response = self._put(
            "/stations/{station_id}/users/{user_id}/resource_policy".format(
                station_id=station_id, user_id=user_id
            ),
            resource_policy_request_to_dict(request),
        )
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

    def delete_station_user_resource_policy(self, station_id, userid):
        response = self._delete(
            "/stations/{station_id}/users/{user_id}/resource_policy".format(
                station_id=station_id, user_id=userid
            )
        )

        return response.json()  # Boolean

    def get_station_roles(self, station_id, query):
        response = self._get(
            "/stations/{station_id}/roles".format(station_id=station_id), query=query
        )
        response = response.json()
        roles = response["roles"]
        return [role_dict_to_station_role(role) for role in roles]

    def create_station_role(self, station_id, request):
        print(station_role_request_to_dict(request))
        response = self._post(
            "/stations/{station_id}/roles".format(station_id=station_id),
            station_role_request_to_dict(request),
        )
        response = response.json()
        role = response["role"]
        return role_dict_to_station_role(role)

    def update_station_role(self, station_id, station_role_id, request):
        response = self._put(
            "/stations/{station_id}/roles/{role_id}".format(
                station_id=station_id, role_id=station_role_id
            ),
            station_role_request_to_dict(request),
        )
        response = response.json()
        role = response["role"]
        return role_dict_to_station_role(role)

    def delete_station_role(self, station_id, station_role_id):
        response = self._delete(
            "/stations/{station_id}/roles/{role_id}".format(
                station_id=station_id, role_id=station_role_id
            )
        )

        return response.json()  # Boolean

    def get_station_role_resource_policy(self, station_id, role_id):
        response = self._get(
            "/stations/{station_id}/roles/{role_id}/resource_policy".format(
                station_id=station_id, role_id=role_id
            )
        )
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

    def update_station_role_resource_policy(self, station_id, role_id, request):
        response = self._put(
            "/stations/{station_id}/roles/{role_id}/resource_policy".format(
                station_id=station_id, role_id=role_id
            ),
            resource_policy_request_to_dict(request),
        )
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

    def delete_station_role_resource_policy(self, station_id, role_id):
        response = self._delete(
            "/stations/{station_id}/roles/{role_id}/resource_policy".format(
                station_id=station_id, role_id=role_id
            )
        )

        return response.json()  # Boolean

    def add_machines_to_station(self, station_id, mids):
        response = self._post(
            "/station/{station_id}/machines".format(station_id=station_id),
            {"mids": mids},
        )
        return response.json()

    def remove_machines_from_station(self, station_id, mids):
        response = self._delete(
            "/station/{station_id}/machines".format(station_id=station_id),
            {"mids": mids},
        )
        return response.json()

    def get_station_machine_resource_policy(self, station_id, machine_id):
        response = self._get(
            "/stations/{station_id}/machines/{machine_id}/resource_policy".format(
                station_id=station_id, machine_id=machine_id
            )
        )
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

    def update_station_machine_resource_policy(self, station_id, machine_id, request):
        response = self._put(
            "/stations/{station_id}/machines/{machine_id}/resource_policy".format(
                station_id=station_id, machine_id=machine_id
            ),
            resource_policy_request_to_dict(request),
        )
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

    def delete_station_machine_resource_policy(self, station_id, machine_id):
        response = self._delete(
            "/stations/{station_id}/machines/{machine_id}/resource_policy".format(
                station_id=station_id, machine_id=machine_id
            )
        )

        return response.json()

    def get_station_machine_resource_limits(self, station_id, machine_id):
        response = self._get(
            "/stations/{station_id}/machines/{machine_id}/resource_limits".format(
                station_id=station_id, machine_id=machine_id
            )
        )
        response = response.json()
        policy = response["resource_policy"]
        if policy is None:
            return None
        return resource_policy_dict_to_resource_policy(policy)

    def add_volumes_to_station(self, station_id, name, mount_point, access):
        response = self._post(
            "/station/{station_id}/volumes".format(station_id=station_id),
            {"name": name, "mount_point": mount_point, "access": access.value},
        )
        json = response.json()
        volume = json["volumes"]
        return volume_dict_to_volume(volume)

    def add_host_path_to_volume(self, station_id, volume_id, mid, host_path):
        response = self._post(
            "/station/{station_id}/volumes/{volume_id}/host_paths".format(
                station_id=station_id, volume_id=volume_id
            ),
            {"mid": mid, "host_path": host_path},
        )
        json = response.json()
        volume = json["volume"]
        return volume_dict_to_volume(volume)

    def delete_host_path_from_volume(self, station_id, volume_id, host_path_id):
        response = self._delete(
            "/station/{station_id}/volumes/{volume_id}/host_paths/{host_path_id}".format(
                station_id=station_id, volume_id=volume_id, host_path_id=host_path_id
            )
        )
        return response.json()

    def remove_volume_from_station(self, station_id, volume_id):
        response = self._delete(
            "/station/{station_id}/volumes/{volume_id}".format(
                station_id=station_id, volume_id=volume_id
            )
        )
        return response.json()


def resource_policy_request_to_dict(request):
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
        "max_projects": request.max_projects,
        "max_users_in_station": request.max_users_in_station,
        "max_stations": request.max_stations,
        "max_project_types": request.max_project_types,
        "max_cloud_storage_space": request.max_cloud_storage_space,
        "max_spend_per_day": request.max_spend_per_day,
        "max_spend_per_week": request.max_spend_per_week,
        "max_spend_per_month": request.max_spend_per_month,
        "max_spend_per_year": request.max_spend_per_year,
        "cpu_credits_per_hour": request.cpu_credits_per_hour,
        "memory_credits_per_hour": request.memory_credits_per_hour,
        "gpu_credits_per_hour": request.gpu_credits_per_hour,
    }


def station_role_request_to_dict(request):
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
        "add_machine": request.add_machine,
        "remove_any_machine": request.remove_any_machine,
        "view_all_jobs": request.view_all_jobs,
        "control_all_jobs": request.control_all_jobs,
        "view_jobs_on_own_machines": request.view_jobs_on_own_machines,
        "control_jobs_on_own_machines": request.control_jobs_on_own_machines,
        "view_own_jobs": request.view_own_jobs,
        "control_own_jobs": request.control_own_jobs,
        "view_complete_activity": request.view_complete_activity,
        "edit_station_policy": request.edit_station_policy,
        "edit_own_machine_policy": request.edit_own_machine_policy,
        "edit_machine_policy": request.edit_machine_policy,
        "edit_user_policy": request.edit_user_policy,
        "edit_job_resource_limits": request.edit_job_resource_limits,
        "add_autoscale": request.add_autoscale,
        "edit_autoscale": request.edit_autoscale,
        "remove_autoscale": request.remove_autoscale,
        "manage_volumes": request.manage_volumes,
        "reject_user_requests": request.reject_user_requests,
    }


def role_dict_to_station_role(role):
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
        add_machine=role["add_machine"],
        remove_any_machine=role["remove_any_machine"],
        view_all_jobs=role["view_all_jobs"],
        control_all_jobs=role["control_all_jobs"],
        view_jobs_on_own_machines=role["view_jobs_on_own_machines"],
        control_jobs_on_own_machines=role["control_jobs_on_own_machines"],
        view_own_jobs=role["view_own_jobs"],
        control_own_jobs=role["control_own_jobs"],
        view_complete_activity=role["view_complete_activity"],
        edit_station_policy=role["edit_station_policy"],
        edit_own_machine_policy=role["edit_own_machine_policy"],
        edit_machine_policy=role["edit_machine_policy"],
        edit_user_policy=role["edit_user_policy"],
        edit_job_resource_limits=role["edit_job_resource_limits"],
        manage_volumes=role["manage_volumes"],
        reject_user_requests=role["reject_user_requests"],
    )


def host_path_dict_to_host_path(hostpath):
    return VolumeHostPath(
        volumehostpathid=hostpath["volumehostpathid"],
        mid=hostpath["mid"],
        host_path=hostpath["host_path"],
    )


def volume_dict_to_volume(volume):
    return Volume(
        volumeid=volume["volumeid"],
        name=volume["name"],
        mount_point=volume["mount_point"],
        stationid=volume["stationid"],
        access=EVolumeAccess(volume["access"]),
        host_paths=[
            host_path_dict_to_host_path(host_path) for host_path in volume["host_paths"]
        ],
    )


def autoscale_settings_dict_to_autoscale_settings(settings):
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
    autoscale_settings = station.get("autoscale_settings", None)
    if autoscale_settings is not None:
        autoscale_settings = [
            autoscale_settings_dict_to_autoscale_settings(settings)
            for settings in autoscale_settings
        ]

    return Station(
        stationid=station["stationid"],
        name=station["name"],
        description=station["description"],
        users=[user_dict_to_station_user(user) for user in station["users"]],
        lz_ids=station["mids"],
        volumes=[volume_dict_to_volume(volume) for volume in station["volumes"]],
        status=station.get("status", None),
        organization_id=station.get("organization_id", None),
        creation_timestamp=station.get("creation_timestamp", None),
        updated_timestamp=station.get("updated_timestamp", None),
        autoscale_settings=autoscale_settings,
    )


def user_dict_to_station_user(user):
    return StationUser(
        stationuserid=user["stationuserid"],
        userid=user["userid"],
        status=EStationUserRole[user["status"]],
        station_id=user.get("station_id", None),
        role_id=user.get("role_id", None),
        creation_timestamp=user.get("creation_timestamp", None),
        updated_timestamp=user.get("updated_timestamp", None),
    )


def resource_policy_dict_to_resource_policy(policy):
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
        max_projects=policy["max_projects"],
        max_users_in_station=policy["max_users_in_station"],
        max_stations=policy["max_stations"],
        max_project_types=policy["max_project_types"],
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
