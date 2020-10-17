from flask import request
from injector import singleton
from mock import Mock
from repository.blog_posts_interface import BlogPostsInterface
from repository.blog_posts_database_repository import BlogPostsDatabaseRepository
from repository.blog_posts_in_memory_repository import BlogPostsInMemoryRepository
from repository.users_interface import UsersInterface
from repository.users_database_repository import UsersDatabaseRepository
from repository.users_in_memory_repository import UsersInMemoryRepository
from setup.database_config import DatabaseConfig
from services.authentication import Authentication

def configure_production(binder):
    binder.bind(UsersInterface, to=UsersDatabaseRepository, scope=request)
    binder.bind(BlogPostsInterface, to=BlogPostsDatabaseRepository, scope=request)
    binder.bind(DatabaseConfig, to=DatabaseConfig, scope=request)
    binder.bind(Authentication, to=Authentication, scope=singleton)


def configure_testing(binder):
    binder.bind(UsersInterface, to=UsersInMemoryRepository, scope=request)
    binder.bind(BlogPostsInterface, to=BlogPostsInMemoryRepository, scope=request)
    binder.bind(DatabaseConfig, to=Mock(DatabaseConfig), scope=request)
    binder.bind(Authentication, to=Authentication, scope=singleton)
