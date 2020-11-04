from injector import inject
from repository.blog_posts_interface import BlogPostsInterface
from repository.users_interface import UsersInterface

class BlogPostsUsersRelation:

    @inject
    def __init__(self, posts: BlogPostsInterface, users: UsersInterface):
        self.posts = posts
        self.users = users


    def verify_if_owner_is_user(self, owner):
        for user in self.users.get_all_users():
            if owner == user.user_id:
                return True
        return False
