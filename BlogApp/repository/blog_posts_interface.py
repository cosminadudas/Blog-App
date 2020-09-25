import abc
from models.blog_post import BlogPost

class BlogPostsInterface(metaclass=abc.ABCMeta):
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
    def get_all_posts(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_post_by_id(self, post_id):
        raise NotImplementedError

    @abc.abstractmethod
    def count(self):
        raise NotImplementedError


    @abc.abstractmethod
    def add(self, new_post: BlogPost):
        raise NotImplementedError


    @abc.abstractmethod
    def edit(self, post_id, new_title, new_content):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, post_id):
        raise NotImplementedError
