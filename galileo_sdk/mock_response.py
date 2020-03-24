from .compat import mock


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.raise_for_status = mock.Mock()

    def json(self):
        return self.json_data
