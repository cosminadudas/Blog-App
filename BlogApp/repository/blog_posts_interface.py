import abc
from models.blog_post import BlogPost
from models.pagination import Pagination

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
    def verify_if_owner_is_user(self, owner):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_posts(self, user, pagination: Pagination):
        raise NotImplementedError

    @abc.abstractmethod
    def get_post_by_id(self, post_id):
        raise NotImplementedError

    @abc.abstractmethod
    def count(self, user):
        raise NotImplementedError


    @abc.abstractmethod
    def add(self, new_post: BlogPost):
        raise NotImplementedError


    @abc.abstractmethod
    def edit(self, post_id, new_title, new_content, new_image):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, post_id):
        raise NotImplementedError
