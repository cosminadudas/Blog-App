from hashlib import sha256

class PasswordManager:

    @staticmethod
    def hash(password):
        hashed = sha256()
        hashed.update(password.encode())
        if password == '':
            return ''
        return hashed.hexdigest().upper()
