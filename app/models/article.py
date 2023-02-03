from app.extensions import db
from sqlalchemy.sql import func


class Article(db.Model):
    __tablename__ = "article_table"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))    
    title = db.Column(db.String(50))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    sections = db.relationship("Section", back_populates="article")
    
    def __repr__(self):
        return '<Article %r>' % (self.title)



