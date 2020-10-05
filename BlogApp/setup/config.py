from abc import ABC, abstractmethod
from configparser import ConfigParser

class Config(ABC):
    def __init__(self):
        self.parser = ConfigParser()


    @abstractmethod
    def is_configured(self):
        pass


    @abstractmethod
    def get_credentials(self, filename, section):
        pass

    @abstractmethod
    def save_credentials(self, section, user, password, database):
        pass
