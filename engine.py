from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class Engine(object):

    def __init__(self, resource):
        self.session = None
        Base = declarative_base()
        engine = create_engine(resource)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        self.set_session(session)


    def set_session(self, session):
        self.session = session


    def get_session(self):
        return self.session