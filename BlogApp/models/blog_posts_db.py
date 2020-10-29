from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class BlogPostsDb(Base):

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    owner = Column(String)
    title = Column(String)
    content = Column(String)
    created_at = Column(Date)
    modified_at = Column(Date)


    def __repr__(self):
        return "<BlogPostsDb(owner='{}', title='{}', content='{}', created_at='{}')>"\
            .format(self.owner, self.title, self.content, self.created_at)