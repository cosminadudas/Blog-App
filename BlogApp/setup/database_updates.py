POSTS_TABLE = """ CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY UNIQUE NOT NULL,
                owner TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP,
                modified_at TIMESTAMP
                )
        """

USERS_TABLE = """CREATE TABLE IF NOT EXISTS users(
id SERIAL PRIMARY KEY UNIQUE NOT NULL,
name TEXT UNIQUE NOT NULL,
email TEXT,
password TEXT,
created_at TIMESTAMP,
modified_at TIMESTAMP)"""


ADMIN_USER = """INSERT INTO users (name,email,created_at,modified_at)
VALUES 
('admin',
'user@yahoo.com',
current_timestamp,
current_timestamp)"""

queries = [POSTS_TABLE, USERS_TABLE, ADMIN_USER]

POSTS_OWNERS_NOT_REGISTER = '''INSERT INTO users (name)
SELECT DISTINCT owner FROM posts WHERE 
CAST(posts.owner AS TEXT) NOT IN (SELECT CAST(id AS TEXT) FROM users) '''

queries.append(POSTS_OWNERS_NOT_REGISTER)


USERS_UPDATE = '''UPDATE users SET
email='user@yahoo.com', password='',
created_at=now()::timestamp(0), modified_at=now()::timestamp(0)
WHERE password is null'''

queries.append(USERS_UPDATE)


OWNERS = '''UPDATE posts
SET owner=users.id FROM users 
WHERE CAST(posts.owner AS TEXT)=users.name OR CAST(posts.owner AS TEXT)=CAST(users.id AS TEXT)'''

queries.append(OWNERS)

OWNERS_INTS = 'ALTER TABLE posts ALTER COLUMN owner TYPE INTEGER USING owner::integer'

FOREIGN_KEY = '''ALTER TABLE posts
ADD FOREIGN KEY (owner) REFERENCES users (id)'''

queries.append(OWNERS_INTS)
queries.append(FOREIGN_KEY)
