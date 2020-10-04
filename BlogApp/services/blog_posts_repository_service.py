from injector import inject
from repository.blog_posts_interface import BlogPostsInterface
from models.blog_post import BlogPost

class BlogPostsRepositoryService:
    @inject
    def __init__(self, blog_posts: BlogPostsInterface):
        self.blog_posts = blog_posts


    def add(self, new_post: BlogPost):
        return self.blog_posts.add(new_post)


    def edit(self, post_id, new_title, new_content):
        return self.blog_posts.edit(post_id, new_title, new_content)


    def delete(self, post_id):
        return self.blog_posts.delete(post_id)


    def get_post_by_id(self, post_id):
        return self.blog_posts.get_post_by_id(post_id)

    def get_all_posts(self):
        return self.blog_posts.get_all_posts()
