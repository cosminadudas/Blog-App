from datetime import datetime
from repository.users_interface import UsersInterface
from models.user import User
from setup.database_setup import DatabaseSetup
from services.password_manager import PasswordManager

class UsersDatabaseRepository(UsersInterface):

    def __init__(self):
        self.database = DatabaseSetup()


    def add(self, new_user: User):
        self.database.connect()
        cur = self.database.conn.cursor()
        hashed_password = PasswordManager.hash(new_user.password)
        cur.execute("""INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)""", (
            new_user.name, new_user.email, hashed_password))
        new_user.created_at = datetime.now()
        cur.execute("SELECT id FROM users WHERE name=%s", (new_user.name,))
        new_user.user_id = int(cur.fetchone()[0])
        self.database.close()


    def edit(self, user_to_edit, new_name, new_email, new_password):
        hashed_new_password = PasswordManager.hash(new_password)
        self.database.connect()
        cur = self.database.conn.cursor()
        cur.execute("""UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s""", (
            new_name, new_email, hashed_new_password, user_to_edit.user_id))
        self.database.close()

    def delete(self, user_id):
        self.database.connect()
        cur = self.database.conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", ((user_id,)))
        self.database.close()

    def get_all_users(self):
        self.database.connect()
        cur = self.database.conn.cursor()
        cur.execute("SELECT * FROM users ORDER BY id DESC")
        entries = cur.fetchall()
        users = []
        for user_data in entries:
            user = User(int(user_data[0]), user_data[1], user_data[2], user_data[3])
            users.append(user)
        self.database.close()
        return users

    def get_user_by_id(self, user_id):
        self.database.connect()
        cur = self.database.conn.cursor()
        cur.execute("SELECT * FROM users WHERE ID = %s", ((user_id,)))
        entry = cur.fetchone()
        user = User(int(entry[0]), entry[1], entry[2], entry[3])
        self.database.close()
        return user

    def get_user_by_name_or_email(self, name_or_email):
        self.database.connect()
        cur = self.database.conn.cursor()
        cur.execute("SELECT * FROM users WHERE NAME = %s OR EMAIL = %s",
                    ((name_or_email, name_or_email)))
        entry = cur.fetchone()
        user = None
        if entry is not None:
            user = User(int(entry[0]), entry[1], entry[2], entry[3])
        self.database.close()
        return user
