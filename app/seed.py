from app import db
from app.models.category import Category
from app.models.subject import Subject


INITIAL_SUBJECTS = [
    {
        "name": "Mathematics",
        "description": "Notes, guides, and study material about mathematical topics.",
        "categories": [
            {
                "name": "Algebra",
                "description": "Equations, expressions, functions, and algebraic reasoning."
            },
            {
                "name": "Geometry",
                "description": "Shapes, angles, proofs, measurements, and spatial reasoning."
            },
            {
                "name": "Calculus",
                "description": "Limits, derivatives, integrals, and change."
            }
        ]
    },
    {
        "name": "Programming",
        "description": "Resources for learning software development and computer science.",
        "categories": [
            {
                "name": "Python",
                "description": "Python syntax, scripts, projects, and backend development."
            },
            {
                "name": "Java",
                "description": "Object-oriented programming, Java syntax, and applications."
            },
            {
                "name": "Web Development",
                "description": "HTML, CSS, JavaScript, Flask, and web application concepts."
            },
            {
                "name": "Databases",
                "description": "SQL, data modeling, queries, and database design."
            }
        ]
    },
    {
        "name": "Science",
        "description": "Study material for scientific concepts and natural sciences.",
        "categories": [
            {
                "name": "Biology",
                "description": "Cells, organisms, ecosystems, genetics, and life sciences."
            },
            {
                "name": "Chemistry",
                "description": "Atoms, reactions, compounds, and laboratory concepts."
            },
            {
                "name": "Physics",
                "description": "Motion, energy, forces, waves, and physical laws."
            }
        ]
    },
    {
        "name": "History",
        "description": "Summaries, timelines, and guides about historical events.",
        "categories": [
            {
                "name": "World History",
                "description": "Global events, civilizations, conflicts, and historical processes."
            },
            {
                "name": "Local History",
                "description": "Regional and national history resources."
            }
        ]
    }
]


def seed_initial_data():
    ensure_note_category_columns()

    for subject_data in INITIAL_SUBJECTS:
        subject = Subject.query.filter_by(
            name=subject_data["name"]
        ).first()

        if subject is None:
            subject = Subject(
                name=subject_data["name"],
                description=subject_data["description"]
            )
            db.session.add(subject)
            db.session.flush()

        for category_data in subject_data["categories"]:
            category = Category.query.filter_by(
                name=category_data["name"],
                subject_id=subject.id
            ).first()

            if category is None:
                db.session.add(
                    Category(
                        name=category_data["name"],
                        description=category_data["description"],
                        subject_id=subject.id
                    )
                )

    db.session.commit()
    assign_default_category_to_existing_notes()


def ensure_note_category_columns():
    note_columns = db.session.execute(
        db.text("PRAGMA table_info(notes)")
    ).fetchall()
    existing_column_names = {
        column[1]
        for column in note_columns
    }

    if "subject_id" not in existing_column_names:
        db.session.execute(
            db.text("ALTER TABLE notes ADD COLUMN subject_id INTEGER")
        )

    if "category_id" not in existing_column_names:
        db.session.execute(
            db.text("ALTER TABLE notes ADD COLUMN category_id INTEGER")
        )

    db.session.commit()


def assign_default_category_to_existing_notes():
    default_subject = Subject.query.filter_by(
        name="Mathematics"
    ).first()

    if default_subject is None:
        return

    default_category = Category.query.filter_by(
        name="Algebra",
        subject_id=default_subject.id
    ).first()

    if default_category is None:
        return

    db.session.execute(
        db.text(
            """
            UPDATE notes
            SET subject_id = :subject_id,
                category_id = :category_id
            WHERE subject_id IS NULL
               OR category_id IS NULL
            """
        ),
        {
            "subject_id": default_subject.id,
            "category_id": default_category.id
        }
    )
    db.session.commit()
