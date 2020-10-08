import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from setup.database_config import DatabaseConfig

COMMAND = """ CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
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


    def connect(self):
        database_credentials = self.credentials.load_credentials()
        self.conn = psycopg2.connect("user={} password={}".format(database_credentials.user,
                                                                  database_credentials.password))

    def close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()


    def create_table(self, command):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(command)
        self.close()

    def create_database(self, database_name):
        self.connect()
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = self.conn.cursor()
        try:
            cur.execute("CREATE DATABASE {}".format(database_name))
            self.conn.close()
        except psycopg2.DatabaseError:
            pass
        self.create_table(COMMAND)
