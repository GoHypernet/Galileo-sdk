from galileo_sdk.compat import urlunparse, requests

from galileo_sdk.business.objects.profiles import Profile, ProfileWallet
from galileo_sdk.data.repositories.stations import station_dict_to_station


class ProfilesRepository:
    def __init__(
        self, settings_repository, auth_provider, namespace,
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider
        self._namespace = namespace

    def _make_url(
        self, endpoint, params, query, fragment,
    ):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse(
            (
                schema,
                "{addr}{namespace}".format(addr=addr, namespace=self._namespace),
                endpoint,
                params,
                query,
                fragment,
            )
        )

    def _request(
        self, request, endpoint, data=None, params=None, query=None, fragment=None,
    ):
        url = self._make_url(endpoint, params, query, fragment)
        access_token = self._auth_provider.get_access_token()
        headers = {
            "Authorization": "Bearer {access_token}".format(access_token=access_token)
        }
        r = request(url, json=data, headers=headers)
        r.raise_for_status()
        return r

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request(requests.post, *args, **kwargs)

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


def user_dict_to_profile(profile):
    return Profile(
        userid=profile["userid"],
        username=profile["username"],
        mids=profile["mids"],
        wallets=[wallet_dict_to_wallet(wallet) for wallet in profile["wallets"]],
    )
