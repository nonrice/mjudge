from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)


    # Register blueprints
    from app.grading.routes import grading_bp 

    app.register_blueprint(grading_bp, url_prefix="/")

    return app