class ProjectsSdk:
    def __init__(self, projects_service):
        self._projects_service = projects_service

    def list_projects(
        self, ids=None, names=None, user_ids=None, page=1, items=25,
    ):
        """
        Get list of projects

        :param ids: Optional[List[str]]: Filter by project id
        :param names: Optional[List[str]]: Filter by project name
        :param user_ids: Optional[List[str]]: Filter by user ids
        :param page: Optional[int]: Page #
        :param items: Optional[int]: # of items per page
        :return: List[Project]
        """
        return self._projects_service.list_projects(
            ids=ids, names=names, user_ids=user_ids, page=page, items=items
        )

    def create_project(self, create_project_request):
        """
        Create a project
        :param: CreateProjectRequest
        :return: Project
        """
        return self._projects_service.create_project(create_project_request)

    def upload(self, project_id, directory):
        """
        Upload a directory

        :param project_id: str: Project you want to upload the file to
        :param directory: str: Path to folder that you want to upload
        :return: bool
        """
        return self._projects_service.upload(project_id, directory)

    def run_job_on_station(self, project_id, station_id):
        """
        Run a job on a station

        :param project_id: str
        :param station_id: str
        :return: Job
        """
        return self._projects_service.run_job_on_station(project_id, station_id)

    def run_job_on_machine(self, project_id, station_id, machine_id):
        """
        Run a job on a machine

        :param project_id: str
        :param station_id: str
        :param machine_id: str
        :return: Job
        """
        return self._projects_service.run_job_on_machine(
            project_id, station_id, machine_id
        )

    def create_and_upload_project(self, create_project_request, directory):
        project = self._projects_service.create_project(create_project_request)
        self._projects_service.upload(project.project_id, directory)
        return project

    def create_project_and_run_job(
        self, create_project_request, directory, station_id, machine_id=None,
    ):
        """

        :param create_project_request:
        :param directory: str: filepath to the folder you want to upload
        :param station_id: str: station id the project will be ran in
        :param machine_id: Optional[str] if you want to run on a specific machine
        :return: Job
        """
        project = self._projects_service.create_project(create_project_request)
        self._projects_service.upload(project.project_id, directory)
        if machine_id:
            job = self._projects_service.run_job_on_machine(
                project.project_id, station_id, machine_id
            )
        else:
            job = self._projects_service.run_job_on_station(
                project.project_id, station_id
            )

        return job

    def inspect_project(self, project_id):
        """
        Provides the metadata of all files in a project
        :param project_id: project you want to inspect
        :return: DirectoryListing
        """

        return self._projects_service.inspect_project(project_id)

    def delete_file(self, project_id):
        return self._projects_service.delete_file(project_id)

    def update_project(self, project_id, update_project_request):
        return self._projects_service.update_project(project_id, update_project_request)

    def update_project_args(self, project_id, args):
        return self._projects_service.update_project(project_id, args)

    def delete_project_files(self, project_id):
        return self._projects_service.delete_project_files(project_id)

    def get_project_types(self):
        """

        :return:
        """
        return self._projects_service.get_project_types()
