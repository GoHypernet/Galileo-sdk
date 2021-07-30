from .event import EventsSdk
from ..business.objects.lz import UpdateLzRequest


class LzSdk(EventsSdk):
    def __init__(self, lz_service, connector=None, events=None):
        self._lz_service = lz_service
        super(LzSdk, self).__init__(
            connector=connector,
            events=events,
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
        Get a specific Landing Zone's info by its id

        :param lz_id: str
        :return: Lz

        Example:
            >>> lz = galileo.lz.get_lz_by_id("lz_id")
            >>> print(lz.name)
        """
        return self._lz_service.get_lz_by_id(lz_id)

    def delete_lz_by_id(self, lz_id):
        """
        Remove a specific Landing Zone by its id

        :param lz_id: str
        :return: boolean 

        Example:
            >>> galileo.lz.delete_lz_by_id("lz_id")
        """
        return self._lz_service.delete_lz_by_id(lz_id).get("success", False)

    def list_lz(
        self,
        lz_ids=None,
        user_ids=None,
        page=1,
        items=25,
    ):
        """
        Get a filtered list of landing zones Landing Zones and their stats. 

        :param lz_ids: List[str]: Filter by landing zone id
        :param user_ids: List[str]: Filter by user id
        :param page: int: Page number you would like returned
        :param items: int: Number of Landing Zones per page
        :return: List[Lz]

        Example:
            >>> lzs = galileo.lz.list_lz(items=10)
            >>> for lz in lzs:
            >>>    print(lz.name)
        """
        return self._lz_service.list_lz(lz_ids=lz_ids,
                                        user_ids=user_ids,
                                        page=page,
                                        items=items)

    def update_lz(
        self,
        lz_id,
        name=None,
        active=None,
    ):
        """
        Update the info about a Landing Zone

        :param lz_id: Landing zone you want to update
        :param name: update lz name
        :param active: bool
        :return: Lz

        Example:
            >>> lz = galileo.lz.update_lz("lz_id", name="new_name")
            >>> print(lz.name)
        """
        request = UpdateLzRequest(lz_id, name=name, active=active)

        return self._lz_service.update(request)
