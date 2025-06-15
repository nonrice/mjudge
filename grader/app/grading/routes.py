from flask import Blueprint, request, jsonify
from app.grading.core.judge import judge_code 

grading_bp = Blueprint("grading", __name__)

@grading_bp.route("/grade", methods=["POST"])
def grade_submission():

    # Start a grading process...
    # This is a placeholder for the actual grading logic.

    data = request.get_json()

    print("Received data for grading:")
    print(data)
    if not data or "submission_id" not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    judge_code(data["submission_id"])

    return jsonify({"message": "Grading started"}), 200
