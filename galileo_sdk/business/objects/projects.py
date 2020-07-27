from ...business.objects.event import EventEmitter
import enum


class FileListing:
    def __init__(
        self, filename, path, modification_date, creation_date, file_size, nonce=None,
    ):
        self.filename = filename
        self.path = path
        self.modification_date = modification_date
        self.creation_date = creation_date
        self.file_size = file_size
        self.nonce = nonce


class DirectoryListing:
    def __init__(
        self, storage_id, path, listings,
    ):
        self.storage_id = storage_id
        self.path = path
        self.listings = listings


class Project:
    def __init__(
        self,
        project_id,
        name,
        description,
        source_storage_id,
        source_path,  # default will be project_id
        destination_storage_id,
        destination_path,  # default will be project_id
        user_id,
        creation_timestamp,
        project_type_id,
    ):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.source_storage_id = source_storage_id
        self.source_path = source_path
        self.destination_storage_id = destination_storage_id
        self.destination_path = destination_path
        self.user_id = user_id
        self.creation_timestamp = creation_timestamp
        self.project_type_id = project_type_id


class ProjectsEvents:
    def __init__(self):
        self._events = EventEmitter()


class ProjectType:
    def __init__(self, id, name, description, version):
        self.id = id
        self.name = name
        self.description = description
        self.version = version


class CreateProjectRequest(object):
    def __init__(
        self,
        name,
        description,
        source_storage_id=None,
        destination_storage_id=None,
        project_type_name=None,
        source_path=None,
        destination_path=None,
        project_type_id=None,
    ):
        self.name = name
        self.description = description
        self.source_storage_id = source_storage_id
        self.destination_storage_id = destination_storage_id
        self.source_path = source_path
        self.destination_path = destination_path
        self.project_type_id = project_type_id
        self.project_type_name = project_type_name


class HECRASProject(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        plan,
        input_path,
        output_path,
        version=None,
        project_type_id=None,
        source_storage_id=None,
        destination_storage_id=None,
        source_path=None,  # default will be project_id
        destination_path=None,  # default will be project_id
        files_to_run=[],
        nfs=False,
    ):
        if not version and not project_type_id:
            raise Exception(
                "Either 'version' or 'project_type_id' parameter must be filled"
            )
        super(HECRASProject, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            project_type_name="HECRAS",
            source_path=source_path,
            destination_path=destination_path,
            project_type_id=project_type_id,
        )
        self.version = version
        self.plan = plan
        self.files_to_run = files_to_run
        self.nfs = nfs
        self.input_path = input_path
        self.output_path = output_path


class HECRASPlan(enum.Enum):
    ActivePlan = "Active Plan"
    AllPlans = "All Plans"
    ManuallySelect = "Manually Select"


class PythonProject(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        filename,
        cpu_count,
        version=None,
        project_type_id=None,
        source_storage_id=None,
        destination_storage_id=None,
        source_path=None,  # default will be project_id
        destination_path=None,  # default will be project_id
        arg=[],
        dependencies=[],
        env={},
    ):
        if not version and not project_type_id:
            raise Exception(
                "Either 'version' or 'project_type_id' parameter must be filled"
            )
        super(PythonProject, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            project_type_name="Python",
            source_path=source_path,
            destination_path=destination_path,
            project_type_id=project_type_id,
        )

        self.version = version
        self.filename = filename
        self.cpu_count = cpu_count
        self.arg = arg
        self.dependencies = dependencies
        self.env = env


class JuliaProject(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        filename,
        cpu_count,
        version=None,
        project_type_id=None,
        source_path=None,  # default will be project_id
        destination_path=None,  # default will be project_id
        source_storage_id=None,
        destination_storage_id=None,
        arg=[],
        dependencies=[],
        env={},
    ):
        if not version and not project_type_id:
            raise Exception(
                "Either 'version' or 'project_type_id' parameter must be filled"
            )
        super(JuliaProject, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            project_type_name="Julia",
            source_path=source_path,
            destination_path=destination_path,
            project_type_id=project_type_id,
        )
        self.version = version
        self.filename = filename
        self.cpu_count = cpu_count
        self.arg = arg
        self.dependencies = dependencies
        self.env = env


class RProject(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        filename,
        cpu_count,
        version=None,
        project_type_id=None,
        source_path=None,  # default will be project_id
        destination_path=None,  # default will be project_id
        source_storage_id=None,
        destination_storage_id=None,
        arg=[],
        dependencies=[],
        cran_dependencies=[],
        env={},
    ):
        if not version and not project_type_id:
            raise Exception(
                "Either 'version' or 'project_type_id' parameter must be filled"
            )
        super(RProject, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            project_type_name="R",
            source_path=source_path,
            destination_path=destination_path,
            project_type_id=project_type_id,
        )
        self.version = version
        self.filename = filename
        self.cpu_count = cpu_count
        self.arg = arg
        self.dependencies = dependencies
        self.cran_dependencies = cran_dependencies
        self.env = env


