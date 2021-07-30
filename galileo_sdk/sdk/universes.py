class UniversesSdk:
    def __init__(self, universes_service):
        self._universes_service = universes_service

    def list_universes(self):
        """
        Get list of Universes associated with your account

        :return: List[Universe]
        
        Example:
            >>> universes = galileo.universes.list_universes()
            >>> for universe in universes:
            >>>    print(universe.name)
        """
        return self._universes_service.list_universes()

    def create_universe(self, name, admin_user_ids, require_positive_credit_balance=True, allow_scheduling_without_quota=True):
        """
        Create a Universe (Need very high privileges) 
        :param name: str:
        :param admin_user_ids: List[str]:  
        :param require_positive_balance: Optional[boolean]:
        :param allow_scheduling_without_quota: Optional[boolean]:

        :return: Universe
        
        Example:
            >>> universe = galileo.universes.create_universe("universe_name", ["admin_id"])
            >>> print(universe.name)
            >>> print(universe.id)
        """
        return self._universes_service.create_universe(name, admin_user_ids, require_positive_credit_balance=require_positive_credit_balance, allow_scheduling_without_quota=allow_scheduling_without_quota)