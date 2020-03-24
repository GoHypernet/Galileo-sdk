from ..utils.generate_query_str import generate_query_str


class ProfilesService:
    def __init__(self, profile_repo):
        self._profile_repo = profile_repo

    def list_users(
        self,
        userids=None,
        usernames=None,
        partial_usernames=None,
        wallets=None,
        public_keys=None,
        page=None,
        items=None,
    ):
        query = generate_query_str(
            {
                "page": page,
                "items": items,
                "userids": userids,
                "usernames": usernames,
                "partial_usernames": partial_usernames,
                "wallets": wallets,
                "public_keys": public_keys,
            }
        )
        return self._profile_repo.list_users(query)

    def self(self):
        return self._profile_repo.self()

    def list_station_invites(self):
        return self._profile_repo.list_station_invites()
