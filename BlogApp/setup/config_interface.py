import abc
from models.database_setup_model import DatabaseSetupModel

class ConfigInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_credentials') and
                callable(subclass.get_credentials) and
                hasattr(subclass, 'save_credentials') and
                callable(subclass.save_credentials) or
                NotImplemented)

    @abc.abstractmethod
    def save_credentials(self, database_setup: DatabaseSetupModel):
        raise NotImplementedError
