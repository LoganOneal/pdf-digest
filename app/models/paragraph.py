from app.extensions import db


class Paragraph(db.Model):
    __tablename__ = "paragraph_table"
    id = db.Column(db.Integer, primary_key=True)
    text =  db.Column(db.String(5000))
    section_id = db.Column(db.Integer, db.ForeignKey("section_table.id"))
    section = db.relationship("Section", back_populates="paragraphs")

    def __repr__(self):
        return '<Paragraph %r>' % (self.id)



