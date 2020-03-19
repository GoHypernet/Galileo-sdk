from typing import List, Optional

from galileo_sdk.business.objects.profiles import Profile
from galileo_sdk.business.objects.stations import Station

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
    ) -> List[Profile]:
        """
        Get all Galileo users and their profiles

        :param userids: optional, filter by list of userids
        :param usernames: optional, filter by list of usernames
        :param partial_usernames: optional, filter by partial usernames
        :param wallets: optional, filter by list of wallet ids
        :param public_keys: optional, filter by public key
        :param page: optional, page #
        :param items: optional, items per page
        :return: {"users": [Profile]}
        """
        return self._profile_service.list_users(
            userids=userids,
            usernames=usernames,
            partial_usernames=partial_usernames,
            wallets=wallets,
            public_keys=public_keys,
            page=page,
            items=items,
        )

    def self(self) -> Profile:
        """
        Get your Galileo profile

        :return: Profile
        """
        return self._profile_service.self()

    def list_station_invites(self) -> List[Station]:
        """
        Get all your station invites

        :return: List[Station]
        """
        return self._profile_service.list_station_invites()
