#!/usr/bin/python3
"""__init__  to create a unique FileStorage instance for your application"""
import os

from models.engine.db_storage import DBStorage
import cloudinary

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_NAME'),
    api_key=os.getenv('CLOUDINARY_KEY'),
    api_secret=os.getenv('CLOUDINARY_SECRET')
)

storage = DBStorage()
storage.reload()
