from setup.config import Config
from models.database_credentials import DatabaseCredentials

class DatabaseConfig(Config):

    def __init__(self):
        self.section = 'postgresql'
        super().__init__()


    def load_credentials(self):
        data = super().load(self.section)
        database_credentials = DatabaseCredentials(data['user'],
                                                   data['password'],
                                                   data['database'])
        return database_credentials


    def save_credentials(self, database_setup: DatabaseCredentials):
        credentials = {
            "host": database_setup.host,
            "user": database_setup.user,
            "password": database_setup.password,
            "database": database_setup.database_name
        }

        super().save(self.section, credentials)
