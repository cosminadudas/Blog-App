class DatabaseSetupModel:

    def __init__(self, section, host, user, password, database_name):
        self.section = section
        self.host = host
        self.user = user
        self.password = password
        self.database_name = database_name
