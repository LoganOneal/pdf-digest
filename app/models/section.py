from app.extensions import db


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

