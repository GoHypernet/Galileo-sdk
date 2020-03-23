from ..utils.generate_query_str import generate_query_str


class MachinesService:
    def __init__(self, machines_repo):
        self._machines_repo = machines_repo

    def get_machine_by_id(self, machine_id):
        return self._machines_repo.get_machine_by_id(machine_id)

    def list_machines(
        self, mids=None, userids=None, page=1, items=25,
    ):
        query = generate_query_str(
            {"mids": mids, "userids": userids, "page": page, "items": items}
        )
        return self._machines_repo.list_machines(query)

    def update(self, request):
        return self._machines_repo.update(request)
