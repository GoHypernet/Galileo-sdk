from enum import Enum

from ...config.settings import development, local, production


class Config(Enum):
    Local: "local"
    Development: "development"
    Production: "production"


class Settings:
    def __init__(self):
        self.backend = ""


class SettingsRepository:
    def __init__(self, config):
        self._settings = Settings()

        if Config.Production == config:
            self._settings.backend = production.BACKEND
        elif Config.Development == config:
            self._settings.backend = development.BACKEND
        else:
            self._settings.backend = local.BACKEND

    def get_settings(self):
        return self._settings
