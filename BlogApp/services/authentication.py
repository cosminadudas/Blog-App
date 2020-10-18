from exceptions import LoginError, UserNotSetupError
from injector import inject
from flask import session, redirect
from services.password_manager import PasswordManager
from repository.users_interface import UsersInterface


class Authentication:

    @inject
    def __init__(self, users: UsersInterface):
        self.users = users
        self.user = None
        self.session = None


    def login(self, name_or_email, password):
        self.user = self.users.get_user_by_name_or_email(name_or_email)
        if self.user.password == '':
            raise UserNotSetupError
        hashed_password = PasswordManager.hash(password)
        if hashed_password == self.user.password:
            session['username'] = self.user.name
            session['id'] = self.user.user_id
            return redirect('/home')
        raise LoginError

    def logout(self):
        session.pop('username', None)
        session.pop('id', None)
        self.session = session
        self.user = None
