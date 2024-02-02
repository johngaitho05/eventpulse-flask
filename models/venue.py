#!/usr/bin/python3
"""Defines the Place class."""
from sqlalchemy import Column, String, ForeignKey, Text

from models.base_model import Base, BaseModel
from models.country import Country


class Venue(BaseModel, Base):
    """
    Venue ORM
    """
    __tablename__ = 'venues'

    name = Column(String(1028), nullable=False)
    address = Column(String(1028), nullable=False)
    country_id = Column(String(60), ForeignKey('countries.id'), nullable=False)

    def to_dict(self, anotate=None):
        """Attach ManyToOne records"""
        from models import storage
        res = super(Venue, self).to_dict()
        if anotate and 'country_id' in anotate:
            res.update({'country_id': storage.get(Country, self.country_id).to_dict()})
        return res
