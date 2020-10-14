import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from setup.database_config import DatabaseConfig

COMMAND = """ CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY UNIQUE NOT NULL,
                owner TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP,
                modified_at TIMESTAMP
                )
        """

class DatabaseSetup():

    def __init__(self):
        self.conn = None
        self.credentials = DatabaseConfig()
        self.version = self.get_credentials_version()


    def get_credentials_version(self):
        return self.credentials.get_version()



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


    def create_table(self, command):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(command)
        self.close()

    def create_database(self):
        db_credentials = self.credentials.load_credentials()
        conn = psycopg2.connect(user=db_credentials.user, password=db_credentials.password)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        try:
            cur.execute("CREATE DATABASE {}".format(db_credentials.database_name))
            conn.close()
        except psycopg2.DatabaseError:
            pass
        self.create_table(COMMAND)
