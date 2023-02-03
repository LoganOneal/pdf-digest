from app.extensions import db


class Paragraph(db.Model):
    __tablename__ = "paragraphs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    text =  db.Column(db.String(5000))
    section_idf = db.Column(db.Integer, db.ForeignKey("sections.id"))



