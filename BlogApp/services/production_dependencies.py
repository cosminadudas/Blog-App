from flask import request
from repository.blog_posts_interface import BlogPostsInterface
from repository.blog_posts_database_repository import BlogPostsDatabaseRepository
from services.blog_posts_repository_service import BlogPostsRepositoryService

def production_configure(binder):
    binder.bind(BlogPostsRepositoryService, to=BlogPostsRepositoryService, scope=request)
    binder.bind(BlogPostsInterface, to=BlogPostsDatabaseRepository, scope=request)
