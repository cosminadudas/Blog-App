from hashlib import sha256
from flask import session, abort

class AuthManager:

    @staticmethod
    def convert_to_hashed_password(password):
        hashed = sha256()
        hashed.update(password.encode())
        return hashed.hexdigest().upper()


    @staticmethod
    def login(user, password):
        hashed_password = AuthManager.convert_to_hashed_password(password)
        if user is not None and hashed_password == user.password:
            session['username'] = user.name
            session['id'] = user.user_id
        else:
            raise SyntaxError


    @staticmethod
    def logout():
        session.pop('username', None)
        session.pop('id', None)


    @staticmethod
    def admin_required():
        if 'username' in session and session['username'] != 'admin':
            return abort(403)
        return None
