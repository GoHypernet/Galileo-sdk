import os

from ..utils.generate_query_str import generate_query_str
from galileo_sdk.compat import quote


class UniversesService:
    def __init__(self, universes_repo):
        self._universes_repo = universes_repo

    def list_universes(self):
        return self._universes_repo.list_universes()