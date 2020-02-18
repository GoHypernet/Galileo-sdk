from ..business.services.projects import ProjectsService


class ProjectsSdk:
    def __init__(self, projects_service: ProjectsService):
        self._projects_service = projects_service

    def create_project(self):
        """
        Create a project

        :return: {"project": Project}
        """
        return self._projects_service.create_project()

    def upload_single_file(self, project_id: str):
        """
        Upload a single file

        :param project_id: Project you want to upload the file to
        :return: boolean
        """
        return self._projects_service.upload_single_file(project_id)

    def run_job_on_station(self, project_id: str, station_id: str):
        """
        Run a job on a station

        :param project_id: Project id
        :param station_id: Station id
        :return: {"job": Job}
        """
        return self._projects_service.run_job_on_station(project_id, station_id)

    def run_job_on_machine(self, project_id: str, station_id: str, machine_id: str):
        """
        Run a job on a machine

        :param project_id: Project id
        :param station_id: Station id
        :param machine_id: Machine id
        :return: {"job": Job}
        """
        return self._projects_service.run_job_on_machine(
            project_id, station_id, machine_id
        )
