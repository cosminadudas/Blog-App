from exceptions import LoginError
from flask import session
from services.password_manager import PasswordManager
from repository.users_interface import UsersInterface


class AuthenticationManager:

    @staticmethod
    def login(user, password):
        hashed_password = PasswordManager.hash(password)
        if hashed_password == user.password:
            session['username'] = user.name
            session['id'] = user.user_id
        else:
            raise LoginError


    @staticmethod
    def logout():
        session.pop('username', None)
        session.pop('id', None)


    @staticmethod
    def set_password(users: UsersInterface, user, password):
        if user is not None:
            if user.password != '':
                return
            users.edit(user.user_id, user.name, user.email, password)
