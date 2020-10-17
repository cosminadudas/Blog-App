from exceptions import LoginError
from injector import inject
from flask import session
from services.password_manager import PasswordManager
from repository.users_interface import UsersInterface


class Authentication:

    @inject
    def __init__(self, users: UsersInterface):
        self.users = users
        self.session = None


    def login(self, name_or_email, password):
        user = self.users.get_user_by_name_or_email(name_or_email)
        hashed_password = PasswordManager.hash(password)
        if hashed_password == user.password:
            session['username'] = user.name
            session['id'] = user.user_id
        else:
            raise LoginError


    def logout(self):
        session.pop('username', None)
        session.pop('id', None)
        self.session = session
