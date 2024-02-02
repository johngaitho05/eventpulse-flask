#!/usr/bin/python3
"""Defines the Review class."""
from sqlalchemy import Column, String, ForeignKey, Table, DateTime, Text
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel
from models.venue import Venue

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
    description = Column(Text, nullable=False)
    venue_id = Column(String(60), ForeignKey('venues.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    banner_url = Column(String(2048), nullable=False)
    attendees = relationship("User", secondary=event_attendees, viewonly=False)
    tracks = relationship("EventTrack", backref="event", cascade="all, delete, delete-orphan")

    def to_dict(self, anotate=None):
        """Attach ManyToOne records"""
        from models import storage
        res = super(Event, self).to_dict()
        if anotate and 'venue_id' in anotate:
            res.update({'venue_id': storage.get(Venue, self.venue_id).to_dict()})
        if anotate and 'tracks' in anotate:
            res.update({'tracks': [track.to_dict() for track in self.tracks]})
        return res
