import os

class ImageManager:

    @staticmethod
    def save_image(new_image):
        new_image.save(os.path.join('./static/images', new_image.filename))

    @staticmethod
    def delete_image(filename):
        if str(filename) != 'default.png' and ImageManager.verify_image_already_exists(filename):
            os.remove('./static/images/' + str(filename))

    @staticmethod
    def verify_image_already_exists(filename):
        return os.path.exists('./static/images/' + str(filename))

    @staticmethod
    def rename_image(image):
        image.filename = '0' + image.filename
        image.name = '0' + image.name

    @staticmethod
    def verify_format(filename):
        allowed_formats = ['jpg', 'jpeg', 'png']
        if filename.split('.')[1] in allowed_formats:
            return True
        return False
