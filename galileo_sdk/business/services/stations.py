from ..utils.generate_query_str import generate_query_str


class StationsService:
    def __init__(self, stations_repo):
        self._stations_repo = stations_repo

    def list_stations(
        self,
        stationids=None,
        names=None,
        mids=None,
        user_roles=None,
        volumeids=None,
        descriptions=None,
        page=1,
        items=25,
        active=True,
        userids=None,
        partial_names=None,
        updated=None,
        machine_count_min=None,
        machine_count_max=None,
        machine_status=None
    ):
        query = generate_query_str(
            {
                "page": page,
                "items": items,
                "stationids": stationids,
                "names": names,
                "mids": mids,
                "user_roles": user_roles,
                "volumeids": volumeids,
                "descriptions": descriptions,
                "active": active,
                "userids": userids,
                "partial_names": partial_names,
                "updated": updated,
                "machine_count_min": machine_count_min,
                "machine_count_max": machine_count_max,
                "machine_status": machine_status
            }
        )

        return self._stations_repo.list_stations(query)

    def create_station(self, name, description, userids=None):
        return self._stations_repo.create_station(name, description, userids)

    def update_station(self, request):
        return self._stations_repo.update_station(request)

    def delete_station(self, station_id):
        return self._stations_repo.delete_station(station_id)

    def get_station_resource_policy(self, station_id):
        return self._stations_repo.get_station_resource_policy(station_id)

    def update_station_resource_policy(self, request):
        return self._stations_repo.update_station_resource_policy(request)

    def delete_station_resource_policy(self, station_id):
        return self._stations_repo.delete_station_resource_policy(station_id)

    def get_self_resource_limits(self, station_id):
        return self._stations_repo.get_self_resource_limits(station_id)

    def invite_to_station(self, station_id, userids, role_id):
        return self._stations_repo.invite_to_station(station_id, userids, role_id)

    def accept_station_invite(self, station_id):
        return self._stations_repo.accept_station_invite(station_id)

    def reject_station_invite(self, station_id):
        return self._stations_repo.reject_station_invite(station_id)

    def request_to_join(self, station_id):
        return self._stations_repo.request_to_join(station_id)

    def approve_request_to_join(self, station_id, userids):
        return self._stations_repo.approve_request_to_join(station_id, userids)

    def reject_request_to_join(self, station_id, userids):
        return self._stations_repo.reject_request_to_join(station_id, userids)

    def leave_station(self, station_id):
        return self._stations_repo.leave_station(station_id)

    def update_station_member(self, station_id, userid, role_id):
        return self._stations_repo.update_station_member(station_id, userid, role_id)

    def get_station_user_resource_policy(self, station_id, userid):
        return self._stations_repo.get_station_resource_policy(station_id, userid)

    def update_station_user_resource_policy(self, request):
        return self._stations_repo.update_station_resource_policy(request)

    def delete_station_user_resource_policy(self, station_id, userid):
        return self._stations_repo.delete_station_user_resource_policy(station_id, userid)

    def get_station_roles(self, page, items, names, role_types):
        query = generate_query_str({
            "page": page,
            "items": items,
            "names": names,
            "role_types": role_types
        })

        return self._stations_repo.get_station_roles(query)

    def create_station_role(self, request):
        return self._stations_repo.create_station(request)

    def update_station_role(self, request):
        return self._stations_repo.update_station_role(request)

    def get_station_role_resource_policy(self, station_id, role_id):
        return self._stations_repo.get_station_role_resource_policy(station_id, role_id)

    def update_station_role_resource_policy(self, request):
        return self._stations_repo.update_station_role_resource_policy(request)

    def delete_station_role_resource_policy(self, station_id, role_id):
        return self._stations_repo.delete_station_role_resource_policy(station_id, role_id)

    def delete_station_role(self, request):
        return self._stations_repo.delete_station_role(request)

    def remove_member_from_station(self, station_id, userid):
        return self._stations_repo.remove_member_from_station(station_id, userid)

    def add_machines_to_station(self, station_id, mids):
        return self._stations_repo.add_machines_to_station(station_id, mids)

    def remove_machines_from_station(self, station_id, mids):
        return self._stations_repo.remove_machines_from_station(station_id, mids)

    def get_station_machine_resource_policy(self, station_id, machine_id):
        return self._stations_repo.get_station_machine_resource_policy(station_id, machine_id)

    def update_station_machine_resource_policy(self, request):
        return self._stations_repo.update_station_machine_resource_policy(request)

    def delete_station_machine_resource_policy(self, station_id, machine_id):
        return self._stations_repo.delete_station_machine_resource_policy(station_id, machine_id)

    def get_station_machine_resource_limits(self, station_id, machine_id):
        return self._stations_repo.get_station_machine_resource_limits(station_id, machine_id)

    def add_volumes_to_station(self, station_id, name, mount_point, access):
        return self._stations_repo.add_volumes_to_station(
            station_id, name, mount_point, access
        )

    def add_host_path_to_volume(self, station_id, volume_id, mid, host_path):
        return self._stations_repo.add_host_path_to_volume(
            station_id, volume_id, mid, host_path
        )

    def delete_host_path_from_volume(self, station_id, volume_id, host_path_id):
        return self._stations_repo.delete_host_path_from_volume(
            station_id, volume_id, host_path_id
        )

    def remove_volume_from_station(self, station_id, volume_id):
        return self._stations_repo.remove_volume_from_station(station_id, volume_id)
