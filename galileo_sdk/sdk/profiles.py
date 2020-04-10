class ProfilesSdk:
    def __init__(self, profiles_service):
        self._profile_service = profiles_service

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
        """
        Get all Galileo users and their profiles

        :param userids: Optional[List[str]]: filter by list of userids
        :param usernames: Optional[List[str]]: filter by list of usernames
        :param partial_usernames: Optional[List[str]]: filter by partial usernames
        :param wallets: Optional[List[Wallet]]: filter by list of wallet ids
        :param public_keys: Optional[List[str]]: filter by public key
        :param page: Optional[int]: page #
        :param items: Optional[int]: items per page
        :return: List[Profile]
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

    def self(self):
        """
        Get your Galileo profile

        :return: Profile
        """
        return self._profile_service.self()

    def list_station_invites(self):
        """
        Get all your station invites

        :return: List[Station]
        """
        return self._profile_service.list_station_invites()
