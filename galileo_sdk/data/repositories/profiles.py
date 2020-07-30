from galileo_sdk.business.objects import Profile, ProfileWallet, ProfileCard
from galileo_sdk.data.repositories.stations import station_dict_to_station
from galileo_sdk.data.repositories import RequestsRepository


class ProfilesRepository(RequestsRepository):
    def __init__(
        self, settings_repository, auth_provider, namespace,
    ):
        super(ProfilesRepository, self).__init__(
            settings_repository=settings_repository,
            auth_provider=auth_provider,
            namespace=namespace,
        )

    def self(self):
        response = self._get("/users/self")
        json = response.json()
        return user_dict_to_profile(json)

    def list_users(self, query):
        response = self._get("/users", query=query)
        json = response.json()
        users = json["users"]
        return [user_dict_to_profile(user) for user in users]

    def list_station_invites(self):
        response = self._get("/users/invites")
        json = response.json()
        stations = json["stations"]
        return [station_dict_to_station(station) for station in stations]


def wallet_dict_to_wallet(wallet):
    return ProfileWallet(
        wallet=wallet["wallet"],
        public_key=wallet["public_key"],
        profilewalletid=wallet["profilewalletid"],
    )


def cards_dict_to_cards(stored_cards):
    return ProfileCard(
        stored_cards["id"],
        stored_cards["user_id"],
        stored_cards["stripe_payment_method_id"],
        stored_cards["creation_timestamp"],
    )


def user_dict_to_profile(profile):
    return Profile(
        userid=profile["userid"],
        username=profile["username"],
        lz_ids=profile["mids"],
        wallets=[wallet_dict_to_wallet(wallet) for wallet in profile["wallets"]],
        stripe_customer_id=profile.get("stripe_customer_id", None),
        pricing_tier_id=profile.get("pricing_tier_id", None),
        stored_cards=[cards_dict_to_cards(card) for card in profile["stored_cards"]]
        if profile.get("stored_cards", None) is not None
        else None,
    )
