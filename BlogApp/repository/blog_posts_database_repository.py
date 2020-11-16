from datetime import datetime
from exceptions import FormatFileNotAccepted
from injector import inject
from sqlalchemy import desc, select, join
from models.blog_post import BlogPost
from models.pagination import Pagination
from repository.models.blog_post_db import BlogPostDb
from repository.models.user_db import UserDb
from repository.blog_posts_interface import BlogPostsInterface
from repository.image_manager_interface import ImageManagerInterface
from setup.database_setup import DatabaseSetup

class BlogPostsDatabaseRepository(BlogPostsInterface):

    @inject
    def __init__(self, users, image_manager: ImageManagerInterface):
        self.database = DatabaseSetup()
        self.users = users
        self.image_manager = image_manager

    def verify_if_owner_is_user(self, owner):
        for user in self.users.get_all_users():
            if owner == user.user_id:
                return True
        return False

    def get_all_posts(self, user, pagination: Pagination):
        entries = []
        command = select([BlogPostDb.id,
                          BlogPostDb.title,
                          BlogPostDb.content,
                          BlogPostDb.image,
                          UserDb.name])
        if user is not None:
            command = command.where(UserDb.name == user)
        command = command.select_from(join(UserDb,
                                           BlogPostDb,
                                           UserDb.id == BlogPostDb.owner))
        command = command.order_by(desc(BlogPostDb.id))
        if pagination is not None:
            limit_number = pagination.limit
            skipped_number = pagination.page_number * pagination.limit
            command = command.limit(limit_number).offset(skipped_number).alias('a')
        else:
            command = command.alias('a')
        session = self.database.get_session()
        entries = session.query(command).all()
        posts = []
        for post_data in entries:
            post = BlogPost(int(post_data.id),
                            post_data.name,
                            post_data.title,
                            post_data.content,
                            post_data.image)
            post.image = self.image_manager.get_image_path(str(post.image))
            posts.append(post)
        return posts

    def count(self, user):
        session = self.database.get_session()
        if user is None:
            count = session.query(BlogPostDb).count()
        elif user is not None:
            count = session.query(select(['*'])
                                  .select_from(join(UserDb,
                                                    BlogPostDb,
                                                    UserDb.id == BlogPostDb.owner))
                                  .where(UserDb.name == user)
                                  .alias('a')).count()
        return int(count)

    def get_post_by_id(self, post_id):
        session = self.database.get_session()
        entry = session.query(select([BlogPostDb.id,
                                      BlogPostDb.title,
                                      BlogPostDb.content,
                                      BlogPostDb.image,
                                      UserDb.name])
                              .select_from(join(UserDb,
                                                BlogPostDb,
                                                UserDb.id == BlogPostDb.owner))
                              .where(BlogPostDb.id == str(post_id))
                              .alias('a')).first()
        post = BlogPost(int(entry.id), entry.name, entry.title, entry.content, entry.image)
        post.image = self.image_manager.get_image_path(str(post.image))[1:]
        return post


    def add(self, new_post: BlogPost):
        if self.verify_if_owner_is_user(new_post.owner):
            new_post.created_at = datetime.now()
            session = self.database.get_session()
            post_to_add = BlogPostDb(new_post.owner,
                                     new_post.title,
                                     new_post.content,
                                     new_post.created_at,
                                     '')
            session.add(post_to_add)
            session.commit()
            command = session.query(BlogPostDb)
            post = command.filter_by(title=new_post.title).first()
            new_post.post_id = post.id
            post.image = self.image_manager.rename_image(new_post.image, new_post.post_id)
            if new_post.image is not None and post.image != '':
                try:
                    self.image_manager.save_image(new_post.image)
                    new_post.image = post.image
                except:
                    post = session.query(BlogPostDb).filter_by(id=new_post.post_id).first()
                    session.delete(post)
                    session.commit()
                    raise FormatFileNotAccepted
            else:
                post.image = 'default.png'
            session.commit()

    def edit(self, post_id, new_title, new_content, new_image):
        session = self.database.get_session()
        post = session.query(BlogPostDb).filter_by(id=post_id).first()
        post.title = new_title
        post.content = new_content
        post.modified_at = datetime.now()
        if new_image.filename != '':
            try:
                old_image = post.image
                post.image = self.image_manager.rename_image(new_image, post.id)
                self.image_manager.edit_image(new_image, old_image)
            except FormatFileNotAccepted:
                raise FormatFileNotAccepted
        session.commit()

    def delete(self, post_id):
        session = self.database.get_session()
        post = self.get_post_by_id(post_id)
        if post.image is not None:
            self.image_manager.delete_image(post.image)
        post = session.query(BlogPostDb).filter_by(id=post_id).first()
        session.delete(post)
        session.commit()
