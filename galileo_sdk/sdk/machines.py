from typing import Callable, List, Optional

from ..business.objects.machines import (Machine, MachineHardwareUpdateEvent,
                                         MachineRegisteredEvent,
                                         MachinesEvents,
                                         MachineStatusUpdateEvent,
                                         UpdateMachineRequest)
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
        """
        Callback will execute upon a machine status update event

        :param func: Callable[[MachineStatusUpdateEvent], None]
        :return: None
        """
        self._events.on_machine_status_update(func)

    def on_machine_hardware_update(
        self, func: Callable[[MachineHardwareUpdateEvent], None]
    ):
        """
        Callback will execute upon a machine hardware update event

        :param func: Callable[[MachineHardwareUpdateEvent], None]
        :return: None
        """
        self._events.on_machine_hardware_update(func)

    def on_machine_registered(self, func: Callable[[MachineRegisteredEvent], None]):
        """
        Callback will execute upon a machine hardware update event

        :param func: Callable[[MachineRegisteredEvent], None]
        :return: None
        """
        self._events.on_machine_registered(func)

    def get_machines_by_id(self, machine_id: str) -> Machine:
        """
        Get machine's info by its id

        :param machine_id: machines id
        :return: Machine
        """
        return self._machines_service.get_machine_by_id(machine_id)

    def list_machines(
        self,
        mids: Optional[List[str]] = None,
        userids: Optional[List[str]] = None,
        page: Optional[int] = 1,
        items: Optional[int] = 25,
    ) -> List[Machine]:
        """
        List all machines

        :param mids: Filter by machine id
        :param userids: Filter by user id
        :param page: Page #
        :param items: Items per page
        :return: List[Machine]
        """
        return self._machines_service.list_machines(
            mids=mids, userids=userids, page=page, items=items
        )

    def update_machine(self, request: UpdateMachineRequest) -> Machine:
        """
        Update info about machine

        :param request: UpdateMachineRequest
        :return: Machine
        """

        return self._machines_service.update(request)
