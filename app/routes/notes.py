from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from app import db
from app.models.note import Note


notes = Blueprint("notes", __name__)


@notes.route("/notes")
def list_notes():
    all_notes = Note.query.order_by(Note.created_at.desc()).all()

    return render_template(
        "notes.html",
        notes=all_notes
    )


@notes.route("/upload-note", methods=["GET", "POST"])
@login_required
def upload_note():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        file_url = request.form.get("file_url")

        new_note = Note(
            title=title,
            description=description,
            file_url=file_url,
            user_id=current_user.id
        )

        db.session.add(new_note)
        db.session.commit()

        return redirect(url_for("auth.dashboard"))

    return render_template("upload_note.html")
