from app.extensions import db
from sqlalchemy.sql import func

class File(db.Model):
    __tablename__ = "file"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    extension = db.Column(db.String(16))
    data = db.Column(db.LargeBinary)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))