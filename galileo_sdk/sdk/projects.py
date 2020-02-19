from typing import Any, List, Optional

from ..business.services.projects import ProjectsService


class ProjectsSdk:
    def __init__(self, projects_service: ProjectsService):
        self._projects_service = projects_service

    def list_projects(
        self,
        ids: Optional[List[str]] = None,
        names: Optional[List[str]] = None,
        user_ids: Optional[List[str]] = None,
        page: Optional[int] = 1,
        items: Optional[int] = 25,
    ):
        """
        Get list of projects

        :param ids: Filter by project id
        :param names: Filter by project name
        :param user_ids: Filter by user ids
        :param page: Page #
        :param items: # of items per page
        :return: {"projects": Projects}
        """
        return self._projects_service.list_projects(
            ids=ids, names=names, user_ids=user_ids, page=page, items=items
        )

    def create_project(self, name: str, description: str):
        """
        Create a project

        :return: {"project": Project}
        """
        return self._projects_service.create_project(name, description)

    def upload(self, project_id: str, file: Any, filename: str):
        """
        Upload a single file

        :param project_id: Project you want to upload the file to
        :param file:
        :param filename:
        :return: boolean
        """
        return self._projects_service.upload(project_id, file, filename)

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
