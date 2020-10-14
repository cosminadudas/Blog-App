USERS_TABLE = """CREATE TABLE IF NOT EXISTS users(
id SERIAL PRIMARY KEY UNIQUE NOT NULL,
name TEXT UNIQUE NOT NULL,
email TEXT NOT NULL,
password TEXT NOT NULL,
created_at TIMESTAMP,
modified_at TIMESTAMP)"""

ADMIN_USER = """INSERT INTO users (name,email,password,created_at,modified_at)
VALUES 
('admin',
'admin@yahoo.com',
'8C6976E5B5410415BDE908BD4DEE15DFB167A9C873FC4BB8A81F6F2AB448A918',
current_timestamp,
current_timestamp)"""

queries = [USERS_TABLE, ADMIN_USER]

POSTS_OWNERS_NOT_REGISTER = '''SELECT DISTINCT owner FROM posts
WHERE CAST(posts.owner AS TEXT) NOT IN (SELECT CAST(id AS TEXT) FROM users)'''

queries.append(POSTS_OWNERS_NOT_REGISTER)

OWNERS = '''UPDATE posts
SET owner=users.id FROM users 
WHERE CAST(posts.owner AS TEXT)=users.name OR CAST(posts.owner AS TEXT)=CAST(users.id AS TEXT)'''

queries.append(OWNERS)

OWNERS_INTS = 'ALTER TABLE posts ALTER COLUMN owner TYPE INTEGER USING owner::integer'

FOREIGN_KEY = '''ALTER TABLE posts
ADD FOREIGN KEY (owner) REFERENCES users (id)'''

queries.append(OWNERS_INTS)
queries.append(FOREIGN_KEY)
