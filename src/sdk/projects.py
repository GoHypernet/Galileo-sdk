from ..business.services.projects import ProjectsService


class ProjectsSdk:
    def __init__(self, projects_service: ProjectsService):
        self._projects_service = projects_service

    def create_project(self):
        return self._projects_service.create_project()

    def run_job_on_station(self, project_id: str, station_id: str):
        return self._projects_service.run_job_on_station(project_id, station_id)

    def run_job_on_machine(self, project_id: str, station_id: str, machine_id: str):
        return self._projects_service.run_job_on_machine(
            project_id, station_id, machine_id
        )
