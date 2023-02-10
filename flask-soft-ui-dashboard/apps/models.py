# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps import db
from sqlalchemy.sql import func
from sqlalchemy import Enum

'''
Add your models below
'''


# Book Sample
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))

class Status(Enum):
    UNPROCESSED = 1
    PARSING = 2
    PARSED = 3
    SUMMARIZED = 4

class File(db.Model):
    __tablename__ = 'Files'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    date = db.Column(db.DateTime(timezone=True), default=func.now())
    filename = db.Column(db.String(50))
    extension = db.Column(db.String(8))
    status = db.Column(db.Integer, default=Status.UNPROCESSED.value)))
    data = db.Column(db.LargeBinary)
    
    def __init__(self, filename, data, extension, user_id):
        self.filename = filename
        self.data = data
        self.extension = extension
        self.user_id = user_id

    def __repr__(self):
        return str(self.id)

