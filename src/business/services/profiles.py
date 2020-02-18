from typing import List, Optional

from ...data.repositories.profiles import ProfilesRepository
from ..utils.generate_query_str import generate_query_str


class ProfilesService:
    def __init__(self, profile_repo: ProfilesRepository):
        self._profile_repo = profile_repo

    def list_users(
        self,
        userids: Optional[List[str]] = None,
        usernames: Optional[List[str]] = None,
        partial_usernames: Optional[List[str]] = None,
        wallets: Optional[List[str]] = None,
        public_keys: Optional[List[str]] = None,
        page: Optional[int] = None,
        items: Optional[int] = None,
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
        r = self._profile_repo.list_users(query)
        return r.json()

    def self(self):
        r = self._profile_repo.self()
        return r.json()

    def list_station_invites(self):
        r = self._profile_repo.list_station_invites()
        return r.json()
