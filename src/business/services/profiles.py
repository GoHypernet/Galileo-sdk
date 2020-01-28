class ProfilesService:
    def __init__(self, profile_repo):
        self._profile_repo = profile_repo

    def list_users(self, page, items):
        self._profile_repo(page, items)
