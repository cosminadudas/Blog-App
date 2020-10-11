from hashlib import sha256

class PasswordManager:

    @staticmethod
    def convert_to_hashed_password(password):
        hashed = sha256()
        hashed.update(password.encode())
        return hashed.hexdigest().upper()
