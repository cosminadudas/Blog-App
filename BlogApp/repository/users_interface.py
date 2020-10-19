import abc
from models.user import User

class UsersInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'add') and
                callable(subclass.add) and
                hasattr(subclass, 'edit') and
                callable(subclass.edit) and
                hasattr(subclass, 'delete') and
                callable(subclass.delete) and
                hasattr(subclass, 'get_all_users') and
                callable(subclass.get_all_users) and
                hasattr(subclass, 'get_user_by_id') and
                callable(subclass.get_user_by_id) and
                hasattr(subclass, 'get_user_by_name_or_email') and
                callable(subclass.get_user_by_name_or_email) or
                NotImplemented)


    @abc.abstractmethod
    def add(self, new_user: User):
        raise NotImplementedError


    @abc.abstractmethod
    def edit(self, user_to_edit, new_name, new_email, new_password):
        raise NotImplementedError


    @abc.abstractmethod
    def delete(self, user_id):
        raise NotImplementedError


    @abc.abstractmethod
    def get_all_users(self):
        raise NotImplementedError


    @abc.abstractmethod
    def get_user_by_id(self, user_id):
        raise NotImplementedError


    @abc.abstractmethod
    def get_user_by_name_or_email(self, name_or_email):
        raise NotImplementedError

    @abc.abstractmethod
    def verify_user_already_exist(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def are_credentials_unavailable(self, user_to_edit, new_name, new_email):
        raise NotImplementedError
