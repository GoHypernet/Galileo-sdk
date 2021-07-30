from ..utils.generate_query_str import generate_query_str


class ProfilesService:
    def __init__(self, profile_repo):
        """
        Profile service 

        :param profile_repo: ProfileRepository 
        :type profile_repo: ProfileRepository
        """
        self._profile_repo = profile_repo

    def list_users(
        self,
        user_ids=None,
        usernames=None,
        partial_usernames=None,
        page=None,
        items=None,
    ):
        """ Filters users by the given criteria.

        :param user_ids: Filter users by user ids, defaults to None
        :type user_ids: List[str], optional
        :param usernames: Filter users by usernames, defaults to None
        :type usernames: List[str], optional
        :param partial_usernames: Filter users by matching partial usernames, defaults to None
        :type partial_usernames: List[str], optional
        :param page: Current page of results, defaults to None
        :type page: int, optional
        :param items: Number of items per page, defaults to None
        :type items: int, optional
        :return: List of users
        :rtype: List[Profile]
        """
        query = generate_query_str({
            "page": page,
            "items": items,
            "userids": user_ids,
            "usernames": usernames,
            "partial_usernames": partial_usernames,
        })
        return self._profile_repo.list_users(query)

    def self(self):
        """
        Get the current logged-in user's profile

        :return: Current user's profile
        :rtype: Profile
        """
        return self._profile_repo.self()

    def list_station_invites(self):
        """
        List all inbound station invites

        :return: Stations inviting the current user
        :rtype: List[Station]
        """
        return self._profile_repo.list_station_invites()
