import os
from typing import Any, List, Optional

from galileo_sdk.business.objects import Job
from galileo_sdk.business.objects.projects import DirectoryListing, Project

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
    ) -> List[Project]:
        query = generate_query_str(
            {
                "ids": ids,
                "names": names,
                "user_ids": user_ids,
                "page": page,
                "items": items,
            }
        )

        return self._projects_repo.list_projects(query)

    def create_project(self, name: str, description: str) -> Project:
        return self._projects_repo.create_project(name, description)

    def upload(self, project_id: str, dir: str) -> bool:
        name = os.path.basename(dir)
        for root, dirs, files in os.walk(dir):
            for file in files:
                basename = os.path.basename(root)
                if basename == name:
                    filename = file
                else:
                    filename = os.path.join(os.path.basename(root), file)

                filepath = os.path.join(os.path.abspath(root), file)
                f = open(filepath, "rb").read()
                self._projects_repo.upload_single_file(project_id, f, filename)
        return True

    def run_job_on_station(self, project_id: str, station_id: str) -> Job:
        return self._projects_repo.run_job_on_station(project_id, station_id)

    def run_job_on_machine(
        self, project_id: str, station_id: str, machine_id: str
    ) -> Job:
        return self._projects_repo.run_job_on_machine(
            project_id, station_id, machine_id
        )

    def inspect_project(self, project_id: str) -> DirectoryListing:
        return self._projects_repo.inspect_project(project_id)
