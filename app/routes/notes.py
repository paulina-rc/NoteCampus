from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from app import db
from app.models.category import Category
from app.models.note import Note
from app.models.subject import Subject


notes = Blueprint("notes", __name__)


@notes.route("/notes")
def list_notes():
    subjects = Subject.query.order_by(Subject.name.asc()).all()

    return render_template(
        "notes.html",
        subjects=subjects
    )


@notes.route("/upload-note", methods=["GET", "POST"])
@login_required
def upload_note():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        file_url = request.form.get("file_url")
        subject_id = request.form.get("subject_id")
        category_id = request.form.get("category_id")

        category = Category.query.filter_by(
            id=category_id,
            subject_id=subject_id
        ).first()

        if category is None:
            return redirect(url_for("notes.upload_note"))

        new_note = Note(
            title=title,
            description=description,
            file_url=file_url,
            user_id=current_user.id,
            subject_id=subject_id,
            category_id=category_id
        )

        db.session.add(new_note)
        db.session.commit()

        return redirect(url_for("auth.dashboard"))

    subjects = Subject.query.order_by(Subject.name.asc()).all()
    categories = Category.query.order_by(Category.name.asc()).all()

    return render_template(
        "upload_note.html",
        subjects=subjects,
        categories=categories
    )
