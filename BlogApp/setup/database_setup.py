import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from setup.database_config import DatabaseConfig


class DatabaseSetup():

    def __init__(self):
        self.conn = None
        self.credentials = DatabaseConfig()


    def connect(self):
        self.conn = psycopg2.connect(
            **self.credentials.load('postgresql'))

    def close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()


    def create_table(self, command):
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(command)


    def create_database(self, database_name, user, password):
        self.conn = psycopg2.connect("user={} password={}".format(user, password))
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = self.conn.cursor()
        cur.execute("CREATE DATABASE {}".format(database_name))
        self.conn.close()
