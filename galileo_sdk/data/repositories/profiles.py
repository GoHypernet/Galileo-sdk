from galileo_sdk.business.objects import Profile, ProfileCard
from galileo_sdk.data.repositories.stations import station_dict_to_station
from galileo_sdk.data.repositories import RequestsRepository


class ProfilesRepository(RequestsRepository):
    def __init__(
        self,
        settings_repository,
        auth_provider,
        namespace,
    ):
        """
        Profile repository

        :param settings_repository: Settings repository
        :type settings_repository: SettingsRepository
        :param auth_provider: Authentication provider
        :type auth_provider: AuthProvider
        :param namespace: Backend URL
        :type namespace: str
        """
        super(ProfilesRepository, self).__init__(
            settings_repository=settings_repository,
            auth_provider=auth_provider,
            namespace=namespace,
        )

    def self(self):
        """
        Get the current logged in user's profile

        :return: Current user's profile
        :rtype: Profile
        """
        response = self._get("/users/self")
        json = response.json()
        return user_dict_to_profile(json)

    def list_users(self, query):
        """
        Searches for a list of filtered users

        :param query: Query to filter users by
        :type query: str
        :return: Found filtered users
        :rtype: List[Profile]
        """
        response = self._get("/users", query=query)
        json = response.json()
        users = json["users"]
        return [user_dict_to_profile(user) for user in users]

    def list_station_invites(self):
        """
        List all inbound station invites

        :return: Stations inviting the current user
        :rtype: List[Station]
        """
        response = self._get("/users/invites")
        json = response.json()
        stations = json["stations"]
        return [station_dict_to_station(station) for station in stations]


def card_dict_to_card(stored_card):
    """
    Convert a stored card dictionary to a card object

    :param stored_card: Stored card dictionary 
    :type stored_card: Dict
    :return: Profile card object
    :rtype: ProfileCard
    """
    return ProfileCard(
        stored_card["id"],
        stored_card["user_id"],
        stored_card["stripe_payment_method_id"],
        stored_card["creation_timestamp"],
    )


def user_dict_to_profile(profile):
    """
    Convert a stored profile dictionary to a profile object

    :param profile: Profile dictionary
    :type profile: Dict
    :return: Profile object
    :rtype: Profile
    """
    return Profile(
        user_id=profile["userid"],
        username=profile["username"],
        lz_ids=profile["mids"],
        stripe_customer_id=profile.get("stripe_customer_id", None),
        pricing_tier_id=profile.get("pricing_tier_id", None),
        stored_cards=[
            card_dict_to_card(card) for card in profile["stored_cards"]
        ] if profile.get("stored_cards", None) is not None else None,
    )
