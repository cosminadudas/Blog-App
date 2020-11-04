from setup.config import Config
from models.database_credentials import DatabaseCredentials


class DatabaseConfig(Config):

    def __init__(self):
        self.section = 'postgresql'
        super().__init__()

    def get_version(self):
        data = super().load(self.section)
        if 'version' not in data:
            super().update(self.section, 'version', '1')
            data_updated = super().load(self.section)
            return int(data_updated['version'])

        return int(data['version'])

    def update_version(self, updated_version):
        super().update(self.section, 'version', updated_version)

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
