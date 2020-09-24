import psycopg2
from models.BlogPost import BlogPost
from repository.formal_posts_interface import FormalPostsInterface

conn = psycopg2.connect(
            host="localhost",
            database="blog",
            user="postgres",
            password="postgres")
cur = conn.cursor()

class DatabasePosts(FormalPostsInterface):

    def __init__(self):
        self.conn = conn
        self.cur = cur
        

    def get_all_posts(self):
        self.cur.execute("SELECT * FROM posts")
        self.conn.commit()


    def get_post_by_id(self, post_id):
        self.cur.execute("SELECT * FROM posts WHERE ID = %s", ((post_id,)))
        self.conn.commit()

    def count(self):
        self.cur.execute("SELECT COUNT(*) FROM posts")
        self.conn.commit()


    def add(self, new_post:BlogPost):
        self.cur.execute("""INSERT INTO posts (OWNER, TITLE, CONTENT) 
        VALUES (%s, %s, %s)""", (
            new_post.owner, new_post.title, new_post.content))
        self.conn.commit()
        


    def edit(self, post_id, new_title, new_content):
        self.cur.execute("UPDATE posts SET TITLE = new_title AND CONTENT = new_content WHERE ID = post_id")
        self.conn.commit()
        self.conn.close()

    def delete(self, post_id):
        self.cur.execute("DELETE FROM posts WHERE ID = post_id")