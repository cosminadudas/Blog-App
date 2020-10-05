import os
from setup.config import Config

class DatabaseConfig(Config):

    def is_configured(self):
        return  os.path.exists('setup/database.ini')

    def get_credentials(self, filename, section):
        self.parser.read(filename)
        database = {}
        if self.parser.has_section(section):
            params = self.parser.items(section)
            for param in params:
                database[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        return database


    def save_credentials(self, section, user, password, database):
        open('setup/database.ini', "w+").close()
        self.parser.add_section(section)

        self.parser[section]['host'] = 'localhost'
        self.parser[section]['user'] = user
        self.parser[section]['password'] = password
        self.parser[section]['database'] = database

        with open('setup/database.ini', 'w') as configfile:
            self.parser.write(configfile)
