import psycopg2
from database_setup.config import Config

class Database():

    def __init__(self):
        self.conn = None
        self.database = Config()


    def connect(self):
        self.conn = psycopg2.connect(**self.database.get_credentials())


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
