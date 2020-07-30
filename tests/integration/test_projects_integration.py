from galileo_sdk import GalileoSdk
from galileo_sdk.business.objects.missions import Mission

# Must set env variables before running tests
CONFIG = "development"

galileo = GalileoSdk(config=CONFIG)


def test_list_projects():
    project_list = galileo.missions.list_missions()

    assert project_list[0].creation_timestamp is not None
    assert project_list[0].source_path is not None


def test_upload_file():
    project = galileo.missions.create_mission(
        name="project", description="upload_single_file",
    )

    response = galileo.missions.upload(project.mission_id, "flatplate/flatplate")

    assert response == True
    assert project is not None


def test_create_and_upload():
    project = galileo.missions.create_and_upload_mission(
        "sdk_project_test", "flatplate/flatplate"
    )

    assert project is not None
    assert isinstance(project, Mission)


galileo.disconnect()
