from setup.database_config import DatabaseConfig
from setup.database_updates import queries
from setup.database import init_db, db_session


class DatabaseSetup:

    def __init__(self):
        self.session = db_session
        self.credentials = DatabaseConfig()
        self.latest_version = 3

    def is_updated(self):
        return self.credentials.get_version() == self.latest_version

    def update(self):
        for query in queries:
            self.session.execute(query)
        self.credentials.update_version()


    def create_database(self):
        init_db()
        if not self.is_updated:
            self.update()
