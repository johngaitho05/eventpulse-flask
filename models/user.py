#!/usr/bin/python3
"""Defines the User class."""
from sqlalchemy import Column, String, ForeignKey

from models.base_model import Base, BaseModel


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

    m2x = {'country_id': 'Country'}
