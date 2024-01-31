#!/usr/bin/python3
"""
Defines the Amenity class.
"""

from sqlalchemy import Column, String, ForeignKey

from models.base_model import Base, BaseModel


class Room(BaseModel, Base):
    """
    Room ORM
    """
    __tablename__ = 'rooms'

    name = Column(String(128), nullable=False)
    venue_id = Column(String(60), ForeignKey('venues.id'), nullable=False)
