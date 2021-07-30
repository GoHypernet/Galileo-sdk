from ...config.settings import development, production


class Settings:
    def __init__(self):
        """
        SDK Settings
        """
        self.backend = ""
        self.universe = None


class SettingsRepository:
    def __init__(self, config):
        """
        Setups the SettingsRepository for GalileoSDK
        :param config: Which Backend to use (production, development, or custom URL)
        """
        self._settings = Settings()

        if "production" == config:
            self._settings.backend = production.BACKEND
        elif "development" == config:
            self._settings.backend = development.BACKEND
        else:
            self._settings.backend = config

    def get_settings(self):
        """
        Gets the current SDK Settings

        :return: SDK settings
        :rtype: Settings
        """
        return self._settings
