from galileo_sdk.business.objects.lz import ELzStatus, Lz
from galileo_sdk.data.repositories import RequestsRepository


#TODO Replace some bool return types with Success objects
class LzRepository(RequestsRepository):
    def __init__(
        self,
        settings_repository,
        auth_provider,
        namespace,
    ):
        """
        LZ Repository
        :param settings_repository: Settings repository
        :type settings_repository: SettingsRepository
        :param auth_provider: Authentication provider
        :type auth_provider: AuthProvider
        :param namespace: Backend URL
        :type namespace: str
        """
        super(LzRepository, self).__init__(
            settings_repository=settings_repository,
            auth_provider=auth_provider,
            namespace=namespace,
        )

    def get_lz_by_id(self, lz_id):
        """
        Get a Landing Zone by ID

        :param lz_id: The Landing Zone's ID
        :type machine_id: str
        :return: LZ Object
        :rtype: Lz
        """
        response = self._get("/machines/{machine_id}".format(machine_id=lz_id))
        json = response.json()
        return lz_dict_to_lz(json)

    def list_lz(self, query):
        """
        List Lzs with a specific query

        :param query: The attributes to filter Lzs by
        :type query: str
        :return: List of Lz objects
        :rtype: List[Lz]
        """
        response = self._get("/machines", query=query)
        json = response.json()
        lzs = json["machines"]
        return [lz_dict_to_lz(lz) for lz in lzs]

    # FIXME: Could return success object rather than bool
    def delete_lz_by_id(self, lz_id):
        """
        Delete a Landing Zone by ID

        :param lz_id: LZ ID of the machine to delete
        :type lz_id: str
        :return: Success
        :rtype: bool
        """
        response = self._delete("/machines/{lz_id}".format(lz_id=lz_id))
        return response.json()

    def update(self, request):
        """
        Update a Landing Zone

        :param request: Update request
        :type request: UpdateLzRequest
        :return: Updated LZ
        :rtype: Lz
        """
        response = self._put(
            "/machines/{lz_id}".format(lz_id=request.lz_id),
            {
                "name": request.name,
                "active": request.active,
            },
        )
        json = response.json()
        lz = json["machine"]
        return lz_dict_to_lz(lz)


def lz_dict_to_lz(lz):
    """
    Convert Landing Zone dictionary to Lz object.

    :param lz: LZ dictionary
    :type lz: Dict
    :return: LZ object
    :rtype: Lz
    """
    return Lz(
        name=lz["name"],
        user_id=lz["userid"],
        status=ELzStatus[lz["status"]],
        lz_id=lz["mid"],
        gpu_count=lz["gpu_count"],
        cpu_count=lz["cpu_count"],
        operating_system=lz["operating_system"],
        arch=lz["arch"],
        memory_amount=lz["memory_amount"],
        memory=lz["memory"],
        job_runner=lz["job_runner"],
        container_technology=lz["container_technology"],
    )
