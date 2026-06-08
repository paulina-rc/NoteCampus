from flask import Blueprint, abort, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from app import db
from app.models.category import Category
from app.models.note import Note
from app.models.subject import Subject


notes = Blueprint("notes", __name__)


def validate_note_owner(note):
    if note.user_id != current_user.id:
        abort(403)


@notes.route("/notes")
def list_notes():
    subjects = Subject.query.order_by(Subject.name.asc()).all()

    return render_template(
        "notes.html",
        subjects=subjects
    )


@notes.route("/notes/<int:note_id>")
def note_detail(note_id):
    note = Note.query.get_or_404(note_id)

    return render_template(
        "note_detail.html",
        note=note
    )


@notes.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    validate_note_owner(note)

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
            return redirect(url_for("notes.edit_note", note_id=note.id))

        note.title = title
        note.description = description
        note.file_url = file_url
        note.subject_id = subject_id
        note.category_id = category_id

        db.session.commit()

        return redirect(url_for("notes.note_detail", note_id=note.id))

    subjects = Subject.query.order_by(Subject.name.asc()).all()
    categories = Category.query.order_by(Category.name.asc()).all()

    return render_template(
        "edit_note.html",
        note=note,
        subjects=subjects,
        categories=categories
    )


@notes.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    validate_note_owner(note)

    db.session.delete(note)
    db.session.commit()

    return redirect(url_for("auth.dashboard"))


@notes.route("/search")
def search():
    query = request.args.get("q", "").strip()
    search_results = []

    if query:
        search_pattern = f"%{query}%"
        search_results = Note.query.filter(
            db.or_(
                Note.title.ilike(search_pattern),
                Note.description.ilike(search_pattern)
            )
        ).order_by(
            Note.created_at.desc()
        ).all()

    return render_template(
        "search_results.html",
        query=query,
        notes=search_results
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
