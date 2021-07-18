class ProfilesSdk:
    def __init__(self, profiles_service):
        self._profile_service = profiles_service

    def list_users(
        self,
        user_ids=None,
        usernames=None,
        partial_usernames=None,
        public_keys=None,
        page=None,
        items=None,
    ):
        """
        Get all Galileo users and their profiles

        :param user_ids: Optional[List[str]]: filter by list of userids
        :param usernames: Optional[List[str]]: filter by list of usernames
        :param partial_usernames: Optional[List[str]]: filter by partial usernames
        :param public_keys: Optional[List[str]]: filter by public key
        :param page: Optional[int]: page #
        :param items: Optional[int]: items per page
        :return: List[Profile]

        Example:
            >>> users = galileo.profiles.list_users()
        """
        return self._profile_service.list_users(
            userids=user_ids,
            usernames=usernames,
            partial_usernames=partial_usernames,
            public_keys=public_keys,
            page=page,
            items=items,
        )

    def self(self):
        """
        Get your Galileo profile

        :return: Profile

        Example:
            >>> profile = galileo.profiles.self()
            >>> print(profile.id, profile.username)
        """
        return self._profile_service.self()

    def list_station_invites(self):
        """
        Get all your station invites

        :return: List[Station]

        Example:
            >>> invites = galileo.profiles.list_station_invites()
            >>> for station in invites:
            >>>     print(station.station_id, station.name)
        """
        return self._profile_service.list_station_invites()
