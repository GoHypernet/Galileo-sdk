from typing import List, Optional

from galileo_sdk.business.objects.machines import Machine, UpdateMachineRequest

from ...data.repositories.machines import MachinesRepository
from ..utils.generate_query_str import generate_query_str


class MachinesService:
    def __init__(self, machines_repo: MachinesRepository):
        self._machines_repo = machines_repo

    def get_machine_by_id(self, machine_id: str) -> Machine:
        return self._machines_repo.get_machine_by_id(machine_id)

    def list_machines(
        self,
        mids: Optional[List[str]] = None,
        userids: Optional[List[str]] = None,
        page: Optional[int] = 1,
        items: Optional[int] = 25,
    ) -> List[Machine]:
        query = generate_query_str(
            {"mids": mids, "userids": userids, "page": page, "items": items}
        )
        return self._machines_repo.list_machines(query)

    def update(self, request: UpdateMachineRequest) -> Machine:
        return self._machines_repo.update(request)
