import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="blog",
    user="postgres",
    password="postgres")

cur = conn.cursor()
cur.execute("""
CREATE TABLE posts
(
ID INT NOT NULL,
OWNER TEXT NOT NULL,
TITLE TEXT NOT NULL,
CONTENT TEXT NOT NULL
)
"""
)

conn.commit()
conn.close()