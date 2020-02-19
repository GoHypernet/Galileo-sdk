from typing import List, Optional

from ...data.repositories.machines import MachinesRepository
from ..utils.generate_query_str import generate_query_str


class MachinesService:
    def __init__(self, machines_repo: MachinesRepository):
        self._machines_repo = machines_repo

    def get_machine_by_id(self, machine_id: str):
        r = self._machines_repo.get_machine_by_id(machine_id)
        return r.json()

    def list_machines(
        self,
        mids: Optional[List[str]] = None,
        userids: Optional[List[str]] = None,
        page: Optional[int] = 1,
        items: Optional[int] = 25,
    ):
        query = generate_query_str(
            {"mids": mids, "userids": userids, "page": page, "items": items}
        )
        r = self._machines_repo.list_machines(query)
        return r.json()

    def update_max_concurrent_jobs(self, mid: str, amount: int):
        r = self._machines_repo.update_max_concurrent_jobs(mid, amount)
        return r.json()
