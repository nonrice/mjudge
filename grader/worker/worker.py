import sys
import core.runner

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import select, update
import os

def main(*args, **kwargs):
    if len(sys.argv) < 2:
        print("Usage: python worker.py <submission_id>")
        sys.exit(1)

    submission_id = int(sys.argv[1])

    engine = create_engine(os.getenv("DATABASE_URL"))

    metadata = MetaData()
    submissions = Table("submissions", metadata, autoload_with=engine)
    testcases = Table("testcases", metadata, autoload_with=engine)
    problemset = Table("problems", metadata, autoload_with=engine)

    with engine.connect() as conn:
        submission_query = select(submissions).where(submissions.c.id == submission_id)
        submission_result = conn.execute(submission_query).fetchone()

        if not submission_result:
            print(f"No submission found with ID {submission_id}")
            sys.exit(1)
        if submission_result.status != "Waiting":
            print(f"Submission {submission_id} is not in 'Waiting' status, current status: {submission_result.status}")
            sys.exit(1)

        update_query = (
            update(submissions)
            .where(submissions.c.id == submission_id)
            .values(status="Running")
        )
        conn.execute(update_query)
        conn.commit() 

        problem_id = submission_result.problem_id
        testcases_query = select(testcases).where(testcases.c.problem_id == problem_id)
        testcases_result = conn.execute(testcases_query).fetchall()
        if not testcases_result:
            print(f"No testcases found for problem ID {problem_id}")
            sys.exit(1)

        problem_query = select(problemset).where(problemset.c.id == problem_id)
        problem_result = conn.execute(problem_query).fetchone()

        if not problem_result:
            print(f"No problem found with ID {problem_id}")
            sys.exit(1)

        user_code = submission_result.code
        user_lang = submission_result.language
        model_code = problem_result.solution
        model_lang = problem_result.solution_lang
        checker_code = problem_result.checker
        checker_lang = problem_result.checker_lang

        user_sol_path = f"/tmp/user_submission_{submission_id}.{user_lang}"
        with open(user_sol_path, "w") as f:
            f.write(user_code)
        model_sol_path = f"/tmp/model_solution_{problem_id}.{model_lang}"
        with open(model_sol_path, "w") as f:
            f.write(model_code)
        checker_path = f"/tmp/checker_{problem_id}.{checker_lang}"
        with open(checker_path, "w") as f:
            f.write(checker_code)

        time_limit = problem_result.time_limit/1000
        memory_limit = problem_result.memory_limit

        testcases_list = [ (tc.data, tc.sample) for tc in sorted(testcases_result, key=lambda x: x.number) ]
        try:
            status, feedback, in_contest_feedback, max_time, max_memory = core.runner.run_submission(
                user_sol_path,
                user_lang, 
                model_sol_path,
                model_lang,
                checker_path,
                checker_lang,
                testcases_list,
                time_limit=time_limit,
                memory_limit=memory_limit
            )
            print(status, feedback)
            update_query = (
                update(submissions)
                .where(submissions.c.id == submission_id)
                .values(status=status)
                .values(feedback=feedback)
                .values(in_contest_feedback=in_contest_feedback)
                .values(max_time=max_time)
                .values(max_memory=max_memory)
            )
            conn.execute(update_query)
            conn.commit()
        except Exception as e:
            print("Error during submission processing:", e)

        # uncomment to keep container alive for debugging
        # import time
        # while True:
        #     time.sleep(60)



if __name__ == "__main__":
    main()