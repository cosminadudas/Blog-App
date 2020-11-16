from datetime import datetime
from exceptions import FormatFileNotAccepted
from injector import inject
from models.blog_post import BlogPost
from models.pagination import Pagination
from repository.blog_posts_interface import BlogPostsInterface
from repository.image_manager_interface import ImageManagerInterface

IMAGE = """data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNby
blAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="""

class BlogPostsInMemoryRepository(BlogPostsInterface):

    @inject
    def __init__(self, users, image_manager: ImageManagerInterface):
        self.users = users
        self.posts = self.users.posts
        self.image_manager = image_manager


    def verify_if_owner_is_user(self, owner):
        for user in self.users.get_all_users():
            if owner == user.user_id:
                return True
        return False


    def get_all_posts(self, user, pagination: Pagination):
        all_posts = []
        posts = []
        if user is not None:
            for post in self.posts:
                if post.owner == user:
                    all_posts.append(post)
        else:
            all_posts = self.posts
            posts = all_posts
        if pagination is not None:
            posts = []
            start_index = int(pagination.limit * (pagination.page_number))
            i = start_index
            while i < len(all_posts) and i < start_index + pagination.limit:
                posts.append(all_posts[i])
                i += 1
        return posts



    def get_post_by_id(self, post_id):
        for post in self.posts:
            if str(post.post_id) == str(post_id):
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
            if new_post.image is not None and new_post.image.filename != '':
                new_post.image = self.image_manager.save_image(new_post.image)
            else:
                new_post.image = 'data:image/gif;base64,R0lGODlhAQABAAAAACw='
            self.posts.insert(0, new_post)


    def edit(self, post_id, new_title, new_content, new_image):
        post_to_edit = self.get_post_by_id(post_id)
        if post_to_edit is not None:
            post_to_edit.title = new_title
            post_to_edit.content = new_content
            post_to_edit.modified_at = datetime.now()
        if new_image.filename != '':
            try:
                post_to_edit.image = self.image_manager.edit_image(new_image, post_to_edit.image)
            except FormatFileNotAccepted:
                raise FormatFileNotAccepted

    def delete(self, post_id):
        post_to_delete = self.get_post_by_id(post_id)
        self.posts.remove(post_to_delete)
