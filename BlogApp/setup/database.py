from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.database_credentials import DatabaseCredentials


Base = declarative_base()

def get_engine(db_credentials: DatabaseCredentials):
    database_uri = 'postgresql+psycopg2://{}:{}@localhost/{}'
    engine = create_engine(database_uri.format(db_credentials.user,
                                               db_credentials.password,
                                               db_credentials.database_name),
                           convert_unicode=True)
    return engine

def get_session(db_credentials: DatabaseCredentials):
    session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=get_engine(db_credentials)))
    return session

def init_db(db_session, db_credentials: DatabaseCredentials):
    engine = get_engine(db_credentials)
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
