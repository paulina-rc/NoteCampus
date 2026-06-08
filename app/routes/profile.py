from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.user import User
from app.models.note import Note

profile = Blueprint("profile", __name__)


@profile.route("/profile")
@login_required
def profile_view():
    """Display user profile with statistics and recent notes."""
    
    total_notes = Note.query.filter_by(user_id=current_user.id).count()
    
    total_subjects = db.session.query(Note.subject_id).filter_by(
        user_id=current_user.id
    ).distinct().count()
    
    recent_notes = Note.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Note.created_at.desc()
    ).limit(5).all()
    
    return render_template(
        "profile.html",
        user=current_user,
        total_notes=total_notes,
        total_subjects=total_subjects,
        recent_notes=recent_notes
    )


@profile.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    """Edit user profile (username and email)."""
    
    errors = {}
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        
        if not username:
            errors["username"] = "Username cannot be empty."
        elif len(username) < 3:
            errors["username"] = "Username must be at least 3 characters."
        elif len(username) > 50:
            errors["username"] = "Username must be at most 50 characters."
        
        if not email:
            errors["email"] = "Email cannot be empty."
        elif len(email) > 120:
            errors["email"] = "Email must be at most 120 characters."
        elif "@" not in email or "." not in email.split("@")[-1]:
            errors["email"] = "Please enter a valid email address."
        
        if username and not errors.get("username"):
            existing_username = User.query.filter(
                User.username == username,
                User.id != current_user.id
            ).first()
            if existing_username:
                errors["username"] = "This username is already taken."
        
        if email and not errors.get("email"):
            existing_email = User.query.filter(
                User.email == email,
                User.id != current_user.id
            ).first()
            if existing_email:
                errors["email"] = "This email is already in use."
        
        if not errors:
            try:
                current_user.username = username
                current_user.email = email
                db.session.commit()
                return redirect(url_for("profile.profile_view"))
            except IntegrityError:
                db.session.rollback()
                errors["general"] = "An error occurred while saving. Please try again."
    
    return render_template(
        "edit_profile.html",
        user=current_user,
        errors=errors
    )
