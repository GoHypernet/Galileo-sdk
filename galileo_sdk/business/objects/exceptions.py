class JobsException(Exception):
    def __init__(self, job_id, msg=None):
        self.job_id = job_id
        super().__init__(msg)
