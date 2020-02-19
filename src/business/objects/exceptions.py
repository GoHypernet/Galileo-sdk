from typing import Optional


class JobsException(Exception):
    def __init__(self, job_id: str, msg: [Optional[str]] = None):
        self.job_id = job_id
        super().__init__(msg)
