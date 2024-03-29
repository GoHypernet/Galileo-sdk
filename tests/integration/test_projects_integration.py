from galileo_sdk import GalileoSdk
from galileo_sdk.business.objects.missions import Mission, MissionType

# Must set env variables before running tests
CONFIG = "development"

galileo = GalileoSdk(config=CONFIG)

missions = galileo.missions.list_missions(archived=False)


def test_list_projects():
    assert missions[0].creation_timestamp is not None
    assert missions[0].source_path is not None


# def test_upload_file():
#     project = galileo.missions.create_mission(
#         name="project", description="upload_single_file",
#     )
#
#     response = galileo.missions.upload(project.mission_id, "flatplate/flatplate")
#
#     assert response == True
#     assert project is not None

# def test_create_and_upload():
#     project = galileo.missions.create_and_upload_mission(
#         "sdk_project_test", "flatplate/flatplate"
#     )
#
#     assert project is not None
#     assert isinstance(project, Mission)


def test_list_mission_types():
    mission_types = galileo.missions.list_mission_types()

    assert mission_types is not None
    assert len(mission_types) > 0
    assert isinstance(mission_types[0], MissionType)


def test_get_mission_type():
    mission_types = galileo.missions.list_mission_types()
    mission_type = galileo.missions.get_mission_type(mission_types[1].id)

    assert mission_type is not None
    assert mission_type.wizard_spec is not None


def test_get_mission_files():
    files = galileo.missions.get_mission_files(missions[0].mission_id)

    assert len(files) > 0
    assert files[0].filename is not None


def test_update_mission():
    response = galileo.missions.update_mission(missions[0].mission_id,
                                               "new name")
    updated_mission = galileo.missions.get_mission_by_id(
        missions[0].mission_id)

    assert response is True
    assert updated_mission.name == "new name"


def test_delete_mission():
    mission = galileo.missions.create_mission("test_mission")

    response = galileo.missions.delete_mission_by_id(mission.mission_id)

    assert response["success"] is True


def test_update_mission_args():
    mission = galileo.missions.create_mission("test_mission")

    # FIXME: This is broken
    response = galileo.missions.update_mission_args(mission.mission_id,
                                                    ["arg1", "arg2", "arg3"])
    updated_mission = galileo.missions.get_mission_by_id(mission.mission_id)

    assert response['success'] is True
    assert updated_mission.settings["arg"] == ["arg1", "arg2", "arg3"]

    galileo.missions.delete_mission_by_id(mission.mission_id)


def test_mission_type_settings():

    mission = galileo.missions.create_mission(
        "test_mission",
        mission_type_id="jupyter-notebook_lab",
        settings={
            'interface': 'lab',
            'jupyterversion': 'datascience-notebook',
            'dependencies': [],
            'manualdependencies': [],
            'reqstxt': None,
            'vim': False,
            'proxy': False
        })

    settings = galileo.missions.get_mission_type_settings_info(
        mission.mission_type_id)
    assert isinstance(settings, dict)
    galileo.missions.delete_mission_by_id(mission.mission_id)


galileo.disconnect()
