from configparser import ConfigParser

class Config():

    def __init__(self):
        self.parser = ConfigParser()

    def get_credentials(self, filename):
        self.parser.read(filename)
        database = {}
        section = 'postgresql'
        if self.parser.has_section(section):
            params = self.parser.items(section)
            for param in params:
                database[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        return database


    def save_credentials(self, user, password, database):
        open('database_setup/database.ini', "w+").close()
        self.parser.add_section('postgresql')

        self.parser['postgresql']['host'] = 'localhost'
        self.parser['postgresql']['user'] = user
        self.parser['postgresql']['password'] = password
        self.parser['postgresql']['database'] = database

        with open('database_setup/database.ini', 'w') as configfile:
            self.parser.write(configfile)