class STATAProject(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        filename,
        cpu_count,
        version=None,
        project_type_id=None,
        source_path=None,  # default will be project_id
        destination_path=None,  # default will be project_id
        source_storage_id=None,
        destination_storage_id=None,
        arg=[],
        dependencies=[],
        env={},
    ):
        if not version and not project_type_id:
            raise Exception(
                "Either 'version' or 'project_type_id' parameter must be filled"
            )
        super(STATAProject, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            project_type_name="STATA",
            source_path=source_path,
            destination_path=destination_path,
            project_type_id=project_type_id,
        )
        self.version = version
        self.filename = filename
        self.cpu_count = cpu_count
        self.arg = arg
        self.dependencies = dependencies
        self.env = env


class OctaveProject(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        filename,
        version=None,
        project_type_id=None,
        source_path=None,
        destination_path=None,
        source_storage_id=None,
        destination_storage_id=None,
        arg=[],
        dependencies=[],
    ):
        if not version and not project_type_id:
            raise Exception(
                "Either 'version' or 'project_type_id' parameter must be filled"
            )
        super(OctaveProject, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            project_type_name="Octave",
            source_path=source_path,
            destination_path=destination_path,
            project_type_id=project_type_id,
        )
        self.version = version
        self.filename = filename
        self.dependencies = dependencies
        self.arg = arg


class SWMM5Project(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        filename,
        version=None,
        project_type_id=None,
        source_path=None,
        destination_path=None,
        source_storage_id=None,
        destination_storage_id=None,
    ):
        if not version and not project_type_id:
            raise Exception(
                "Either 'version' or 'project_type_id' parameter must be filled"
            )
        super(SWMM5Project, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            project_type_name="SWMM5",
            source_path=source_path,
            destination_path=destination_path,
            project_type_id=project_type_id,
        )
        self.version = (version,)
        self.filename = filename


class AutoDockVinaProject(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        filename,
        version=None,
        project_type_id=None,
        source_path=None,
        destination_path=None,
        source_storage_id=None,
        destination_storage_id=None,
    ):
        if not version and not project_type_id:
            raise Exception(
                "Either 'version' or 'project_type_id' parameter must be filled"
            )
        super(AutoDockVinaProject, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            project_type_name="AutoDock Vina",
            source_path=source_path,
            destination_path=destination_path,
            project_type_id=project_type_id,
        )
        self.version = version
        self.filename = filename


class BioconductorProject(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        version=None,
        project_type_id=None,
        source_path=None,
        destination_path=None,
        source_storage_id=None,
        destination_storage_id=None,
    ):
        if not version and not project_type_id:
            raise Exception(
                "Either 'version' or 'project_type_id' parameter must be filled"
            )
        super(BioconductorProject, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            project_type_name="Bioconductor",
            source_path=source_path,
            destination_path=destination_path,
            project_type_id=project_type_id,
        )
        self.version = version


class BlenderProject(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        copy_in_path,
        copy_container_path,
        version=None,
        project_type_id=None,
        source_path=None,
        destination_path=None,
        source_storage_id=None,
        destination_storage_id=None,
    ):
        if not version and not project_type_id:
            raise Exception(
                "Either 'version' or 'project_type_id' parameter must be filled"
            )
        super(BlenderProject, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            project_type_name="Blender",
            source_path=source_path,
            destination_path=destination_path,
            project_type_id=project_type_id,
        )
        self.version = version
        self.copy_in_path = copy_in_path
        self.copy_container_path = copy_container_path


class QuantumEspressoProject(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        filename,
        version=None,
        project_type_id=None,
        source_path=None,
        destination_path=None,
        source_storage_id=None,
        destination_storage_id=None,
    ):
        if not version and not project_type_id:
            raise Exception(
                "Either 'version' or 'project_type_id' parameter must be filled"
            )
        super(QuantumEspressoProject, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            project_type_name="Quantum Espresso",
            source_path=source_path,
            destination_path=destination_path,
            project_type_id=project_type_id,
        )
        self.version = (version,)
        self.filename = filename


class FLO2DProject(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        filename,
        version=None,
        project_type_id=None,
        source_path=None,
        destination_path=None,
        source_storage_id=None,
        destination_storage_id=None,
    ):
        if not version and not project_type_id:
            raise Exception(
                "Either 'version' or 'project_type_id' parameter must be filled"
            )
        super(FLO2DProject, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            project_type_name="FLO2D",
            source_path=source_path,
            destination_path=destination_path,
            project_type_id=project_type_id,
        )
        self.version = version
        self.filename = filename


class MatLabProject(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        filename,
        version=None,
        project_type_id=None,
        source_path=None,
        destination_path=None,
        source_storage_id=None,
        destination_storage_id=None,
    ):
        if not version and not project_type_id:
            raise Exception(
                "Either 'version' or 'project_type_id' parameter must be filled"
            )
        super(MatLabProject, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            project_type_name="MatLab",
            source_path=source_path,
            destination_path=destination_path,
            project_type_id=project_type_id,
        )
        self.version = version
        self.filename = filename


class Dependency:
    def __init__(self, name, version):
        self.name = name
        self.version = version


class UpdateProjectRequest(CreateProjectRequest):
    def __init__(
        self,
        name,
        description,
        source_storage_id=None,
        destination_storage_id=None,
        source_path=None,
        destination_path=None,
        settings=None,
    ):
        super(CreateProjectRequest, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            source_path=source_path,
            destination_path=destination_path,
        )
        self.settings = settings
