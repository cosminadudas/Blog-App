import abc

class UserInterface(metaclass=abc.ABCMeta):
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
                callable(subclass.get_user_by_id) or
                NotImplemented)


    @abc.abstractmethod
    def add(self):
        raise NotImplementedError


    @abc.abstractmethod
    def edit(self):
        raise NotImplementedError


    @abc.abstractmethod
    def delete(self):
        raise NotImplementedError


    @abc.abstractmethod
    def get_all_users(self):
        raise NotImplementedError


    @abc.abstractmethod
    def get_user_by_id(self):
        raise NotImplementedError
