from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class UsersDb(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    email = Column(String(150), unique=True)
    password = Column(String(20))
    created_at = Column(Date)
    modified_at = Column(Date)


    def __repr__(self):
        return "<UsersDb(name='{}', email='{}', password='{}', created_at='{}')>"\
            .format(self.name, self.email, self.password, self.created_at)
