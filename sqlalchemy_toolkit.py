from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def init_db(database_url, **database_connect_options):
    """init the database with the url, and binding the Base"""
    engine = create_engine(database_url,
                           convert_unicode=True,
                           **database_connect_options)

    Base.metadata.reflect(engine)
    Base.metadata.create_all(engine)
    session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine))
    Base.query = session.query_property()

    return session
