#!/usr/bin/python3
"""database storage engine"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.country import Country
from models.event import Event
from models.event_track import EventTrack
from models.room import Room
from models.venue import Venue
from models.user import User
from os import getenv


classes = {
    "User": User,
    "Country": Country,
    "Event": Event,
    "EventTrack": EventTrack,
    "Room": Room,
    "Venue": Venue,
}


class DBStorage:
    """database storage engine for mysql storage"""
    __engine = None
    __session = None

    def __init__(self):
        """instantiate new dbstorage instance"""
        user = getenv('EVENTPULSE_USER')
        pwd = getenv('EVENTPULSE_PWD')
        host = getenv('EVENTPULSE_HOST')
        db = getenv('EVENTPULSE_DB')
        env = getenv('EVENTPULSE_ENV')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db
                                                 ), pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current db session all cls objects
        this method must return a dictionary: (like FileStorage)
        key = <class-name>.<object-id>
        value = object
        """
        dct = {}
        if cls is None:
            for c in classes.values():
                objs = self.__session.query(c).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dct[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                dct[key] = obj
        return dct

    def new(self, obj):
        """adds the obj to the current db session"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self):
        """commit all changes of the current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """ deletes from the current database session the obj
            if it's not None
        """
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete()

    def reload(self):
        """reloads the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """closes the working SQLAlchemy session"""
        self.__session.close()