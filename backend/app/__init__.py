from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    origins_list = os.getenv("CORS_ORIGINS", "").split(",")
    print("Allowed CORS origins:", origins_list)
    CORS(app, origins=origins_list)

    db.init_app(app)

    global limiter
    limiter.init_app(app)
    limiter.storage_uri = "memory://"
    limiter.default_limits = ["3 per second"]

    # Register blueprints
    from .auth.routes import auth_bp
    from .contests.routes import contests_bp
    from .submissions.routes import submissions_bp
    from .admin.routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(contests_bp, url_prefix="/api")
    app.register_blueprint(submissions_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")

    with app.app_context():
        from . import models
        db.create_all()

    return app