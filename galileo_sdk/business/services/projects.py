import os

from ..utils.generate_query_str import generate_query_str
from ..objects import UpdateProjectRequest, CreateProjectRequest


class ProjectsService:
    def __init__(self, projects_repo):
        self._projects_repo = projects_repo

    def list_projects(
        self, ids=None, names=None, user_ids=None, page=1, items=25,
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

        return self._projects_repo.list_projects(query)

    def create_project(
        self,
        name,
        description="",
        source_storage_id=None,
        destination_storage_id=None,
        project_type_name=None,
        source_path=None,
        destination_path=None,
        project_type_id=None,
    ):

        # if not project_type_id:
        #     project_types = self.get_project_types()
        #     for project_type in project_types:
        #         if project_type.version == create_project_request.version and \
        #                 project_type.name == create_project_request.project_type_name:
        #             create_project_request.project_type_id = project_type.id
        #
        #     if not create_project_request.project_type_id:
        #         raise Exception("Version of this project type is not found")

        return self._projects_repo.create_project(
            CreateProjectRequest(
                name,
                description,
                source_storage_id,
                destination_storage_id,
                project_type_name,
                source_path,
                destination_path,
                project_type_id,
            )
        )

    def upload(self, project_id, dir):
        name = os.path.basename(dir)
        for root, dirs, files in os.walk(dir):
            for file in files:
                basename = os.path.basename(root)
                if basename == name:
                    filename = file
                else:
                    filename = os.path.join(os.path.basename(root), file)

                filename = filename.replace(" ", "_")

                filepath = os.path.join(os.path.abspath(root), file)
                f = open(filepath, "rb").read()
                self._projects_repo.upload_single_file(project_id, f, filename)
        return True

    def run_job_on_station(self, project_id, station_id):
        return self._projects_repo.run_job_on_station(project_id, station_id)

    def run_job_on_lz(self, project_id, station_id, lz_id):
        return self._projects_repo.run_job_on_lz(
            project_id, station_id, lz_id
        )

    def get_project_files(self, project_id):
        return self._projects_repo.get_project_files(project_id)

    def delete_project(self, project_id):
        return self._projects_repo.delete_project(project_id)

    def update_project(self, project_id, update_project_request):
        return self._projects_repo.update_project(project_id, update_project_request)

    def update_project_args(self, project_id, args):
        update_project_request = UpdateProjectRequest(
            None, None, None, None, None, args
        )
        return self._projects_repo.update_project(project_id, update_project_request)

    def delete_project_files(self, project_id):
        return self._projects_repo.delete_project_files(project_id)

    def get_project_types(self):
        return self._projects_repo.get_project_types()
