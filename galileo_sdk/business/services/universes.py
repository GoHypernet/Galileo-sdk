import os

from ..utils.generate_query_str import generate_query_str
from galileo_sdk.compat import quote


class UniversesService:
    def __init__(self, universes_repo):
        self._universes_repo = universes_repo

    def list_universes(self):
        return self._universes_repo.list_universes()
        
    def create_universe(self, name, admin_user_ids, require_positive_credit_balance=True, allow_scheduling_without_quota=True):
        return self._universes_repo.create_universe(name, admin_user_ids, require_positive_credit_balance=require_positive_credit_balance, allow_scheduling_without_quota=allow_scheduling_without_quota)



