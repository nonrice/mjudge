from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///site.db")
    app.config["SECRET_KEY"] = "your_jwt_secret_key"
    CORS(app, origins=["http://127.0.0.1:4999", "http://127.0.0.1:3000"])

    db.init_app(app)

    # Register blueprints
    from .auth.routes import auth_bp
    from .contests.routes import contests_bp
    from .submissions.routes import submissions_bp

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(contests_bp, url_prefix="/api")
    app.register_blueprint(submissions_bp, url_prefix="/api")

    with app.app_context():
        from . import models
        db.create_all()

    return app