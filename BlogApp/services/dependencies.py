from flask import request
from mock import Mock
from repository.blog_posts_interface import BlogPostsInterface
from repository.blog_posts_database_repository import BlogPostsDatabaseRepository
from repository.blog_posts_in_memory_repository import BlogPostsInMemoryRepository
from setup.database_config import DatabaseConfig


def configure_production(binder):
    binder.bind(BlogPostsInterface, to=BlogPostsDatabaseRepository, scope=request)
    binder.bind(DatabaseConfig, to=DatabaseConfig, scope=request)


def configure_testing(binder):
    binder.bind(BlogPostsInterface, to=BlogPostsInMemoryRepository, scope=request)
    binder.bind(DatabaseConfig, to=Mock(DatabaseConfig), scope=request)
