import os

from ..utils.generate_query_str import generate_query_str
from galileo_sdk.compat import quote


class CargoBaysService:
    def __init__(self, cargo_bays_repo):
        """
        Cargo Bay Service

        :param cargo_bays_repo: Cargo Bays Repository
        :type cargo_bays_repo: CargoBaysRepository
        """
        self._cargo_bays_repo = cargo_bays_repo

    def list_cargobays(self):
        """
        List all Cargo Bays

        :return: A list of all available Cargo Bays
        :rtype: List[CargoBay] 
        """
        return self._cargo_bays_repo.list_cargo_bays()