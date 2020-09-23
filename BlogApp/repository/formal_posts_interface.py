import abc
from models.BlogPost import BlogPost

class FormalPostsInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'add') and 
                callable(subclass.add) and 
                hasattr(subclass, 'edit') and 
                callable(subclass.edit) and
                hasattr(subclass, 'delete') and 
                callable(subclass.delete) or 
                NotImplemented)


    @abc.abstractmethod
    def add(self, new_post : BlogPost):
        raise NotImplementedError


    @abc.abstractmethod
    def edit(self, post_id, new_title, new_content):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, post_id):
        raise NotImplementedError

