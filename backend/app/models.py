from . import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class Contests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Interval, nullable=False)

class Problems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    statement = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=True)
    solution_lang = db.Column(db.String(50), nullable=True)
    checker = db.Column(db.Text, nullable=True)
    checker_lang = db.Column(db.String(50), nullable=True)

class Testcases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey("problems.id"), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    data = db.Column(db.Text, nullable=False)
    problem = db.relationship("Problems", backref=db.backref("testcases", lazy=True))
    sample = db.Column(db.Boolean, default=False, nullable=False)

class Contest_Problems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer, db.ForeignKey("contests.id"), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey("problems.id"), nullable=False)
    letter = db.Column(db.String(1), nullable=False)
    contest = db.relationship("Contests", backref=db.backref("contest_problems", lazy=True))
    problem = db.relationship("Problems", backref=db.backref("contest_problems", lazy=True))

class Submissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    problem_id = db.Column(db.Integer, db.ForeignKey("problems.id"), nullable=False)  # Problem ID
    contest_id = db.Column(db.Integer, db.ForeignKey("contests.id"), nullable=True)  # Contest ID (nullable)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # User ID
    code = db.Column(db.Text, nullable=False)  # Submitted code
    language = db.Column(db.String(50), nullable=False)  # Programming language
    status = db.Column(db.String(50), nullable=False)  # Submission status (e.g., "Wrong answer")
    feedback = db.Column(db.Text, nullable=True)  # Feedback (e.g., compilation errors)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now())  # Submission time
    in_contest_feedback = db.Column(db.Boolean, default=True, nullable=False)  # Whether feedback is for in-contest use    

    # Relationships
    problem = db.relationship("Problems", backref=db.backref("submissions", lazy=True))
    contest = db.relationship("Contests", backref=db.backref("submissions", lazy=True))
    user = db.relationship("Users", backref=db.backref("submissions", lazy=True))


