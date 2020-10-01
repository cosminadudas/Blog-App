import psycopg2
from database_setup.config import Config

class Database():

    def __init__(self):
        self.conn = None
        self.credentials = Config()


    def connect(self):
        self.conn = psycopg2.connect(**self.credentials.get_credentials())
        
    
    def is_set_up(self):
        return self.credentials.is_config()


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


    def create_database(self):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("CREATE DATABASE blog")
        self.close()