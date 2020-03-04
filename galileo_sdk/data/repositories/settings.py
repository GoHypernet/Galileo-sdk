from ...config.settings import development, production


class Settings:
    def __init__(self):
        self.backend = ""


class SettingsRepository:
    def __init__(self, config):
        self._settings = Settings()

        if "production" == config:
            self._settings.backend = production.BACKEND
        elif "development" == config:
            self._settings.backend = development.BACKEND
        else:
            self._settings.backend = config

    def get_settings(self):
        return self._settings
