from galileo_sdk import GalileoSdk
from galileo_sdk.business.objects.jobs import Job
from galileo_sdk.business.objects.projects import (
    Project,
    JuliaProject,
    HECRASProject,
    PythonProject,
    RProject,
    STATAProject,
    OctaveProject,
    SWMM5Project,
    AutoDockVinaProject,
    BlenderProject,
    QuantumEspressoProject,
    MatLabProject,
    FLO2DProject,
)

# Must set env variables before running tests
CONFIG = "development"

galileo = GalileoSdk(config=CONFIG)


# def test_create_hecras_project():
#     project_types = galileo.projects.get_project_types()
#     hecras_project = None
#     for project_type in project_types:
#         if project_type.name == "HECRAS":
#             hecras_project = HECRASProject(name="test_sdk_hecras_project",
#                                            description="test_description",
#                                            plan="",
#                                            input_path="",
#                                            output_path="",
#                                            project_type_id=project_type.id)
#             break
#
#     project = galileo.projects.create_project(hecras_project)
#
#     assert project.name == "test_sdk_hecras_project"
#     assert project.description == "test_description"
#
#
# def test_create_stata_project():
#     project_types = galileo.projects.get_project_types()
#     project = None
#     for project_type in project_types:
#         if project_type.name == "Stata":
#             project = STATAProject(name="test_sdk_stata_project",
#                                    description="test_description",
#                                    project_type_id=project_type.id,
#                                    cpu_count=2,
#                                    filename="stata")
#             break
#
#     project = galileo.projects.create_project(project)
#
#     assert project.name == "test_sdk_stata_project"
#     assert project.description == "test_description"


def test_list_projects():
    project_list = galileo.projects.list_projects()

    assert project_list[0].creation_timestamp is not None
    assert project_list[0].source_path is not None


def test_upload_file():
    project = galileo.projects.create_project(
        name="project", description="upload_single_file",
    )

    response = galileo.projects.upload(project.project_id, "flatplate/flatplate")

    assert response == True
    assert project is not None


# Currently won't run without a station with an online machine
# def test_create_and_run():
#     stations_list = galileo.stations.list_stations()
#     project_types = galileo.projects.get_project_types()
#     project = None
#
#     for project_type in project_types:
#         if project_type.name == "Julia":
#             project = JuliaProject(
#                 name="project",
#                 description="upload_single_file",
#                 cpu_count=2,
#                 filename="flatplate",
#                 project_type_id=project_type.id
#             )
#             break
#
#     selected_station = None
#     for station in stations_list:
#         if len(station.mids) > 0:
#             selected_station = station
#             break
#
#     if selected_station is None:
#         selected_station = galileo.stations.create_station("projects_integration_test")
#         self_profile = galileo.profiles.self()
#         machines_list = galileo.machines.list_machines(userids=[self_profile.userid])
#         galileo.stations.add_machines_to_station(selected_station.stationid, machines_list[0])
#
#     job = galileo.projects.create_and_upload_project(
#         project, "flatplate/flatplate", selected_station.stationid
#     )
#
#     galileo.stations.delete_station(selected_station.stationid)
#
#     assert job is not None
#     assert isinstance(job, Job)


def test_create_and_upload():
    project = galileo.projects.create_and_upload_project(
        "sdk_project_test", "flatplate/flatplate"
    )

    assert project is not None
    assert isinstance(project, Project)


# def test_create_octave_project():
#     project_types = galileo.projects.get_project_types()
#     project = None
#     for project_type in project_types:
#         if project_type.name == "Octave":
#             project = OctaveProject(name="test_sdk_octave_project",
#                                     description="test_description",
#                                     project_type_id=project_type.id,
#                                     filename="octave")
#             break
#
#     project = galileo.projects.create_project(project)
#
#     assert project.name == "test_sdk_octave_project"
#     assert project.description == "test_description"
#
#
# def test_create_swmm5_project():
#     project_types = galileo.projects.get_project_types()
#     project = None
#     for project_type in project_types:
#         if project_type.name == "SWMM5":
#             project = SWMM5Project(name="test_sdk_swmm5_project",
#                                    description="test_description",
#                                    project_type_id=project_type.id,
#                                    filename="swmm5")
#             break
#
#     project = galileo.projects.create_project(project)
#
#     assert project.name == "test_sdk_swmm5_project"
#     assert project.description == "test_description"
#
#
# def test_create_autodockvina_project():
#     project_types = galileo.projects.get_project_types()
#     project = None
#     for project_type in project_types:
#         if project_type.name == "AutoDock Vina":
#             project = AutoDockVinaProject(name="test_sdk_autodockvina_project",
#                                           description="test_description",
#                                           project_type_id=project_type.id,
#                                           filename="autodockvina")
#             break
#
#     project = galileo.projects.create_project(project)
#
#     assert project.name == "test_sdk_autodockvina_project"
#     assert project.description == "test_description"
#
#
# def test_create_bioconductor_project():
#     project_types = galileo.projects.get_project_types()
#     project = None
#     for project_type in project_types:
#         if project_type.name == "Bioconductor":
#             project = AutoDockVinaProject(name="test_sdk_Bioconductor_project",
#                                           description="test_description",
#                                           project_type_id=project_type.id,
#                                           filename="Bioconductor")
#             break
#
#     project = galileo.projects.create_project(project)
#
#     assert project.name == "test_sdk_Bioconductor_project"
#     assert project.description == "test_description"


# def test_create_blender_project():
#     project_types = galileo.projects.get_project_types()
#     project = None
#     for project_type in project_types:
#         if project_type.name == "Blender":
#             project = BlenderProject(name="test_sdk_blender_project",
#                                      description="test_description",
#                                      project_type_id=project_type.id,
#                                      copy_container_path=".",
#                                      copy_in_path=".")
#             break
#
#     project = galileo.projects.create_project(project)
#
#     assert project.name == "test_sdk_blender_project"
#     assert project.description == "test_description"


# def test_create_quantum_espresso_project():
#     project_types = galileo.projects.get_project_types()
#     project = None
#     for project_type in project_types:
#         if project_type.name == "Quantum Espresso":
#             project = QuantumEspressoProject(name="test_sdk_quantum_espresso_project",
#                                              description="test_description",
#                                              project_type_id=project_type.id,
#                                              filename="quantum_espresso")
#             break
#
#     project = galileo.projects.create_project(project)
#
#     assert project.name == "test_sdk_quantum_espresso_project"
#     assert project.description == "test_description"
#

# def test_create_flo2d_project():
#     project_types = galileo.projects.get_project_types()
#     project = None
#     for project_type in project_types:
#         if project_type.name == "Flo2D":
#             project = FLO2DProject(name="test_sdk_flo2d_project",
#                                              description="test_description",
#                                              project_type_id=project_type.id,
#                                              filename="flo2d")
#             break
#
#     project = galileo.projects.create_project(project)
#
#     assert project.name == "test_sdk_flo2d_project"
#     assert project.description == "test_description"


# def test_create_matlab_project():
#     project_types = galileo.projects.get_project_types()
#     project = None
#     for project_type in project_types:
#         if project_type.name == "MatLab":
#             project = MatLabProject(name="test_sdk_matlab_project",
#                                     description="test_description",
#                                     project_type_id=project_type.id,
#                                     filename="matlab")
#             break
#
#     project = galileo.projects.create_project(project)
#
#     assert project.name == "test_sdk_matlab_project"
#     assert project.description == "test_description"


galileo.disconnect()
