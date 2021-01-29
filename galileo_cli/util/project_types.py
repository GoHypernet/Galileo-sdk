import click
from galileo_sdk.business.objects.projects import (HECRASProject, PythonProject, JuliaProject,
                                                   RProject, STATAProject, OctaveProject, SWMM5Project,
                                                   AutoDockVinaProject, BioconductorProject, BlenderProject,
                                                   QuantumEspressoProject, MatLabProject, HECRASPlan, Dependencies)


def get_hecras_project(name, description, project_type_dict):
    input_path = click.prompt("Input path", type=str)
    output_path = click.prompt("Output path", type=str)
    version = click.prompt("Choose a version ({versions})".format(versions=project_type_dict["HECRAS"]),
                           type=str)
    plan = click.prompt(
        "Do you want to run [1] active plans, [2] all plans, or [3] manually select plans? (enter number)",
        type=int)

    files = None
    if plan == 1:
        hecras_plan = HECRASPlan.ActivePlan
    if plan == 2:
        hecras_plan = HECRASPlan.AllPlans
    if plan == 3:
        hecras_plan = HECRASPlan.ManuallySelect
        files = click.prompt("Which files do you want to run? (delineate with commas)", type=str)

    while version not in project_type_dict["HECRAS"]:
        version = click.prompt("Version must be an exact string (ex. hecras 5.0.5)", type=str)
    return HECRASProject(name=name,
                         description=description,
                         plan=hecras_plan,
                         input_path=input_path,
                         output_path=output_path,
                         version=version,
                         files_to_run=files.replace(" ", "").split(",") if files else None)

def get_python_project(name, description, project_type_dict):
    version = click.prompt("Choose a version ({versions})".format(versions=project_type_dict["Python"]),
                           type=str)
    while version not in project_type_dict["Python"]:
        version = click.prompt("Version must be an exact string (ex. python:3.6)", type=str)
    cpu = click.prompt("# of CPU to use", type=int)
    filename = click.prompt("Filename to run", type=str)
    dependencies_list = get_dependencies(project_type_dict)
    arguments = get_arguments(project_type_dict)
    return PythonProject(name=name,
                         description=description,
                         cpu_count=cpu,
                         filename=filename,
                         version=version,
                         dependencies=dependencies_list,
                         arg=arguments)

def get_julia_project(name, description, project_type_dict):
    version = click.prompt("Choose a version ({versions})".format(versions=project_type_dict["Julia"]),
                           type=str)
    while version not in project_type_dict["Julia"]:
        version = click.prompt("Version must be an exact string (ex. julia 1.0)", type=str)
    cpu = click.prompt("CPU to use", type=int)
    filename = click.prompt("Filename to run", type=str)
    dependencies_list = get_dependencies(project_type_dict)
    arguments = get_arguments(project_type_dict)
    return JuliaProject(name=name,
                        description=description,
                        cpu_count=cpu,
                        filename=filename,
                        dependencies=dependencies_list,
                        arg=arguments,
                        version=version)

def get_r_project(name, description, project_type_dict):
    version = click.prompt("Choose a version ({versions})".format(versions=project_type_dict["R"]),
                           type=str)
    while version not in project_type_dict["R"]:
        version = click.prompt("Version must be an exact string (ex. julia 1.0)", type=str)
    cpu = click.prompt("CPU to use", type=int)
    filename = click.prompt("Filename to run", type=str)
    cran_dependencies = get_dependencies(project_type_dict, True)
    dependencies_list = get_dependencies(project_type_dict)
    arguments = get_arguments(project_type_dict)
    return RProject(name=name,
                    description=description,
                    cpu_count=cpu,
                    filename=filename,
                    dependencies=dependencies_list,
                    arg=arguments,
                    cran_dependencies=cran_dependencies,
                    version=version)

def get_stata_project(name, description, project_type_dict):
    version = click.prompt("Choose a version ({versions})".format(versions=project_type_dict["Stata"]),
                           type=str)
    while version not in project_type_dict["Stata"]:
        version = click.prompt("Version must be an exact string (ex. julia 1.0)", type=str)
    cpu = click.prompt("CPU to use", type=int)
    filename = click.prompt("Filename to run", type=str)
    dependencies_list = get_dependencies(project_type_dict)
    arguments = get_arguments(project_type_dict)
    return STATAProject(name=name,
                        description=description,
                        cpu_count=cpu,
                        filename=filename,
                        dependencies=dependencies_list,
                        arg=arguments,
                        version=version)

