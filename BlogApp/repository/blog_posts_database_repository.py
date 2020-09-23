import psycopg2
from models.BlogPost import BlogPost


class Posts:

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="blog",
            user="postgres",
            password="postgres")
        self.cur = conn.cursor()
        self.cur.execute("""
        CREATE TABLE posts
            (
                ID INT NOT NULL,
                OWNER TEXT NOT NULL,
                TITLE TEXT NOT NULL,
                CONTENT TEXT NOT NULL
            )
        """
        )

    def add_post(self, new_post:BlogPost):
        self.cur.execute("INSERT INTO posts (ID, OWNER, TITLE, CONTENT) VALUES(new_post.id, new_post.owner, new_post.title, new_post.content)")
        self.conn.commit()
        self.conn.close()


    def edit(self, post_id, new_title, new_content):
        self.cur.execute("UPDATE posts SET TITLE = new_title AND CONTENT = new_content WHERE ID = post_id")
        self.conn.commit()
        self.conn.close()

    def delete(self, post_id):
        self.cur.execute("DELETE FROM posts WHERE ID = post_id")