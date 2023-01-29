from app.extensions import db
from flask_login import UserMixin

class File(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.Text, unique=True)
    

   