from flask import Flask, request, jsonify, Blueprint
from app.utils.decorators import jwt_required
from app import db

from app.models import Problems, Testcases
import zipfile
import os
import tempfile
import json

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/upload_prob", methods=["POST"])
@jwt_required
def upload_problem_zip():
    # I'm the only admin :)))
    if request.user["username"] != "eric":
        return jsonify({"error": "Unauthorized"}), 403

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith(".zip"):
        return jsonify({"error": "Uploaded file must be a .zip"}), 400
    


    with tempfile.TemporaryDirectory() as extract_root:
        zip_path = os.path.join(extract_root, "problem.zip")
        file.save(zip_path)

        # By default my computer compresses a folder into a zip. So after unzip, we need to find the top level dir
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_root)

        entries = [e for e in os.listdir(extract_root) if e not in [".DS_Store", "Thumbs.db", "__MACOSX", "problem.zip"]]
        print("Extracted entries:", entries)
        if len(entries) == 1 and os.path.isdir(os.path.join(extract_root, entries[0])):
            tmpdir = os.path.join(extract_root, entries[0])
            print("Extracted to top-level folder:", tmpdir)

        extracted_files = os.listdir(tmpdir)
        tests_dir = os.path.join(tmpdir, "tests")
        info_path = os.path.join(tmpdir, "info.json")

        if not os.path.exists(info_path):
            return jsonify({"error": "Missing info.json"}), 400

        with open(info_path) as f:
            try:
                info = json.load(f)
            except json.JSONDecodeError:
                return jsonify({"error": "Malformed info.json"}), 400

        solution_file = next((f for f in extracted_files if f.startswith("solution.")), None)
        checker_file = next((f for f in extracted_files if f.startswith("checker.")), None)
        statement_file = next((f for f in extracted_files if f.startswith("statement.")), None)

        if not solution_file:
            return jsonify({"error": "Missing solution file"}), 400

        test_inputs = []
        if os.path.isdir(tests_dir):
            for name in os.listdir(tests_dir):
                if name.endswith(".txt") and name[:-4].isdigit():
                    test_inputs.append(name)

        test_inputs.sort(key=lambda x: int(x.split(".")[0]))

        problem_title = info.get("title", "Untitled Problem")
        time_limit = info.get("time_limit", 1000)  # Default to 1000 ms if not specified
        memory_limit = info.get("memory_limit", 256)  # Default to 256 MB if not specified
        solution_lang = info.get("solution_lang", "python3")  # Default to python3 if not specified
        checker_lang = info.get("checker_lang", "python3")  # Default to python3 if not specified
        with open(os.path.join(tmpdir, solution_file)) as sol_file:
            solution_contents = sol_file.read()
        with open(os.path.join(tmpdir, checker_file)) as chk_file:
            checker_contents = chk_file.read()
        with open(os.path.join(tmpdir, statement_file)) as stmt_file:
            statement_contents = stmt_file.read()
        
        new_problem = Problems(
            title=problem_title,
            statement=statement_contents,
            solution=solution_contents,
            solution_lang=solution_lang,
            checker=checker_contents if checker_file else None,
            checker_lang=checker_lang if checker_file else None,
            time_limit=time_limit,
            memory_limit=memory_limit
        )
        db.session.add(new_problem)
        db.session.commit()


        for i, test_input in enumerate(test_inputs, start=1):
            with open(os.path.join(tests_dir, test_input)) as f:
                data = f.read()
            new_testcase = Testcases(
                problem_id=new_problem.id,
                number=i,
                data=data,
                sample=i in info.get("samples", [])
            )
            db.session.add(new_testcase)
        db.session.commit()

        return jsonify({
            "message": "Problem uploaded successfully",
            "info": info,
            "tests": test_inputs,
            "solution": solution_file,
            "checker": checker_file,
            })