#!/usr/bin/python3
"""Defines the Review class."""
from sqlalchemy import Column, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel

event_attendees = Table('event_attendees', Base.metadata,
                        Column('event_id', String(60),
                               ForeignKey('events.id'),
                               nullable=False),
                        Column('user_id', String(60),
                               ForeignKey('users.id'),
                               nullable=False)
                        )


class Event(BaseModel, Base):
    """
    Event ORM
    """
    __tablename__ = 'events'

    title = Column(String(1024), nullable=False)
    venue_id = Column(String(60), ForeignKey('venues.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    attendees = relationship("User", secondary=event_attendees,
                             viewonly=False)
    tracks = relationship("EventTrack", backref="event", cascade="all, delete, delete-orphan")
    banner_url = Column(String(2048))
