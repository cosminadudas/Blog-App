from datetime import datetime
from exceptions import UserAlreadyExists
from sqlalchemy import desc, or_
from repository.users_interface import UsersInterface
from repository.models.user_db import UserDb
from models.user import User
from setup.database_setup import DatabaseSetup
from services.password_manager import PasswordManager


class UsersDatabaseRepository(UsersInterface):

    def __init__(self):
        self.database = DatabaseSetup()

    def add(self, new_user: User):
        if self.verify_user_already_exist(new_user):
            raise UserAlreadyExists
        hashed_password = PasswordManager.hash(new_user.password)
        new_user.created_at = datetime.now()
        user_to_add = UserDb(new_user.name,
                             new_user.email,
                             hashed_password,
                             new_user.created_at)
        session = self.database.get_session()
        session.add(user_to_add)
        session.commit()
        command = session.query(UserDb)
        new_user.user_id = command.filter_by(name=new_user.name).first().id

    def edit(self, user_to_edit: User, new_name, new_email, new_password):
        if self.are_credentials_unavailable(user_to_edit, new_name, new_email):
            raise UserAlreadyExists
        session = self.database.get_session()
        user = session.query(UserDb).filter_by(id=user_to_edit.user_id).first()
        hashed_new_password = PasswordManager.hash(new_password)
        if new_password == "":
            user.name = new_name
            user.email = new_email
        else:
            user.name = new_name
            user.email = new_email
            user.password = hashed_new_password
        user.modified_at = datetime.now()
        session.commit()

    def delete(self, user_id):
        session = self.database.get_session()
        session.query(UserDb).filter_by(id=user_id).delete()
        session.commit()

    def get_all_users(self):
        session = self.database.get_session()
        entries = session.query(UserDb).order_by(desc(UserDb.id)).all()
        users = []
        for user_data in entries:
            user = User(int(user_data.id), user_data.name, user_data.email, user_data.password)
            users.append(user)
        return users

    def get_user_by_id(self, user_id):
        session = self.database.get_session()
        entry = session.query(UserDb).filter_by(id=user_id).first()
        user = User(int(entry.id), entry.name, entry.email, entry.password)
        return user

    def get_user_by_name_or_email(self, name_or_email):
        session = self.database.get_session()
        command = session.query(UserDb)
        command = command.filter(or_(UserDb.email == name_or_email, UserDb.name == name_or_email))
        entry = command.first()
        user = None
        if entry is not None:
            user = User(int(entry.id),
                        entry.name,
                        entry.email,
                        entry.password)
        return user

    def verify_user_already_exist(self, user):
        user_by_name = self.get_user_by_name_or_email(user.name)
        user_by_email = self.get_user_by_name_or_email(user.email)
        return user_by_name is not None or user_by_email is not None

    def are_credentials_unavailable(self, user_to_edit, new_name, new_email):
        user_by_name = self.get_user_by_name_or_email(new_name)
        user_by_email = self.get_user_by_name_or_email(new_email)
        if user_by_name is not None and user_by_name.user_id != user_to_edit.user_id:
            return True
        if user_by_email is not None and user_by_email.user_id != user_to_edit.user_id:
            return True
        return False
