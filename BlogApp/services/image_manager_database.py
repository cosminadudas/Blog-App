import os
from exceptions import FormatFileNotAccepted
from services.image_manager_interface import ImageManagerInterface

class ImageManagerDatabase(ImageManagerInterface):

    def __init__(self):
        self.source = os
        self.allowed_formats = ['JPG', 'JPEG', 'PNG']

    def save_image(self, new_image):
        if not self.verify_format(new_image.filename):
            raise FormatFileNotAccepted
        new_image.save(self.source.path.join('./static/images', new_image.filename))

    def delete_image(self, filename):
        filename = filename.split('/')[-1]
        if str(filename) != 'default.png' and self.verify_image_already_exists(filename):
            self.source.remove('./static/images/' + str(filename))

    def edit_image(self, new_image, old_image):
        if not self.verify_format(new_image.filename):
            raise FormatFileNotAccepted
        self.delete_image(old_image)
        self.save_image(new_image)

    def verify_image_already_exists(self, filename):
        return self.source.path.exists('./static/images/' + str(filename))

    def rename_image(self, image, post_id):
        if image.filename == '':
            return ''
        if self.verify_image_already_exists(image.filename) and image.filename != 'default.png':
            image.filename = str(post_id) + image.filename
            image.name = str(post_id) + image.name
        return image.filename

    def verify_format(self, filename):
        return filename.split('.')[1].upper() in self.allowed_formats
