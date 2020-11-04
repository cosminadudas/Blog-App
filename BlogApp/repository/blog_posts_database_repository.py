from datetime import datetime
from sqlalchemy import desc, select, join
from models.blog_post import BlogPost
from models.pagination import Pagination
from repository.models.blog_post_db import BlogPostDb
from repository.models.user_db import UserDb
from repository.blog_posts_interface import BlogPostsInterface
from setup.database_setup import DatabaseSetup

class BlogPostsDatabaseRepository(BlogPostsInterface):

    def __init__(self):
        self.database = DatabaseSetup()

    def get_all_posts(self, user, pagination: Pagination):
        limit_number = pagination.limit
        skipped_number = pagination.page_number * pagination.limit
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
        command = command.limit(limit_number).offset(skipped_number).alias('a')
        session = self.database.get_session()
        entries = session.query(command).all()
        posts = []
        for post_data in entries:
            post = BlogPost(int(post_data.id),
                            post_data.name,
                            post_data.title,
                            post_data.content,
                            post_data.image)
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
        return post


    def add(self, new_post: BlogPost):
        new_post.created_at = datetime.now()
        session = self.database.get_session()
        post_to_add = BlogPostDb(new_post.owner,
                                 new_post.title,
                                 new_post.content,
                                 new_post.created_at,
                                 new_post.image)
        session.add(post_to_add)
        session.commit()
        command = session.query(BlogPostDb)
        new_post.post_id = command.filter_by(title=new_post.title).first().id



    def edit(self, post_id, new_title, new_content, new_image):
        session = self.database.get_session()
        post = session.query(BlogPostDb).filter_by(id=post_id).first()
        post.title = new_title
        post.content = new_content
        post.modified_at = datetime.now()
        if new_image != '':
            post.image = new_image
        session.commit()

    def delete(self, post_id):
        session = self.database.get_session()
        session.query(BlogPostDb).filter_by(id=post_id).delete()
        session.commit()
