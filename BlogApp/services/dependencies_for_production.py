from flask import request
from repository.blog_posts_interface import BlogPostsInterface
from repository.blog_posts_database_repository import BlogPostsDatabaseRepository
from services.blog_posts_repository_service import BlogPostsRepositoryService
from services.config_database_service import ConfigDatabaseService
from setup.config import Config
from setup.database_config import DatabaseConfig


def production_repository_configure(binder):
    binder.bind(BlogPostsRepositoryService, to=BlogPostsRepositoryService, scope=request)
    binder.bind(BlogPostsInterface, to=BlogPostsDatabaseRepository, scope=request)

def production_database_configure(binder):
    binder.bind(ConfigDatabaseService, to=ConfigDatabaseService, scope=request)
    binder.bind(Config, to=DatabaseConfig, scope=request)
