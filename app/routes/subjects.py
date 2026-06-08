from flask import Blueprint, render_template

from app.models.category import Category
from app.models.subject import Subject


subjects = Blueprint("subjects", __name__)


@subjects.route("/subjects")
def list_subjects():
    all_subjects = Subject.query.order_by(Subject.name.asc()).all()

    return render_template(
        "subjects.html",
        subjects=all_subjects
    )


@subjects.route("/subjects/<int:subject_id>")
def subject_detail(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    return render_template(
        "subject_detail.html",
        subject=subject
    )


@subjects.route("/categories/<int:category_id>")
def category_detail(category_id):
    category = Category.query.get_or_404(category_id)

    return render_template(
        "category_detail.html",
        category=category
    )
