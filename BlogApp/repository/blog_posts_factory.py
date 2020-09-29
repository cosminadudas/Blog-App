from repository.blog_posts_database_repository import BlogPostsDatabaseRepository
from repository.blog_posts_in_memory_repository import BlogPostsInMemoryRepository

def blog_posts_factory(type_of_action):
    if type_of_action == "production":
        return BlogPostsDatabaseRepository()
    return BlogPostsInMemoryRepository()
