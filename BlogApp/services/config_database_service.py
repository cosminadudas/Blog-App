from injector import inject
from setup.config import Config

class ConfigDatabaseService:
    @inject
    def __init__(self, database_config: Config):
        self.database_config = database_config


    def save_credentials(self, section, user, password, database):
        return self.database_config.save_credentials(section, user, password, database)

    def is_configured(self):
        return self.database_config.is_configured()
