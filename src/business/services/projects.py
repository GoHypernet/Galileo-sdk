from ...data.repositories.projects import ProjectsRepository


class ProjectsService:
    def __init__(self, projects_repo: ProjectsRepository):
        self._projects_repo = projects_repo

    def create_project(self):
        r = self._projects_repo.create_project()
        return r.json()

    def run_job_on_station(self, project_id: str, station_id: str):
        r = self._projects_repo.run_job_on_station(project_id, station_id)
        return r.json()

    def run_job_on_machine(self, project_id: str, station_id: str, machine_id: str):
        r = self._projects_repo.run_job_on_machine(project_id, station_id, machine_id)
        return r.json()
