from datetime import datetime

class User:

    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.created_at = self.modified_at = datetime.now()
