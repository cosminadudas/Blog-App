from repository.blog_posts_database_repository import DatabasePosts
from repository.blog_posts_in_memory_repository import InMemoryPosts

def factory(type):
    if type == "production":
        return DatabasePosts()
    if type == "testing":
        return InMemoryPosts()

