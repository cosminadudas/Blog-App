import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from database_setup.config import Config

class Database():

    def __init__(self):
        self.conn = None
        self.credentials = Config()


    def connect(self):
        self.conn = psycopg2.connect(
            **self.credentials.get_credentials(
                'database_setup/database.ini'))

    def close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
        else:
            print("cosmina")

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
