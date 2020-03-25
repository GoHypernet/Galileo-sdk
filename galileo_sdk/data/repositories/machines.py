from galileo_sdk.compat import urlunparse, requests
from galileo_sdk.business.objects.machines import EMachineStatus, Machine


class MachinesRepository:
    def __init__(
        self, settings_repository, auth_provider, namespace,
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider
        self._namespace = namespace

    def _make_url(self, endpoint, params="", query="", fragment=""):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse(
            (
                schema,
                "{addr}{namespace}".format(addr=addr, namespace=self._namespace),
                endpoint,
                params,
                query,
                fragment,
            )
        )

    def _request(
        self, request, endpoint, data=None, params=None, query=None, fragment=None,
    ):
        url = self._make_url(endpoint, params, query, fragment)
        access_token = self._auth_provider.get_access_token()
        headers = {
            "Authorization": "Bearer {access_token}".format(access_token=access_token)
        }
        r = request(url, json=data, headers=headers)
        r.raise_for_status()
        return r

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request(requests.put, *args, **kwargs)

    def get_machine_by_id(self, machine_id):
        response = self._get("/machines/{machine_id}".format(machine_id=machine_id))
        json = response.json()
        return machine_dict_to_machine(json)

    def list_machines(self, query):
        response = self._get("/machines", query=query)
        json = response.json()
        machines = json["machines"]
        return [machine_dict_to_machine(machine) for machine in machines]

    def update(self, request):
        response = self._put(
            "/machines/{mid}".format(mid=request.mid),
            {
                "name": request.name,
                "gpu": request.gpu,
                "cpu": request.cpu,
                "os": request.os,
                "arch": request.arch,
                "memory": request.memory,
                "running_jobs_limit": request.running_jobs_limit,
                "active": request.active,
            },
        )
        json = response.json()
        machine = json["machine"]
        return machine_dict_to_machine(machine)


def machine_dict_to_machine(machine):
    return Machine(
        machine["name"],
        machine["userid"],
        EMachineStatus[machine["status"]],
        machine["mid"],
        machine["gpu"],
        machine["cpu"],
        machine["os"],
        machine["arch"],
        machine["memory"],
        machine["running_jobs_limit"],
    )
