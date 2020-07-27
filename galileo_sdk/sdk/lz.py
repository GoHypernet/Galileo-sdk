from .event import EventsSdk


class LzSdk(EventsSdk):
    def __init__(self, lz_service, connector=None, events=None):
        self._lz_service = lz_service
        super(LzSdk, self).__init__(
            connector=connector, events=events,
        )

    def on_lz_status_update(self, func):
        """
        Callback will execute upon a machine status update event

        :param func: Callable[[MachineStatusUpdateEvent], None]
        :return: None
        """
        self._set_event_handler("lz")
        self._events.on_lz_status_update(func)

    def on_lz_hardware_update(self, func):
        """
        Callback will execute upon a machine hardware update event

        :param func: Callable[[MachineHardwareUpdateEvent], None]
        :return: None
        """
        self._set_event_handler("lz")
        self._events.on_lz_hardware_update(func)

    def on_lz_registered(self, func):
        """
        Callback will execute upon a machine hardware update event

        :param func: Callable[[MachineRegisteredEvent], None]
        :return: None
        """
        self._set_event_handler("lz")
        self._events.on_lz_registered(func)

    def get_lz_by_id(self, machine_id):
        """
        Get landing zone's info by its id

        :param machine_id: str
        :return: Machine
        """
        return self._lz_service.get_lz_by_id(machine_id)

    def list_lz(
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
        return self._lz_service.list_lz(
            mids=mids, userids=userids, page=page, items=items
        )

    def update_lz(self, request):
        """
        Update info about landing zone

        :param request: UpdateMachineRequest
        :return: Machine
        """

        return self._lz_service.update(request)
