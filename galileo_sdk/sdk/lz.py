from .event import EventsSdk
from ..business.objects.lz import UpdateLzRequest


class LzSdk(EventsSdk):
    def __init__(self, lz_service, connector=None, events=None):
        self._lz_service = lz_service
        super(LzSdk, self).__init__(
            connector=connector, events=events,
        )

    def on_lz_status_update(self, func):
        """
        Callback will execute upon a landing zone status update event

        :param func: Callable[[LzStatusUpdateEvent], None]
        :return: None
        """
        self._set_event_handler("lz")
        self._events.on_lz_status_update(func)

    def on_lz_hardware_update(self, func):
        """
        Callback will execute upon a landing zone hardware update event

        :param func: Callable[[LzHardwareUpdateEvent], None]
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

    def get_lz_by_id(self, lz_id):
        """
        Get landing zone's info by its id

        :param lz_id: str
        :return: Lz
        """
        return self._lz_service.get_lz_by_id(lz_id)

    def list_lz(
        self, lz_ids=None, userids=None, page=1, items=25,
    ):
        """
        List all machines

        :param lz_ids: List[str]: Filter by landing zone id
        :param userids: List[str]: Filter by user id
        :param page: int: Page #
        :param items: int: Items per page
        :return: List[Lz]
        """
        return self._lz_service.list_lz(
            lz_ids=lz_ids, userids=userids, page=page, items=items
        )

    def update_lz(
        self, lz_id, name=None, active=None,
    ):
        """
        Update info about landing zone

        :param lz_id: Landing zone you want to update
        :param name: update lz name
        :param active: bool
        :return: Lz
        """
        request = UpdateLzRequest(lz_id, name, active)

        return self._lz_service.update(request)
