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
    unprocesses = 1
    parsing = 2
    parsed = 3
    summarized = 4

class File(db.Model):
    __tablename__ = 'Files'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    date = db.Column(db.DateTime(timezone=True), default=func.now())
    filename = db.Column(db.String(50))
    extension = db.Column(db.String(8))
    status = db.Column(db.String(8))
    data = db.Column(db.LargeBinary)

