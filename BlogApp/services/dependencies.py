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

def configure_testing_isconfigured(binder):
    config = Mock(DatabaseConfig)
    config.is_configured = True
    binder.bind(ConfigInterface, to=config, scope=request)

def configure_testing_notconfigured(binder):
    config = Mock(DatabaseConfig)
    config.is_configured = False
    binder.bind(ConfigInterface, to=config, scope=request)
