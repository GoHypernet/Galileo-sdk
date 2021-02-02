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