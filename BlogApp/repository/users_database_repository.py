from datetime import datetime
from sqlalchemy import desc
from exceptions import UserAlreadyExists
from repository.users_interface import UsersInterface
from models.user import User
from models.user_db import UserDb
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
        self.database.session.add(user_to_add)
        self.database.session.commit()
        new_user.user_id = self.database.session.query(UserDb).filter_by(name=new_user.name).first().id

    def edit(self, user_to_edit: User, new_name, new_email, new_password):
        if self.are_credentials_unavailable(user_to_edit, new_name, new_email):
            raise UserAlreadyExists
        user = self.database.session.query(UserDb).filter_by(id=user_to_edit.user_id).first()
        hashed_new_password = PasswordManager.hash(new_password)
        if new_password == "":
            user.name = new_name
            user.email = new_email
        else:
            user.name = new_name
            user.email = new_email
            user.password = hashed_new_password
        user.modified_at = datetime.now()
        self.database.session.commit()

    def delete(self, user_id):
        self.database.session.query(UserDb).filter_by(id=user_id).delete()
        self.database.session.commit()

    def get_all_users(self):
        entries = self.database.session.query(UserDb).order_by(desc(UserDb.id)).all()
        users = []
        for user_data in entries:
            user = User(int(user_data.id), user_data.name, user_data.email, user_data.password)
            users.append(user)
        return users

    def get_user_by_id(self, user_id):
        entry = self.database.session.query(UserDb).filter_by(id=user_id).first()
        user = User(int(entry.id), entry.name, entry.email, entry.password)
        return user

    def get_user_by_name_or_email(self, name_or_email):
        entry_by_name = self.database.session.query(UserDb).filter_by(name=name_or_email).first()
        entry_by_email = self.database.session.query(UserDb).filter_by(email=name_or_email).first()
        user = None
        if entry_by_name is not None:
            user = User(int(entry_by_name.id),
                        entry_by_name.name,
                        entry_by_name.email,
                        entry_by_name.password)
        if entry_by_email is not None:
            user = User(int(entry_by_email.id),
                        entry_by_email.name,
                        entry_by_email.email,
                        entry_by_email.password)
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
