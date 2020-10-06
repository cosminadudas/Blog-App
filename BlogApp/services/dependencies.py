from flask import request
from mock import Mock
from repository.blog_posts_interface import BlogPostsInterface
from repository.blog_posts_database_repository import BlogPostsDatabaseRepository
from repository.blog_posts_in_memory_repository import BlogPostsInMemoryRepository
from setup.config_interface import ConfigInterface
from setup.database_config import DatabaseConfig


def configure_production_repository(binder):
    binder.bind(BlogPostsInterface, to=BlogPostsDatabaseRepository, scope=request)

def configure_production_database(binder):
    binder.bind(ConfigInterface, to=DatabaseConfig, scope=request)


def configure_testing_repository(binder):
    binder.bind(BlogPostsInterface, to=BlogPostsInMemoryRepository, scope=request)

def configure_testing_database(binder):
    binder.bind(ConfigInterface, to=Mock(DatabaseConfig), scope=request)
