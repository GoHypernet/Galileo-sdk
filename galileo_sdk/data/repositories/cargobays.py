from datetime import datetime

from galileo_sdk.business.objects.cargobays import CargoBay
from galileo_sdk.data.repositories import RequestsRepository


class CargoBaysRepository(RequestsRepository):
    def __init__(
        self, settings_repository, auth_provider, namespace,
    ):
        super(CargoBaysRepository, self).__init__(
            settings_repository=settings_repository,
            auth_provider=auth_provider,
            namespace=namespace,
        )

    def list_cargo_bays(self):
        response = self._get("/storage")
        json = response.json()
        cargobays = json["storage"]
        return [cargo_bay_dict_to_CargoBay(cargobay) for cargobay in cargobays]
		

def cargo_bay_dict_to_CargoBay(cargobay):
    return CargoBay(
        cargobay["name"],
        cargobay["id"],
        cargobay["storage_type"],
        cargobay["creation_date"],
    )
