from galileo_sdk.compat import mock
from galileo_sdk.data.repositories.universes import UniversesRepository
from galileo_sdk.mock_response import MockResponse

BACKEND = "http://BACKEND"
NAMESPACE = "/galileo/user_interface/v1"
UNIVERSE_ID = "universe_id"
NEW_UNIVERSE_ID = "new_universe_id"
HEADERS = {"Authorization": "Bearer ACCESS_TOKEN", "universe-id": UNIVERSE_ID}
# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
settings_repo.get_settings().universe = UNIVERSE_ID
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"
universe_repo = UniversesRepository(settings_repo, auth_provider, NAMESPACE)

ADMIN_USERS = ["admin_user"]

def mocked_requests_get(*args, **kwargs):
    if args[0] == "{backend}{namespace}/universe".format(
        backend=BACKEND, namespace=NAMESPACE
    ):
        return MockResponse(
            {
            "universes": 
                [
                    {
                    "id": "universe-id",
                    "name": "string",
                    "creation_timestamp": "creation-timestamp",
                    "updated_timestamp": "updated-timestamp",
                    "resource_policy_id": "resource-policy-id",
                    "require_positive_credit_balance": True,
                    "allow_scheduling_without_quota": True
                    }
                ]
            },
            200,
        )
    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    if args[0] == "{backend}{namespace}/universe".format(
        backend=BACKEND, namespace=NAMESPACE, 
    ):
        return MockResponse(
            {
                "universe": {
                    "id": NEW_UNIVERSE_ID,
                    "name": NEW_UNIVERSE_ID,
                    "creation_timestamp": "creation-timestamp",
                    "updated_timestamp": "updated-timestamp",
                    "resource_policy_id": "resource-policy-id",
                    "require_positive_credit_balance": True,
                    "allow_scheduling_without_quota": True
                }
            },
            200,
        )

    return MockResponse(None, 404)


@mock.patch("galileo_sdk.compat.requests.get", side_effect=mocked_requests_get)
def test_list_universes(mocked_requests):
    # Call
    r = universe_repo.list_universes()

    # Act
    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/universe".format(
            backend=BACKEND, namespace=NAMESPACE
        ),
        headers=HEADERS,
        json=None,
    )
    print(r)
    # Assert
    assert r[0].universe_id == "universe-id"

@mock.patch("galileo_sdk.compat.requests.post", side_effect=mocked_requests_post)
def test_create_universe(mocked_requests):
    r = universe_repo.create_universe(name=NEW_UNIVERSE_ID, admin_user_ids=ADMIN_USERS)

    mocked_requests.assert_called_once_with(
        "{backend}{namespace}/universe".format(
            backend=BACKEND, namespace=NAMESPACE
        ),
        headers=HEADERS,
        json={
            "name": NEW_UNIVERSE_ID,
            "require_positive_credit_balance": True,
            "allow_scheduling_without_quota": True,
            "admin_user_ids": ADMIN_USERS,
        },
    )

    assert r.universe_id == NEW_UNIVERSE_ID

