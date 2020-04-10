class MachinesSdk:
    def __init__(self, machines_service, events=None):
        self._machines_service = machines_service
        self._events = events

    def on_machine_status_update(self, func):
        """
        Callback will execute upon a machine status update event

        :param func: Callable[[MachineStatusUpdateEvent], None]
        :return: None
        """
        self._events.on_machine_status_update(func)

    def on_machine_hardware_update(self, func):
        """
        Callback will execute upon a machine hardware update event

        :param func: Callable[[MachineHardwareUpdateEvent], None]
        :return: None
        """
        self._events.on_machine_hardware_update(func)

    def on_machine_registered(self, func):
        """
        Callback will execute upon a machine hardware update event

        :param func: Callable[[MachineRegisteredEvent], None]
        :return: None
        """
        self._events.on_machine_registered(func)

    def get_machines_by_id(self, machine_id):
        """
        Get machine's info by its id

        :param machine_id: str
        :return: Machine
        """
        return self._machines_service.get_machine_by_id(machine_id)

    def list_machines(
        self, mids=None, userids=None, page=1, items=25,
    ):
        """
        List all machines

        :param mids: List[str]: Filter by machine id
        :param userids: List[str]: Filter by user id
        :param page: int: Page #
        :param items: int: Items per page
        :return: List[Machine]
        """
        return self._machines_service.list_machines(
            mids=mids, userids=userids, page=page, items=items
        )

    def update_machine(self, request):
        """
        Update info about machine

        :param request: UpdateMachineRequest
        :return: Machine
        """

        return self._machines_service.update(request)
