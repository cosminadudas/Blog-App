import base64
from exceptions import FormatFileNotAccepted
from services.image_manager_interface import ImageManagerInterface

class ImageManagerInMemory(ImageManagerInterface):
    def __init__(self):
        self.source = base64
        self.allowed_formats = ['JPG', 'JPEG', 'PNG']

    def edit_image(self, new_image, old_image):
        if not self.verify_format(new_image.filename):
            raise FormatFileNotAccepted
        image = new_image.read()
        image = self.source.b64encode(image).decode('ascii')
        return 'data:image/png;base64, ' + image

    def save_image(self, new_image):
        if not self.verify_format(new_image.filename):
            raise FormatFileNotAccepted
        image = new_image.read()
        image = self.source.b64encode(image).decode('ascii')
        return 'data:image/png;base64, ' + image

    def verify_format(self, filename):
        return filename.split('.')[1].upper() in self.allowed_formats

    def delete_image(self, filename):
        pass

    def verify_image_already_exists(self, filename):
        pass

    def rename_image(self, image, post_id):
        pass