def get_octave_project(name, description, project_type_dict):
    version = click.prompt("Choose a version ({versions})".format(versions=project_type_dict["Octave"]),
                           type=str)
    while version not in project_type_dict["Octave"]:
        version = click.prompt("Version must be an exact string (ex. julia 1.0)", type=str)
    filename = click.prompt("Filename to run", type=str)
    return OctaveProject(name=name,
                         description=description,
                         filename=filename,
                         version=version)

def get_swmm5_project(name, description, project_type_dict):
    version = click.prompt("Choose a version ({versions})".format(versions=project_type_dict["SWMM5"]),
                           type=str)
    while version not in project_type_dict["SWMM5"]:
        version = click.prompt("Version must be an exact string (ex. julia 1.0)", type=str)
    filename = click.prompt("Filename to run", type=str)
    return SWMM5Project(name=name,
                        description=description,
                        filename=filename,
                        version=version)

def get_autodockvina_project(name, description, project_type_dict):
    version = click.prompt("Choose a version ({versions})".format(versions=project_type_dict["AutoDock Vina"]),
                           type=str)
    while version not in project_type_dict["AutoDock Vina"]:
        version = click.prompt("Version must be an exact string (ex. julia 1.0)", type=str)
    filename = click.prompt("Filename to run", type=str)
    return AutoDockVinaProject(name=name,
                               description=description,
                               filename=filename,
                               version=version)

def get_bioconductor_project(name, description, project_type_dict):
    version = click.prompt("Choose a version ({versions})".format(versions=project_type_dict["Bioconductor"]),
                           type=str)
    while version not in project_type_dict["Bioconductor"]:
        version = click.prompt("Version must be an exact string (ex. julia 1.0)", type=str)
    return BioconductorProject(name=name,
                               description=description,
                               version=version)

def get_blender_project(name, description, project_type_dict):
    version = click.prompt("Choose a version ({versions})".format(versions=project_type_dict["Blender"]),
                           type=str)
    while version not in project_type_dict["Blender"]:
        version = click.prompt("Version must be an exact string (ex. julia 1.0)", type=str)
    copy_in_path = click.prompt("Copy in path", type=str)
    copy_container_path = click.prompt("Copy container path", type=str)
    return BlenderProject(name=name,
                          description=description,
                          copy_in_path=copy_in_path,
                          copy_container_path=copy_container_path,
                          version=version)

def get_quantumespresso_project(name, description, project_type_dict):
    version = click.prompt(
        "Choose a version ({versions})".format(versions=project_type_dict["Quantum Espresso"]),
        type=str)
    while version not in project_type_dict["Quantum Espresso"]:
        version = click.prompt("Version must be an exact string (ex. julia 1.0)", type=str)
    filename = click.prompt("Filename to run", type=str)
    return QuantumEspressoProject(name=name,
                                  description=description,
                                  filename=filename,
                                  version=version)

def get_matlab_project(name, description, project_type_dict):
    version = click.prompt("Choose a version ({versions})".format(versions=project_type_dict["MatLab"]),
                           type=str)
    while version not in project_type_dict["MatLab"]:
        version = click.prompt("Version must be an exact string (ex. julia 1.0)", type=str)
    filename = click.prompt("Filename to run", type=str)
    return MatLabProject(name=name,
                         description=description,
                         filename=filename,
                         version=version)

def get_dependencies(project_type_dict, cran=False):
    if cran:
        dependencies = click.prompt(
            "CRAN Dependencies (delineate with commas, such as 'numpy==latest, beautiful_soup==4.9.0')"
                .format(versions=project_type_dict["Python"]), type=str)
    else:
        dependencies = click.prompt(
            "Dependencies (delineate with commas, such as 'numpy==latest, beautiful_soup==4.9.0')"
                .format(versions=project_type_dict["Python"]), type=str)

    dependencies = dependencies.replace(" ", "").split(",")
    dependencies_list = []

    for dependency in dependencies:
        d = dependency.split("==")
        dependencies_list.append(Dependencies(name=d[0], version=d[1]))

    return dependencies_list

def get_arguments(project_type_dict):
    arguments = click.prompt(
        "Arguments (delineate with commas ex. if the command is test.py 1 2 3 then arguments should be '1,2,3')"
            .format(versions=project_type_dict["Python"]), type=str)

    arguments = arguments.replace(" ", "").split(",")
    return arguments
