from typing import List, Optional

from ..business.services.profiles import ProfilesService


class ProfilesSdk:
    def __init__(self, profiles_service: ProfilesService):
        self._profile_service = profiles_service

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
        return self._profile_service.list_users(
            userids=userids,
            usernames=usernames,
            partial_usernames=partial_usernames,
            wallets=wallets,
            public_keys=public_keys,
            page=page,
            items=items,
        )

    def self(self):
        return self._profile_service.self()

    def list_station_invites(self):
        return self._profile_service.list_station_invites()
