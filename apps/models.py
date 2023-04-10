# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.extensions import db
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
    status = db.Column(db.Integer, default=Status.UNPROCESSED)
    data = db.Column(db.LargeBinary)
    
    def __init__(self, filename, data, extension, user_id):
        self.filename = filename
        self.data = data
        self.extension = extension
        self.user_id = user_id

    def __repr__(self):
        return str(self.id)
    
class ArticleModel(db.Model):
    __tablename__ = "article_table"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))    
    title = db.Column(db.String(50))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    sections = db.relationship("Section", back_populates="article")
    
    def __repr__(self):
        return '<Article %r>' % (self.title)
    

class Paragraph(db.Model):
    __tablename__ = "paragraph_table"
    id = db.Column(db.Integer, primary_key=True)
    text =  db.Column(db.String(5000))
    
    section_id = db.Column(db.Integer, db.ForeignKey("section_table.id"))
    section = db.relationship("Section", back_populates="paragraphs")

    def __repr__(self):
        return '<Paragraph %r>' % (self.id)


class Section(db.Model):
    __tablename__ = "section_table"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    num =  db.Column(db.String(50))
    article_id = db.Column(db.Integer, db.ForeignKey("article_table.id"))

    article = db.relationship("ArticleModel", back_populates="sections")
    paragraphs = db.relationship("Paragraph", back_populates="section")

    def __repr__(self):
        return '<Section %r>' % (self.name)




