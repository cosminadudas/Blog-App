from exceptions import UserAlreadyExists
from datetime import datetime
from repository.users_interface import UsersInterface
from repository.demo_users import users
from models.user import User
from services.password_manager import PasswordManager

class UsersInMemoryRepository(UsersInterface):

    def __init__(self):
        self.users = users


    def count(self):
        return len(self.users)


    def add(self, new_user: User):
        if self.verify_user_already_exist(new_user):
            raise UserAlreadyExists
        new_user.user_id = self.count() + 1
        new_user.password = PasswordManager.hash(new_user.password)
        self.users.insert(0, new_user)


    def edit(self, user_to_edit, new_name, new_email, new_password):
        if user_to_edit is not None:
            if self.are_credentials_unavailable(user_to_edit, new_name, new_email):
                raise UserAlreadyExists
            user_to_edit.name = new_name
            user_to_edit.email = new_email
            if new_password is None:
                pass
            else:
                user_to_edit.password = PasswordManager.hash(new_password)
            user_to_edit.modified_at = datetime.now()


    def delete(self, user_id):
        user_to_delete = self.get_user_by_id(user_id)
        self.users.remove(user_to_delete)


    def get_all_users(self):
        return self.users


    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None


    def get_user_by_name_or_email(self, name_or_email):
        for user in self.users:
            if name_or_email in (user.name, user.email):
                return user
        return None


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
