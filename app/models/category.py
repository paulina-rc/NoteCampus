from app import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    notes = db.relationship(
        "Note",
        backref="category",
        lazy=True
    )

    __table_args__ = (
        db.UniqueConstraint(
            "name",
            "subject_id",
            name="uq_category_name_subject"
        ),
    )

    def __repr__(self):
        return f"<Category {self.name}>"
