from datetime import datetime
from models.blog_post import BlogPost
from repository.demo_posts import posts
from repository.blog_posts_interface import BlogPostsInterface

class BlogPostsInMemoryRepository(BlogPostsInterface):

    def __init__(self):
        self.posts = posts
        self.index = 0


    def get_all_posts(self):
        return self.posts


    def get_post_by_id(self, post_id):
        for post in self.posts:
            if post.post_id == post_id:
                return post
        return None


    def count(self):
        return len(self.posts)


    def add(self, new_post: BlogPost):
        new_post.post_id = self.count() + 1
        self.posts.insert(0, new_post)


    def edit(self, post_id, new_title, new_content):
        post_to_edit = self.get_post_by_id(post_id)
        if post_to_edit is not None:
            post_to_edit.title = new_title
            post_to_edit.content = new_content
            post_to_edit.modified_at = datetime.now()


    def delete(self, post_id):
        post_to_delete = self.get_post_by_id(post_id)
        self.posts.remove(post_to_delete)
