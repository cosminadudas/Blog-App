from flask import request
from repository.blog_posts_interface import BlogPostsInterface
from repository.blog_posts_in_memory_repository import BlogPostsInMemoryRepository
from services.blog_posts_repository_service import BlogPostsRepositoryService

def testing_configure(binder):
    binder.bind(BlogPostsRepositoryService, to=BlogPostsRepositoryService, scope=request)
    binder.bind(BlogPostsInterface, to=BlogPostsInMemoryRepository, scope=request)
