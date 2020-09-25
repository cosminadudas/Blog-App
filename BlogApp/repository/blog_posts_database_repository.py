from datetime import datetime
import psycopg2
from models.BlogPost import BlogPost
from repository.blog_posts_interface import BlogPostsInterface

conn = psycopg2.connect(
    host="localhost",
    database="blog",
    user="postgres",
    password="postgres")
cur = conn.cursor()

class BlogPostsDatabaseRepository(BlogPostsInterface):

    def __init__(self):
        self.conn = conn
        self.cur = cur
        

    def get_all_posts(self):
        self.cur.execute("SELECT * FROM posts")
        entries = cur.fetchall()
        posts = []
        for post_data in entries:
            post = BlogPost(int(post_data[0]), post_data[1], post_data[2], post_data[3])
            posts.append(post)
        return posts

    def get_post_by_id(self, post_id):
        self.cur.execute("SELECT * FROM posts WHERE ID = %s", ((post_id,)))
        entry = cur.fetchone()
        post = BlogPost(int(entry[0]), entry[1], entry[2], entry[3])
        return post

    def count(self):
        return int(len(self.get_all_posts()))


    def add(self, new_post:BlogPost):
        new_post.created_at = datetime.now()
        self.cur.execute("""INSERT INTO posts (OWNER, TITLE, CONTENT) 
        VALUES (%s, %s, %s)""", (
            new_post.owner, new_post.title, new_post.content))
        self.conn.commit()
        

    def edit(self, post_id, new_title, new_content):
        self.cur.execute("""UPDATE posts
       SET TITLE = %s, CONTENT = %s 
       WHERE ID = %s""", (
           new_title, new_content, post_id ))
        self.conn.commit()

    def delete(self, post_id):
        self.cur.execute("DELETE FROM posts WHERE ID = %s", ((post_id,)))
        number = self.cur.execute("SELECT MAX(ID) FROM posts")
        if type(number) != int:
            self.cur.execute("ALTER SEQUENCE posts_id_seq RESTART WITH 1")
        else:
            self.cur.execute("ALTER SEQUENCE posts_id_seq RESTART WITH %s", ((number,)))
        self.conn.commit()