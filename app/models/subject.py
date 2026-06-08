from app import db


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    categories = db.relationship(
        "Category",
        backref="subject",
        lazy=True,
        cascade="all, delete-orphan"
    )

    notes = db.relationship(
        "Note",
        backref="subject",
        lazy=True
    )

    def __repr__(self):
        return f"<Subject {self.name}>"
