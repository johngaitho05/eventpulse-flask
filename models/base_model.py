#!/usr/bin/python3
"""
Contains class BaseModel
"""
import hashlib
import uuid
from datetime import datetime, date

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

import models

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def _refined_kwargs(kwargs):
        """Format the parameters for use when creating or updating a record"""
        special_keys = ['__class__', '_sa_instance_stat']
        kwargs = {k: v for k, v in kwargs.items() if k not in special_keys}
        if 'password' in kwargs:
            kwargs['password'] = hashlib.md5(kwargs['password'].encode('utf-8')).hexdigest().lower()
        if not kwargs.get('id'):
            kwargs['id'] = str(uuid.uuid4())
        if not kwargs.get('created_at'):
            kwargs['created_at'] = datetime.utcnow()
        if not kwargs.get('updated_at'):
            kwargs['updated_at'] = datetime.utcnow()
        if type(kwargs['created_at']) is str:
            kwargs['created_at'] = datetime.strptime(kwargs["created_at"], DATETIME_FORMAT)
        if type(kwargs['updated_at']) is str:
            kwargs['updated_at'] = datetime.strptime(kwargs["updated_at"], DATETIME_FORMAT)
        return kwargs

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        kwargs = self._refined_kwargs(kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, anotate=None):
        """returns a dictionary containing all keys/values of the instance"""
        special_keys = ['_sa_instance_state', '__class__', 'password']
        res = self.__dict__.copy()
        for k, v in res.items():
            if type(res[k]) is datetime:
                res[k] = res[k].strftime(DATETIME_FORMAT)
            elif type(res[k]) is date:
                res[k] = res[k].strftime(DATE_FORMAT)

        return {k: v for k, v in res.items() if k not in special_keys}

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)

    def update(self, kwargs):
        """Update the current record"""
        to_ignore = ['id', 'created_at', 'updated_at']
        kwargs = self._refined_kwargs({k: v for k, v in kwargs.items() if k not in to_ignore})
        for k, v in kwargs:
            setattr(self, k, v)
        self.save()
