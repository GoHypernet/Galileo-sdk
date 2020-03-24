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
