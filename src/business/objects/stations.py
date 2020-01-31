from typing import Callable, List

from ...business.objects.event import EventEmitter


class NewStationEvent:
    def __init__(self, station):
        # TODO: need to type
        self.station = station


class StationAdminInviteSentEvent:
    def __init__(self, stationid, userids):
        self.stationid: str = stationid
        self.userids: List[str] = userids


class StationUserInviteReceivedEvent:
    def __init__(self, station):
        self.station = station


class StationsEvents:
    _event: EventEmitter

    def __init__(self):
        self._event = EventEmitter()

    def on_new_station(self, func: Callable[[NewStationEvent], None]):
        self._event.on("new_station", func)

    def new_station(self, event: NewStationEvent):
        self._event.emit("new_station", event)

    def on_station_admin_invite_sent(
        self, func: Callable[[StationAdminInviteSentEvent], None]
    ):
        self._event.on("station_admin_invite_sent", func)

    def station_admin_invite_sent(self, event: StationAdminInviteSentEvent):
        self._event.emit("station_admin_invite_sent", event)

    def on_station_user_invite_received(
        self, func: Callable[[StationUserInviteReceivedEvent], None]
    ):
        self._event.emit("station_user_invite_received", func)

    def station_user_invite_received(self, event: StationUserInviteReceivedEvent):
        self._event.emit("station_user_invite_received", event)
