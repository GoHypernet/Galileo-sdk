from ..business.objects.stations import StationsEvents
from ..business.services.stations import StationsService


class StationsSdk:
    _stations_service: StationsService
    _events: StationsEvents

    def __init__(self, stations_service: StationsService, events: StationsEvents):
        self._stations_service = stations_service
        self._events = events
