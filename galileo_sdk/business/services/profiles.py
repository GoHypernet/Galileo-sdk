from typing import List, Optional

from galileo_sdk.business.objects.profiles import Profile
from galileo_sdk.business.objects.stations import Station

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
    ) -> List[Profile]:
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

    def self(self) -> Profile:
        return self._profile_repo.self()

    def list_station_invites(self) -> List[Station]:
        return self._profile_repo.list_station_invites()
