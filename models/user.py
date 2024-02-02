#!/usr/bin/python3
"""Defines the User class."""
from sqlalchemy import Column, String, ForeignKey

from models.base_model import Base, BaseModel
from models.country import Country


class User(BaseModel, Base):
    """
    User ORM
    """

    __tablename__ = 'users'
    email = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    name = Column(String(256), nullable=False)
    phone = Column(String(128), nullable=True)
    country_id = Column(String(60), ForeignKey('countries.id'), nullable=False)

    def to_dict(self, anotate=None):
        """Attach ManyToOne records"""
        from models import storage
        res = super(User, self).to_dict()
        if anotate and 'country_id' in anotate:
            res.update({'country_id': storage.get(Country, self.country_id).to_dict()})
        return res
