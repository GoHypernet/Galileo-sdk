from ..utils.generate_query_str import generate_query_str


class LzService:
    def __init__(self, lz_repo):
        self._lz_repo = lz_repo

    def get_lz_by_id(self, lz_id):
        return self._lz_repo.get_lz_by_id(lz_id)

    def list_lz(
        self, lz_ids=None, userids=None, page=1, items=25,
    ):
        query = generate_query_str(
            {"mids": lz_ids, "userids": userids, "page": page, "items": items}
        )
        return self._lz_repo.list_lz(query)

    def update(self, request):
        return self._lz_repo.update(request)
