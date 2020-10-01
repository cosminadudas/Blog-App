import psycopg2
from database_setup.config import Config

class Database():

    def __init__(self):
        self.conn = None
        self.credentials = Config()


    def connect(self):
        self.conn = psycopg2.connect(**self.credentials.get_credentials())


    def close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
        else:
            pass

    def create_table(self, command):
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(command)


    def create_database(self, db_name):
        self.connect()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("CREATE DATABASE " + db_name)
        self.close()