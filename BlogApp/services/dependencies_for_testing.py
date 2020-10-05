from flask import request
from mock import Mock
from repository.blog_posts_interface import BlogPostsInterface
from repository.blog_posts_in_memory_repository import BlogPostsInMemoryRepository
from services.blog_posts_repository_service import BlogPostsRepositoryService
from services.config_database_service import ConfigDatabaseService
from setup.config import Config
from setup.database_config import DatabaseConfig

def checking_repository_configure(binder):
    binder.bind(BlogPostsRepositoryService, to=BlogPostsRepositoryService, scope=request)
    binder.bind(BlogPostsInterface, to=BlogPostsInMemoryRepository, scope=request)

def checking_database_configure(binder):
    binder.bind(ConfigDatabaseService, to=ConfigDatabaseService, scope=request)
    binder.bind(Config, to=Mock(DatabaseConfig), scope=request)
