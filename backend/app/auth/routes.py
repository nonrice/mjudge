from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
from app import db
from app.models import Users
from app.utils.decorators import jwt_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if Users.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "User already exists"}), 400
    
    if len(data["username"]) < 4 or len(data["username"]) > 20 or not all(c.isalnum() or c in ['_', '.'] for c in data["username"]):
        return jsonify({"error": "Username must be between 5 and 20 characters and contain only alphanumeric characters, underscores, and periods"}), 400

    hashed_pw = generate_password_hash(data["password"])
    new_user = Users(username=data["username"], password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = Users.query.filter_by(username=data["username"]).first()
    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({"token": token})

@auth_bp.route("/whoami", methods=["GET"])
@jwt_required
def whoami():
    user_id = request.user["user_id"]
    return jsonify({"message": f"Hello user {user_id}"})