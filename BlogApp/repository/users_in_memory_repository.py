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
        new_user.user_id = self.count() + 1
        new_user.password = PasswordManager.convert_to_hashed_password(new_user.password)
        self.users.insert(0, new_user)


    def edit(self, user_id, new_name, new_email, new_password):
        user_to_edit = self.get_user_by_id(user_id)
        if user_to_edit is not None:
            user_to_edit.name = new_name
            user_to_edit.email = new_email
            user_to_edit.password = PasswordManager.convert_to_hashed_password(new_password)
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
        pass
