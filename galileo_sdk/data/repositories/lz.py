from galileo_sdk.business.objects.lz import ELzStatus, Lz
from galileo_sdk.data.repositories import RequestsRepository


class LzRepository(RequestsRepository):
    def __init__(
        self, settings_repository, auth_provider, namespace,
    ):
        super(LzRepository, self).__init__(
            settings_repository=settings_repository,
            auth_provider=auth_provider,
            namespace=namespace,
        )

    def get_lz_by_id(self, machine_id):
        response = self._get("/machines/{machine_id}".format(machine_id=machine_id))
        json = response.json()
        return machine_dict_to_machine(json)

    def list_lz(self, query):
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
    return Lz(
        name=machine["name"],
        userid=machine["userid"],
        status=ELzStatus[machine["status"]],
        lz_id=machine["mid"],
        gpu_count=machine["gpu_count"],
        cpu_count=machine["cpu_count"],
        operating_system=machine["operating_system"],
        arch=machine["arch"],
        memory_amount=machine["memory_amount"],
        memory=machine["memory"],
        job_runner=machine["job_runner"],
        container_technology=machine["container_technology"],
    )
