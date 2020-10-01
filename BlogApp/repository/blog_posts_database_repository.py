from datetime import datetime
from models.blog_post import BlogPost
from models.database import Database
from repository.blog_posts_interface import BlogPostsInterface

COMMAND = """ CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                owner TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP,
                modified_at TIMESTAMP
                )
        """

class BlogPostsDatabaseRepository(BlogPostsInterface):

    def __init__(self):
        self.database = Database()

    def get_all_posts(self):
        self.database.connect()
        self.database.create_table(COMMAND)
        cur = self.database.conn.cursor()
        cur.execute("SELECT * FROM posts ORDER BY id DESC")
        entries = cur.fetchall()
        posts = []
        for post_data in entries:
            post = BlogPost(int(post_data[0]), post_data[1], post_data[2], post_data[3])
            posts.append(post)
        self.database.close()
        return posts

    def get_post_by_id(self, post_id):
        self.database.connect()
        cur = self.database.conn.cursor()
        cur.execute("SELECT * FROM posts WHERE ID = %s", ((post_id,)))
        entry = cur.fetchone()
        post = BlogPost(int(entry[0]), entry[1], entry[2], entry[3])
        self.database.close()
        return post

    def count(self):
        return len(self.get_all_posts())


    def add(self, new_post: BlogPost):
        new_post.created_at = datetime.now()
        new_post.post_id = self.count() + 1
        self.database.connect()
        cur = self.database.conn.cursor()
        cur.execute("""INSERT INTO posts (OWNER, TITLE, CONTENT)
        VALUES (%s, %s, %s)""", (
            new_post.owner, new_post.title, new_post.content))
        self.database.close()

    def edit(self, post_id, new_title, new_content):
        self.database.connect()
        cur = self.database.conn.cursor()
        cur.execute("""UPDATE posts SET TITLE = %s, CONTENT = %s WHERE ID = %s""", (
            new_title, new_content, post_id))
        self.database.close()


    def delete(self, post_id):
        self.database.connect()
        cur = self.database.conn.cursor()
        cur.execute("DELETE FROM posts WHERE ID = %s", ((post_id,)))
        cur.execute("ALTER SEQUENCE posts_id_seq RESTART WITH %s", ((post_id,)))
        self.database.close()
