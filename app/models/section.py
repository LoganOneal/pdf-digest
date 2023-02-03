from app.extensions import db


class Section(db.Model):
    __tablename__ = "sections"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    num =  db.Column(db.String(50))
    paragraphs = db.relationship("Paragraph")
    article_idf = db.Column(db.Integer, db.ForeignKey("articles.id"))



