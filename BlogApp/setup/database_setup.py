import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from setup.database_config import DatabaseConfig
from setup.database_updates import queries


class DatabaseSetup():

    def __init__(self):
        self.conn = None
        self.credentials = DatabaseConfig()
        self.version = self.credentials.get_version()
        self.latest_version = 2


    def update(self):
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
        except psycopg2.DatabaseError:
            pass

        if self.version == self.latest_version:
            conn.close()
            return

        for query in queries:
            try:
                cur.execute(query)
            except psycopg2.DatabaseError:
                pass
            conn.commit()
        self.update()
        conn.close()
