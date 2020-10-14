from datetime import datetime
from setup.database_setup import DatabaseSetup
from setup.database_updates_for_version_2 import queries, POSTS_OWNERS_NOT_REGISTER

class DatabaseUpdate:

    def __init__(self, database_setup: DatabaseSetup):
        self.database_setup = database_setup
        self.latest_version = 2


    def update_database(self):
        if self.database_setup.version < self.latest_version:
            self.database_setup.connect()
            cur = self.database_setup.conn.cursor()
            for query in queries:
                if query == POSTS_OWNERS_NOT_REGISTER:
                    cur.execute(query)
                    entries = cur.fetchall()
                    for entry in entries:
                        cur.execute("""INSERT INTO users
                        (name, email, password, created_at, modified_at)
                        VALUES (%s, 'user@yahoo.com', 'user', %s, %s)""",
                                    (entry, datetime.now(), datetime.now()))
                else:
                    cur.execute(query)
                self.database_setup.conn.commit()
            self.database_setup.update()
            self.database_setup.close()
