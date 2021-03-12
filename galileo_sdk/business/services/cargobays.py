import os

from ..utils.generate_query_str import generate_query_str
from galileo_sdk.compat import quote


class CargoBaysService:
    def __init__(self, universes_repo):
        self._cargo_bays_repo = universes_repo

    def list_cargobays(self):
        return self._cargo_bays_repo.list_cargo_bays()