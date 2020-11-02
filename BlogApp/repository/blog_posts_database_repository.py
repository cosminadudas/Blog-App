from datetime import datetime
from sqlalchemy import desc, select, join
from models.blog_post import BlogPost
from models.pagination import Pagination
from models.blog_post_db import BlogPostDb
from models.user_db import UserDb
from repository.blog_posts_interface import BlogPostsInterface
from setup.database_setup import DatabaseSetup

class BlogPostsDatabaseRepository(BlogPostsInterface):

    def __init__(self):
        self.database = DatabaseSetup()

    def get_all_posts(self, user, pagination: Pagination):
        limit_number = pagination.limit
        skipped_number = pagination.page_number * pagination.limit
        entries = []
        if user is None:
            entries = self.database.session.query(select([BlogPostDb.id,
                                                          BlogPostDb.title,
                                                          BlogPostDb.content,
                                                          UserDb.name])
                                                  .select_from(join(UserDb,
                                                                    BlogPostDb,
                                                                    UserDb.id == BlogPostDb.owner))
                                                  .order_by(desc(BlogPostDb.id)).limit(limit_number)
                                                  .offset(skipped_number).alias('a')).all()
        else:
            entries = self.database.session.query(select([BlogPostDb.id,
                                                          BlogPostDb.title,
                                                          BlogPostDb.content,
                                                          UserDb.name])
                                                  .where(UserDb.name == user)
                                                  .select_from(join(UserDb,
                                                                    BlogPostDb,
                                                                    UserDb.id == BlogPostDb.owner))
                                                  .order_by(desc(BlogPostDb.id)).limit(limit_number)
                                                  .offset(skipped_number).alias('a')).all()
        posts = []
        for post_data in entries:
            post = BlogPost(int(post_data.id), post_data.name, post_data.title, post_data.content)
            posts.append(post)
        return posts

    def count(self, user):
        if user is None:
            count = self.database.session.query(BlogPostDb).count()
        elif user is not None:
            count = self.database.session.query(select(['*'])
                                                .select_from(join(UserDb,
                                                                  BlogPostDb,
                                                                  UserDb.id == BlogPostDb.owner))
                                                .where(UserDb.name == user)
                                                .alias('a')).count()
        return int(count)

    def get_post_by_id(self, post_id):
        entry = self.database.session.query(select([BlogPostDb.id,
                                                    BlogPostDb.title,
                                                    BlogPostDb.content,
                                                    UserDb.name])
                                            .select_from(join(UserDb,
                                                              BlogPostDb,
                                                              UserDb.id == BlogPostDb.owner))
                                            .where(BlogPostDb.id == str(post_id))
                                            .alias('a')).first()
        post = BlogPost(int(entry.id), entry.name, entry.title, entry.content)
        return post


    def add(self, new_post: BlogPost):
        new_post.created_at = datetime.now()
        post_to_add = BlogPostDb(new_post.owner,
                                 new_post.title,
                                 new_post.content,
                                 new_post.created_at)
        self.database.session.add(post_to_add)
        self.database.session.commit()
        new_post.post_id = self.database.session.query(BlogPostDb).filter_by(title=new_post.title).first().id



    def edit(self, post_id, new_title, new_content):
        post = self.database.session.query(BlogPostDb).filter_by(id=post_id).first()
        post.title = new_title
        post.content = new_content
        post.modified_at = datetime.datetime.now()
        self.database.session.commit()

    def delete(self, post_id):
        self.database.session.query(BlogPostDb).filter_by(id=post_id).delete()
        self.database.session.commit()
