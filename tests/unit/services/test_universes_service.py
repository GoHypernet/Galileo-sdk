from galileo_sdk.compat import mock
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


