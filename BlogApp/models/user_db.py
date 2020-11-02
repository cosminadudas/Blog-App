from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from setup.database import Base

class UserDb(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    email = Column(String(150), unique=True)
    password = Column(String(20))
    created_at = Column(Date)
    modified_at = Column(Date)
    posts = relationship("BlogPostDb", backref="users", cascade="all, delete")

    def __init__(self, name, email, password, created_at):
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at

    def __repr__(self):
        return "<UsersDb(id='{}', name='{}', email='{}', password='{}', created_at='{}')>"\
            .format(self.id, self.name, self.email, self.password, self.created_at)
