import sys

_ver = sys.version_info

is_py2 = _ver[0] == 2
is_py3 = _ver[0] == 3

if is_py3:
    from galileo_sdk.data.events.connector import GalileoConnector


class EventsSdk(object):
    def __init__(self, connector, events=None):
        self._connector = connector
        self._events = events

    def _set_event_handler(self, event_type):
        if is_py2:
            raise Exception("You cannot register event listeners in Python 2!")

        if self._events:
            return

        if event_type == "lz":
            self._events = self._connector.set_lz_events()
        elif event_type == "jobs":
            self._events = self._connector.set_jobs_events()
        elif event_type == "stations":
            self._events = self._connector.set_stations_events()

    def disconnect(self):
        if is_py3 and self._connector:
            self._connector.disconnect()
