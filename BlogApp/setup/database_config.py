from setup.config_interface import ConfigInterface
from setup.config import Config
from models.database_setup_model import DatabaseSetupModel

class DatabaseConfig(ConfigInterface, Config):

    def __init__(self):
        self.filename = 'config.ini'
        self.section = 'postgresql'
        super().__init__(self.filename)


    def save_credentials(self, database_setup: DatabaseSetupModel):
        """Saves data into a specified file"""
        credentials = {
            "host": database_setup.host,
            "user": database_setup.user,
            "password": database_setup.password,
            "database": database_setup.database_name
        }

        super().save(database_setup.section, credentials)
