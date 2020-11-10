from datetime import datetime
import base64
from injector import inject
from models.blog_post import BlogPost
from models.pagination import Pagination
from repository.blog_posts_interface import BlogPostsInterface

class BlogPostsInMemoryRepository(BlogPostsInterface):

    @inject
    def __init__(self, users):
        self.users = users
        self.posts = self.users.posts


    def verify_if_owner_is_user(self, owner):
        for user in self.users.get_all_users():
            if owner == user.user_id:
                return True
        return False


    def get_all_posts(self, user, pagination: Pagination):
        all_posts = []
        if user is not None:
            for post in self.posts:
                if post.owner == user:
                    all_posts.append(post)
        else:
            all_posts = self.posts

        posts = []
        start_index = int(pagination.limit * (pagination.page_number))
        i = start_index
        while i < len(all_posts) and i < start_index + pagination.limit:
            posts.append(all_posts[i])
            i += 1
        return posts



    def get_post_by_id(self, post_id):
        for post in self.posts:
            if post.post_id == post_id:
                return post
        return None


    def count(self, user):
        if user is None:
            return len(self.posts)
        count = 0
        for post in self.posts:
            if post.owner == user:
                count += 1
        return count


    def add(self, new_post: BlogPost):
        if self.verify_if_owner_is_user(new_post.owner):
            new_post.post_id = len(self.posts) + 1
            image = new_post.image.read()
            image = base64.b64encode(image).decode('ascii')
            new_post.image = 'data:image/png;base64, ' + image
            self.posts.insert(0, new_post)


    def edit(self, post_id, new_title, new_content, new_image):
        post_to_edit = self.get_post_by_id(post_id)
        if post_to_edit is not None:
            post_to_edit.title = new_title
            post_to_edit.content = new_content
            post_to_edit.modified_at = datetime.now()
            image = new_image.read()
            image = base64.b64encode(image).decode('ascii')
            post_to_edit.image = 'data:image/png;base64, ' + image


    def delete(self, post_id):
        post_to_delete = self.get_post_by_id(post_id)
        self.posts.remove(post_to_delete)
