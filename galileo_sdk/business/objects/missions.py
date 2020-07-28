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


class Mission:
    def __init__(
        self,
        mission_id,
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
        self.mission_id = mission_id
        self.name = name
        self.description = description
        self.source_storage_id = source_storage_id
        self.source_path = source_path
        self.destination_storage_id = destination_storage_id
        self.destination_path = destination_path
        self.user_id = user_id
        self.creation_timestamp = creation_timestamp
        self.project_type_id = project_type_id


class MissionType:
    def __init__(self, id, name, description, version):
        self.id = id
        self.name = name
        self.description = description
        self.version = version


class CreateMissionRequest(object):
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


class HECRASMission(CreateMissionRequest):
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
        super(HECRASMission, self).__init__(
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


class PythonMission(CreateMissionRequest):
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
        super(PythonMission, self).__init__(
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


class JuliaMission(CreateMissionRequest):
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
        super(JuliaMission, self).__init__(
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


class RMission(CreateMissionRequest):
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
        super(RMission, self).__init__(
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


class STATAMission(CreateMissionRequest):
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
        super(STATAMission, self).__init__(
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


class OctaveMission(CreateMissionRequest):
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
        super(OctaveMission, self).__init__(
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


class SWMM5Mission(CreateMissionRequest):
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
        super(SWMM5Mission, self).__init__(
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


class AutoDockVinaMission(CreateMissionRequest):
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
        super(AutoDockVinaMission, self).__init__(
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


class BioconductorMission(CreateMissionRequest):
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
        super(BioconductorMission, self).__init__(
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


class BlenderMission(CreateMissionRequest):
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
        super(BlenderMission, self).__init__(
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


class QuantumEspressoMission(CreateMissionRequest):
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
        super(QuantumEspressoMission, self).__init__(
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


class FLO2DMission(CreateMissionRequest):
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
        super(FLO2DMission, self).__init__(
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


class MatLabMission(CreateMissionRequest):
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
        super(MatLabMission, self).__init__(
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


class UpdateMissionRequest(CreateMissionRequest):
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
        super(CreateMissionRequest, self).__init__(
            name=name,
            description=description,
            source_storage_id=source_storage_id,
            destination_storage_id=destination_storage_id,
            source_path=source_path,
            destination_path=destination_path,
        )
        self.settings = settings
