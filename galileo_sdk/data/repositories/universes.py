from datetime import datetime

from galileo_sdk.business.objects.universes import Universe
from galileo_sdk.data.repositories import RequestsRepository


class UniversesRepository(RequestsRepository):
    def __init__(
        self, settings_repository, auth_provider, namespace,
    ):
        super(UniversesRepository, self).__init__(
            settings_repository=settings_repository,
            auth_provider=auth_provider,
            namespace=namespace,
        )

    def list_universes(self):
        response = self._get("/universe")
        json = response.json()
        universes = json["universes"]
        return [universe_dict_to_universe(universe) for universe in universes]
		

def universe_dict_to_universe(universe):
    return Universe(
        universe["id"],
        universe["name"],
        universe["creation_timestamp"],
    )
