from configparser import ConfigParser
import os

class Config:

    def __init__(self):
        self.parser = ConfigParser()
        self.filename = 'config.ini'
        self.is_configured = os.path.exists(self.filename)


    def load(self, section):
        self.parser.read(self.filename)
        data = {}
        if self.parser.has_section(section):
            params = self.parser.items(section)
            for param in params:
                data[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, self.filename))
        return data

    def save(self, section, data):
        if not self.is_configured:
            open(self.filename, 'w+').close()
        self.parser[section] = {}
        for key, value in data.items():
            self.parser[section][key] = str(value)

        with open(self.filename, 'w+') as config:
            self.parser.write(config)

        self.is_configured = True
