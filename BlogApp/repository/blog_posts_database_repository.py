from datetime import datetime
from models.blog_post import BlogPost
from repository.blog_posts_interface import BlogPostsInterface
from setup.database_setup import DatabaseSetup

class BlogPostsDatabaseRepository(BlogPostsInterface):

    def __init__(self):
        self.database = DatabaseSetup()

    def get_all_posts(self):
        self.database.connect()
        cur = self.database.conn.cursor()
        cur.execute("""SELECT posts.id, posts.title, posts.content,
        users.name
        FROM posts INNER JOIN users ON posts.owner=users.id ORDER BY posts.id DESC""")
        entries = cur.fetchall()
        posts = []
        for post_data in entries:
            post = BlogPost(int(post_data[0]), post_data[3], post_data[1], post_data[2])
            posts.append(post)
        self.database.close()
        return posts

    def get_post_by_id(self, post_id):
        self.database.connect()
        cur = self.database.conn.cursor()
        cur.execute("""SELECT posts.id, posts.title, posts.content,
        users.name
        FROM posts INNER JOIN users ON posts.owner=users.id WHERE posts.id = %s""", ((post_id,)))
        entry = cur.fetchone()
        post = BlogPost(int(entry[0]), entry[3], entry[1], entry[2])
        self.database.close()
        return post

    def count(self):
        return len(self.get_all_posts())


    def add(self, new_post: BlogPost):
        self.database.connect()
        cur = self.database.conn.cursor()
        cur.execute("""INSERT INTO posts (OWNER, TITLE, CONTENT)
        VALUES (%s, %s, %s)""", (
            new_post.owner, new_post.title, new_post.content))
        new_post.created_at = datetime.now()
        cur.execute("SELECT ID FROM posts WHERE content=%s", (new_post.content,))
        new_post.post_id = int(cur.fetchone()[0])
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
        self.database.close()
