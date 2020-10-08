class DatabaseCredentials:

    def __init__(self, user, password, database_name):
        self.host = 'localhost'
        self.user = user
        self.password = password
        self.database_name = database_name
