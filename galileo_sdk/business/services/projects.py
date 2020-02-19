from typing import Any, List, Optional
import os

from ...data.repositories.projects import ProjectsRepository
from ..utils.generate_query_str import generate_query_str


class ProjectsService:
    def __init__(self, projects_repo: ProjectsRepository):
        self._projects_repo = projects_repo

    def list_projects(
        self,
        ids: Optional[List[str]] = None,
        names: Optional[List[str]] = None,
        user_ids: Optional[List[str]] = None,
        page: Optional[int] = 1,
        items: Optional[int] = 25,
    ):
        query = generate_query_str(
            {
                "ids": ids,
                "names": names,
                "user_ids": user_ids,
                "page": page,
                "items": items,
            }
        )

        r = self._projects_repo.list_projects(query)
        return r.json()

    def create_project(self, name: str, description: str):
        r = self._projects_repo.create_project(name, description)
        return r.json()

    def upload(self, project_id: str, dir: Any, name: str):
        for root, dirs, files in os.walk(dir):
            for file in files:
                basename = os.path.basename(root)
                if basename == name:
                    filename = file
                else:
                    filename = os.path.join(os.path.basename(root), file)

                filepath = os.path.join(os.path.abspath(root), file)
                self._projects_repo.upload_single_file(project_id, filepath, filename)
        return True

    def run_job_on_station(self, project_id: str, station_id: str):
        r = self._projects_repo.run_job_on_station(project_id, station_id)
        return r.json()

    def run_job_on_machine(self, project_id: str, station_id: str, machine_id: str):
        r = self._projects_repo.run_job_on_machine(project_id, station_id, machine_id)
        return r.json()
