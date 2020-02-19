from typing import Callable, List, Optional

from ..business.objects.machines import MachinesEvents, MachineStatusUpdateEvent
from ..business.services.machines import MachinesService


class MachinesSdk:
    _machine_service: MachinesService
    _events: MachinesEvents

    def __init__(self, machines_service: MachinesService, events: MachinesEvents):
        self._machines_service = machines_service
        self._events = events

    def on_machine_status_update(
        self, func: Callable[[MachineStatusUpdateEvent], None]
    ):
        self._events.on_machine_status_update(func)

    def get_machines_by_id(self, machine_id: str):
        return self._machines_service.get_machine_by_id(machine_id)

    def list_machines(
        self,
        mids: Optional[List[str]] = None,
        userids: Optional[List[str]] = None,
        page: Optional[int] = 1,
        items: Optional[int] = 25,
    ):
        return self._machines_service.list_machines(
            mids=mids, userids=userids, page=page, items=items
        )

    def update_concurrent_max_jobs(self, mid: str, amount: str):
        return self._machines_service.update_max_concurrent_jobs(mid, amount)
