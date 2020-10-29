import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from setup.database_config import DatabaseConfig
from setup.database_updates import queries


class DatabaseSetup:

    def __init__(self):
        self.conn = None
        self.credentials = DatabaseConfig()
        self.latest_version = 3

    def is_updated(self):
        return self.credentials.get_version() == self.latest_version

    def update(self):
        db_credentials = self.credentials.load_credentials()
        conn = psycopg2.connect(user=db_credentials.user,
                                password=db_credentials.password,
                                database=db_credentials.database_name)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        for query in queries:
            cur.execute(query)
        conn.close()
        self.credentials.update_version()

    def connect(self):
        database_credentials = self.credentials.load_credentials()
        self.conn = psycopg2.connect(
            user=database_credentials.user,
            password=database_credentials.password,
            database=database_credentials.database_name
            )

    def close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()

    def create_database(self):
        db_credentials = self.credentials.load_credentials()
        conn = psycopg2.connect(user=db_credentials.user, password=db_credentials.password)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        try:
            cur.execute("CREATE DATABASE {}".format(db_credentials.database_name))
            conn.close()
            if not self.is_updated():
                self.update()
        except psycopg2.DatabaseError:
            conn.close()
            if not self.is_updated():
                self.update()
