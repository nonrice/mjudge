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

    model_code = Problems.query.get(problem_id).solution
    model_lang = Problems.query.get(problem_id).solution_lang
    checker = Problems.query.get(problem_id).checker
    checker_lang = Problems.query.get(problem_id).checker_lang
    testcases = { tc.number : tc.data for tc in Testcases.query.filter_by(problem_id=problem_id).all() }
    submission = {
        "submission_id": submission_entry.id,  
        "code": data["code"],
        "language": data["language"],
        "model_code": model_code,
        "model_lang": model_lang,
        "checker": checker,
        "checker_lang": checker_lang,
        "testcases": testcases
    }

    headers = {
        "Content-Type": "application/json"
    }
    url = "http://localhost:4999/grade"
    response = requests.post(url, json=submission, headers=headers);
    if response.status_code != 200:
        return jsonify({"error": "Grading service is unavailable"}), 503

    return jsonify({
        "message": "Code submitted successfully",
        "submission_id": submission_entry.id
    }), 201

@submissions_bp.route("/verdict", methods=["POST"])
def set_verdict():
    print("set a verdict")
    data = request.get_json()
    if not data or "submission_id" not in data or "verdict" not in data:
        return jsonify({"error": "Invalid request"}), 400

    submission_id = data["submission_id"]
    verdict = data["verdict"]
    time_used = data.get("time_used", 0)
    memory_used = data.get("memory_used", 0)

    # Here you would typically save the verdict to the database
    # For this example, we will just print it
    current_app.logger.info(f"Submission {submission_id} verdict: {verdict}, time used: {time_used}, memory used: {memory_used}")

    submission = Submissions.query.get(submission_id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404
    submission.status = verdict
    submission.time_used = time_used
    submission.memory_used = memory_used
    db.session.commit()

    return jsonify({"message": "Verdict recorded successfully"}), 200





