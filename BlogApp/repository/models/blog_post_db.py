from sqlalchemy import Column, Integer, String, Date, ForeignKey
from setup.database import Base


class BlogPostDb(Base):

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    content = Column(String)
    created_at = Column(Date)
    modified_at = Column(Date)
    image = Column(String)

    def __init__(self, owner, title, content, created_at, image):
        self.owner = owner
        self.title = title
        self.content = content
        self.created_at = created_at
        self.image = image

    def __repr__(self):
        post = "<BlogPostsDb(id='{}', owner='{}', title='{}',"\
            +"content='{}', created_at='{}', image='{}')>"
        return post\
            .format(self.id, self.owner, self.title, self.content, self.created_at, self.image)
