from sqlalchemy import Column, Integer, String, Date, ForeignKey
from setup.database import Base


class BlogPostDb(Base):

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, auto_increment=True)
    owner = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    content = Column(String)
    created_at = Column(Date)
    modified_at = Column(Date)

    def __init__(self, owner, title, content, created_at):
        self.owner = owner
        self.title = title
        self.content = content
        self.created_at = created_at

    def __repr__(self):
        return "<BlogPostsDb(id='{}', owner='{}', title='{}', content='{}', created_at='{}')>"\
            .format(self.id, self.owner, self.title, self.content, self.created_at)
