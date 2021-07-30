from ..utils.generate_query_str import generate_query_str


#TODO Replace some bool return types with Success objects
class LzService:
    def __init__(self, lz_repo):
        """
        Landing Zone Service Constructor

        :param lz_repo: LZ Repository
        :type lz_repo: LzRepository
        """
        self._lz_repo = lz_repo

    def get_lz_by_id(self, lz_id):
        """
        Get a Landing Zone by ID

        :param lz_id: The Landing Zone's ID
        :type machine_id: str
        :return: LZ Object
        :rtype: Lz
        """
        return self._lz_repo.get_lz_by_id(lz_id)

    def delete_lz_by_id(self, lz_id):
        """
        Delete a Landing Zone by ID

        :param lz_id: LZ ID of the machine to delete
        :type lz_id: str
        :return: Success
        :rtype: bool
        """
        return self._lz_repo.delete_lz_by_id(lz_id)

    def list_lz(
        self,
        lz_ids=None,
        user_ids=None,
        page=1,
        items=25,
    ):
        """
        Get a filtered list of Landing Zones

        :param lz_ids: Filter by Landing Zone ids, defaults to None
        :type lz_ids: List[str], optional
        :param user_ids: Filter by user ids, defaults to None
        :type user_ids: List[str], optional
        :param page: Request page, defaults to 1
        :type page: int, optional
        :param items: Number of items on page, defaults to 25
        :type items: int, optional
        :return: List of Lz objects
        :rtype: List[Lz]
        """
        query = generate_query_str({
            "mids": lz_ids,
            "userids": user_ids,
            "page": page,
            "items": items
        })
        return self._lz_repo.list_lz(query)

    def update(self, request):
        """
        Update a Landing Zone

        :param request: Update request
        :type request: UpdateLzRequest
        :return: Updated LZ
        :rtype: Lz
        """
        return self._lz_repo.update(request)
