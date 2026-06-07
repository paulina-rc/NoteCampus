from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask, render_template

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)

    # login_manager.init_app(app)

    from app.models.user import User

    with app.app_context():
        db.create_all()

    from app.routes.auth import auth

    app.register_blueprint(auth)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app