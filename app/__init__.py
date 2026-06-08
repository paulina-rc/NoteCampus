from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.models.user import User
    from app.models.subject import Subject
    from app.models.category import Category
    from app.models.note import Note

    with app.app_context():
        db.create_all()
        from app.seed import seed_initial_data
        seed_initial_data()

    from app.routes.auth import auth
    from app.routes.notes import notes
    from app.routes.subjects import subjects
    from app.routes.profile import profile

    app.register_blueprint(auth)
    app.register_blueprint(notes)
    app.register_blueprint(subjects)
    app.register_blueprint(profile)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
