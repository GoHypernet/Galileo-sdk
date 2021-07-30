import os

from ..utils.generate_query_str import generate_query_str
from galileo_sdk.compat import quote


class UniversesService:
    def __init__(self, universes_repo):
        """
        Univeses service

        :param universes_repo: Univeses repo
        :type universes_repo: UniversesRepository
        """
        self._universes_repo = universes_repo

    def list_universes(self):
        """
        List available universes

        :return: A list of available universes
        :rtype: List[Universe]
        """
        return self._universes_repo.list_universes()

    def create_universe(self,
                        name,
                        admin_user_ids,
                        require_positive_credit_balance=True,
                        allow_scheduling_without_quota=True):
        """
        Create a new universe (Need very high permissions)

        :param name: name of the universe
        :type name: str
        :param admin_user_ids: Admin of universe ids
        :type admin_user_ids: List[str
        :param require_positive_credit_balance: Require positive credit balance to be part of universe, defaults to True
        :type require_positive_credit_balance: bool, optional
        :param allow_scheduling_without_quota: Allow job scheduling without quota on universe, defaults to True
        :type allow_scheduling_without_quota: bool, optional
        :return: Created universe
        :rtype: Universe
        """
        return self._universes_repo.create_universe(
            name,
            admin_user_ids,
            require_positive_credit_balance=require_positive_credit_balance,
            allow_scheduling_without_quota=allow_scheduling_without_quota)
