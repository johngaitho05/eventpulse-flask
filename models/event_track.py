#!/usr/bin/python3
"""
Defines the City class.
"""
from sqlalchemy import Column, String, ForeignKey, DateTime, Float

from models.base_model import Base, BaseModel
from models.event import Event


class EventTrack(BaseModel, Base):
    """
     Event Track ORM
    """
    __tablename__ = "event_tracks"

    title = Column(String(1024), nullable=False)
    event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
    responsible = Column(String(60), ForeignKey('users.id'), nullable=True)
    room = Column(String(128), nullable=True)
    start_date = Column(DateTime, nullable=False)
    duration = Column(Float, nullable=True)

    def to_dict(self, anotate=None):
        """Attach ManyToOne records"""
        from models import storage
        res = super(EventTrack, self).to_dict()
        if anotate and 'country_id' in anotate:
            res.update({'country_id': storage.get(Event, self.event_id).to_dict()})
        return res
