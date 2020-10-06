from flask import request
from mock import Mock
from repository.blog_posts_interface import BlogPostsInterface
from repository.blog_posts_database_repository import BlogPostsDatabaseRepository
from repository.blog_posts_in_memory_repository import BlogPostsInMemoryRepository
from setup.config_interface import ConfigInterface
from setup.database_config import DatabaseConfig


def production_repository_configure(binder):
    binder.bind(BlogPostsInterface, to=BlogPostsDatabaseRepository, scope=request)

def production_database_configure(binder):
    binder.bind(ConfigInterface, to=DatabaseConfig, scope=request)


def checking_repository_configure(binder):
    binder.bind(BlogPostsInterface, to=BlogPostsInMemoryRepository, scope=request)

def checking_database_configure(binder):
    binder.bind(ConfigInterface, to=Mock(DatabaseConfig), scope=request)
