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
from services.image_manager_interface import ImageManagerInterface
from services.image_manager_database import ImageManagerDatabase
from services.image_manager_in_memory import ImageManagerInMemory

def configure_production(binder):
    binder.bind(ImageManagerInterface, to=ImageManagerDatabase, scope=singleton)
    binder.bind(UsersInterface, to=UsersDatabaseRepository, scope=singleton)
    binder.bind(BlogPostsInterface,
                to=BlogPostsDatabaseRepository(UsersDatabaseRepository(), ImageManagerDatabase()),
                scope=singleton)
    binder.bind(DatabaseConfig, to=DatabaseConfig, scope=singleton)
    binder.bind(Authentication, to=Authentication, scope=singleton)



def configure_testing(binder):
    binder.bind(ImageManagerInterface, to=ImageManagerInMemory, scope=singleton)
    binder.bind(UsersInterface, to=UsersInMemoryRepository, scope=singleton)
    binder.bind(BlogPostsInterface,
                to=BlogPostsInMemoryRepository(UsersInMemoryRepository(), ImageManagerInMemory()),
                scope=singleton)
    binder.bind(DatabaseConfig, to=Mock(DatabaseConfig), scope=request)
    binder.bind(Authentication, to=Authentication, scope=singleton)
