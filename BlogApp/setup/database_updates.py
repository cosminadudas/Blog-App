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
current_timestamp) ON CONFLICT DO NOTHING"""

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

DROP_ALL_FOREIGN_KEYS = '''
create or replace function remove_fk_by_table_and_column(p_table_name 
varchar, p_column_name varchar) returns INTEGER as $$
declare
     v_fk_name varchar := NULL;
     v_fk_num_removed INTEGER := 0;
begin
     FOR v_fk_name IN (SELECT ss2.conname
         FROM pg_attribute af, pg_attribute a,
             (SELECT conname, conrelid,confrelid,conkey[i] AS conkey, 
confkey[i] AS confkey
                 FROM (SELECT conname, conrelid,confrelid,conkey,confkey,
                     generate_series(1,array_upper(conkey,1)) AS i
                     FROM pg_constraint WHERE contype = 'f') ss) ss2
         WHERE af.attnum = confkey
             AND af.attrelid = confrelid
             AND a.attnum = conkey
             AND a.attrelid = conrelid
             AND a.attrelid = p_table_name::regclass
             AND a.attname = p_column_name) LOOP
         execute 'alter table ' || quote_ident(p_table_name) || ' drop 
constraint ' || quote_ident(v_fk_name);
         v_fk_num_removed = v_fk_num_removed + 1;
     END LOOP;
     return v_fk_num_removed;
end;
$$ language plpgsql;
'''

queries.append(DROP_ALL_FOREIGN_KEYS)

DROP_ALL_FOREIGN_KEYS_ON_POST_OWNER = '''
select remove_fk_by_table_and_column('posts', 'owner')
'''

queries.append(DROP_ALL_FOREIGN_KEYS_ON_POST_OWNER)

ADD_FOREIGN_KEY = '''ALTER TABLE posts
ADD FOREIGN KEY (owner) REFERENCES users (id)
ON DELETE CASCADE
'''

queries.append(ADD_FOREIGN_KEY)
