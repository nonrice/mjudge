from flask import Blueprint, request, jsonify, current_app
from app import db
from app.utils.decorators import jwt_required
from app.models import Submissions, Users, Contests, Problems, Contest_Problems, Testcases
import requests

submissions_bp = Blueprint("submissions", __name__)

@submissions_bp.route("/submit", methods=["POST"])
@jwt_required
def submit_code():
    data = request.get_json()
    if not data or "code" not in data or "language" not in data:
        return jsonify({"error": "Invalid request"}), 400

    contest_id = data.get("contest_id")
    problem_letter = data.get("problem_letter")
    problem_id = None
    if contest_id and problem_letter:
        contest_problem = Contest_Problems.query.filter_by(contest_id=contest_id, letter=problem_letter).first()
        if not contest_problem:
            return jsonify({"error": "Problem not found in the contest"}), 404
        problem_id = contest_problem.problem_id
    elif "problem_id" in data:
        problem_id = data["problem_id"]
    else:
        return jsonify({"error": "Problem ID or contest ID and problem letter must be provided"}), 400
    
    print(data)
    submission_entry = Submissions(
        problem_id=problem_id,
        contest_id=data.get("contest_id"),
        user_id=request.user["user_id"],
        code=data["code"],
        language=data["language"],
        status="Waiting",
        feedback="Waiting"
    )
    db.session.add(submission_entry)
    db.session.commit()

    return jsonify({
        "message": "Code submitted successfully",
        "submission_id": submission_entry.id
    }), 201

@submissions_bp.route("/submissions/<int:contest_id>", methods=["GET"])
@jwt_required
def get_user_submissions(contest_id):
    user_id = request.user["user_id"]
    submissions = Submissions.query.filter_by(user_id=user_id, contest_id=contest_id).all()
    
    return jsonify([{
        "id": submission.id,
        "problem_id": submission.problem_id,
        "code": submission.code,
        "language": submission.language,
        "status": submission.status,
        "feedback": submission.feedback
    } for submission in submissions]), 200

@submissions_bp.route("/submission/<int:submission_id>", methods=["GET"])
@jwt_required
def get_submission(submission_id):
    submission = Submissions.query.get(submission_id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404
    
    contest = Contests.query.get(submission.contest_id)
    if not contest:
        return jsonify({"error": "Contest not found"}), 404

    end_time = contest.start_time + contest.duration
    contest_ended = end_time < db.func.now()

    user_id = request.user["user_id"]
    my_submission = submission.user_id == user_id

    if not my_submission and not contest_ended:
        return jsonify({"error": "You are not allowed to view this submission"}), 403
    
    problem_letter = Contest_Problems.query.filter_by(contest_id=submission.contest_id, problem_id=submission.problem_id).first().letter if submission.contest_id else None
    
    return jsonify({
        "id": submission.id,
        "contest_id": submission.contest_id,
        "problem_letter": problem_letter,
        "code": submission.code,
        "language": submission.language,
        "status": submission.status,
        "feedback": submission.feedback,
        "timestamp": submission.timestamp.isoformat()
    }), 200





