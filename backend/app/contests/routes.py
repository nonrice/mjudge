from datetime import datetime, timezone
from flask import Blueprint, jsonify, abort
from app.models import Contests, Problems, Contest_Problems, Submissions
import os
from app.contests.core import leaderboard
from flask import jsonify

contests_bp = Blueprint("contests", __name__)

@contests_bp.route("/contestList", methods=["GET"])
def contest_list():
    contests = Contests.query.all()
    return jsonify([{
        "id": c.id,
        "title": c.title,
        "start_time": c.start_time.isoformat()
    } for c in contests])

@contests_bp.route("/contest/<int:contest_id>/problems", methods=["GET"])
def get_problems(contest_id):
    problems = Contest_Problems.query.filter_by(contest_id=contest_id).all()
    return jsonify([{
        "id": p.id,
        "letter": p.letter,
        "title": Problems.query.get(p.problem_id).title,
    } for p in problems])

@contests_bp.route("/contest/<int:contest_id>/title", methods=["GET"])
def get_contest_title(contest_id):
    contest = Contests.query.get(contest_id)
    if not contest:
        abort(404)
    return jsonify({"title": contest.title})

@contests_bp.route("/contest/<int:contest_id>/problem/<problem_letter>", methods=["GET"])
def get_problem(contest_id, problem_letter):
    problem = Contest_Problems.query.filter_by(contest_id=contest_id, letter=problem_letter).first()
    if not problem:
        abort(404)

    problem_id = problem.problem_id
    
    return jsonify({
        "title": Problems.query.get(problem_id).title,
        "statement": Problems.query.get(problem_id).statement
    })

@contests_bp.route("/contest/<int:contest_id>/leaderboard", methods=["GET"])
def get_leaderboard(contest_id):
    submissions = Submissions.query.filter_by(contest_id=contest_id).all()
    users = {sub.user_id: sub.user.username for sub in submissions if sub.user}
    problem_legend = { letter : index for index, letter in enumerate(sorted([ p.letter for p in Contest_Problems.query.filter_by(contest_id=contest_id).all() ])) }
    lb = leaderboard.leaderboard(users, problem_legend)
    start_time = Contests.query.get(contest_id).start_time
    duration = Contests.query.get(contest_id).duration.total_seconds() // 60
    for sub in submissions:
        contest_problem = Contest_Problems.query.filter_by(contest_id=contest_id, problem_id=sub.problem_id).first()
        problem_letter = contest_problem.letter if contest_problem else None
        if problem_letter is None:
            continue

        elapsed_time = (sub.timestamp - start_time).total_seconds() // 60
        if elapsed_time > duration:
            continue
        lb.set_submission(sub.user_id, problem_letter, elapsed_time, sub.status == "Accepted")
    data = jsonify(lb.to_dict())

    return data, 200

@contests_bp.route("/contest/<int:contest_id>/timing", methods=["GET"])
def get_contest_timing(contest_id):
    contest = Contests.query.get(contest_id)
    if not contest:
        abort(404)
    
    start_time = contest.start_time.isoformat()
    duration = str(contest.duration.total_seconds() // 60) + " minutes"
    end_time = contest.start_time + contest.duration
    
    return jsonify({
        "start_time": start_time,
        "duration": duration,
        "end_time": end_time.isoformat(),
    })

@contests_bp.route("/server_time", methods=["GET"])
def get_server_time():
    current_time = datetime.now(timezone.utc).isoformat()
    return jsonify({"now": current_time})


