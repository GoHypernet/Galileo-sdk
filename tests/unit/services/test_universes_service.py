from galileo_sdk.compat import mock
from galileo_sdk.business.objects.universes import Universe
from galileo_sdk.business.services.universes import UniversesService 
from galileo_sdk.mock_response import MockResponse

BACKEND = "http://BACKEND"
JOB_ID = "job_id"
DEST_MID = "mid"
FILENAME = "filename"
STATION_ID = "station_id"

# Arrange
settings_repo = mock.Mock()
settings_repo.get_settings().backend = BACKEND
auth_provider = mock.Mock()
auth_provider.get_access_token.return_value = "ACCESS_TOKEN"

universes_repo = mock.Mock()
profile_repo = mock.Mock()
universes_service = UniversesService(universes_repo)

def test_list_universes():
    universes_repo.list_universes.return_value = [
        Universe(
            "universe-id",
            "universe-name",
            "creation-timestamp"
        )
        for _ in range(5)
    ]

    # Call
    r = universes_service.list_universes()

    # Assert
    assert len(r) == 5
    assert r[0].universe_id == "universe-id"


def test_create_universe():
    universes_repo.create_universe.return_value = Universe(
        "universe-id",
        "name",
        "creation-timestamp",
    )

    # Call
    r = universes_service.create_universe("name", "universe-id", "creation-timestamp")

    # Assert
    assert r.universe_id == "universe-id"

