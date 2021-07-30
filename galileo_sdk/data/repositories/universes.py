from datetime import datetime

from galileo_sdk.business.objects.universes import Universe
from galileo_sdk.data.repositories import RequestsRepository


class UniversesRepository(RequestsRepository):
    def __init__(
        self,
        settings_repository,
        auth_provider,
        namespace,
    ):
        """
        UnivesesRepository

        :param settings_repository: Settings repository
        :type settings_repository: SettingsRepository
        :param auth_provider: Authentication provider
        :type auth_provider: AuthProvider
        :param namespace: Backend URL
        :type namespace: str
        """
        super(UniversesRepository, self).__init__(
            settings_repository=settings_repository,
            auth_provider=auth_provider,
            namespace=namespace,
        )

    def list_universes(self):
        """
        List available universes

        :return: A list of available universes
        :rtype: List[Universe]
        """
        response = self._get("/universe")
        json = response.json()
        universes = json["universes"]
        return [universe_dict_to_universe(universe) for universe in universes]

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
        response = self._post(
            "/universe", {
                "name": name,
                "require_positive_credit_balance":
                require_positive_credit_balance,
                "allow_scheduling_without_quota":
                allow_scheduling_without_quota,
                "admin_user_ids": admin_user_ids,
            })
        json = response.json()
        universe = json["universe"]
        return universe_dict_to_universe(universe)


def universe_dict_to_universe(universe):
    """
    Convert a universe dict to a universe

    :param universe: Universe dict
    :type universe: Dict
    :return: Universe object
    :rtype: Universe
    """
    return Universe(
        universe["id"],
        universe["name"],
        universe["creation_timestamp"],
    )
