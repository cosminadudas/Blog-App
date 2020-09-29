from configparser import ConfigParser
import psycopg2

def config(filename=('database_setup/database.ini'), section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    database = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            database[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return database

class Database():

    def __init__(self):
        self.conn = None
        self.database = config()


    def connect(self):
        self.conn = psycopg2.connect(**self.database)


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
