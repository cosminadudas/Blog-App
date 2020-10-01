from configparser import ConfigParser

class Config():

    def __init__(self):
        self.parser = ConfigParser()

    def get_credentials(self, filename=('database_setup/database.ini'), section='postgresql'):
        # read config file
        self.parser.read(filename)
        # get section, default to postgresql
        database = {}
        if self.parser.has_section(section):
            params = self.parser.items(section)
            for param in params:
                database[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        return database
