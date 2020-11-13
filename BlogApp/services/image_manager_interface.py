import abc

class ImageManagerInterface(metaclass=abc.ABCMeta):

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
    def save_image(self, new_image):
        raise NotImplementedError

    @abc.abstractmethod
    def edit_image(self, new_image, old_image):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_image(self, filename):
        raise NotImplementedError

    @abc.abstractmethod
    def verify_image_already_exists(self, filename):
        raise NotImplementedError

    @abc.abstractmethod
    def rename_image(self, image, post_id):
        raise NotImplementedError


    @abc.abstractmethod
    def verify_format(self, filename):
        raise NotImplementedError
