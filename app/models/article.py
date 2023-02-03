from app.extensions import db
from sqlalchemy.sql import func


class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))    
    title = db.Column(db.String(50))
    sections = db.relationship("Section")



