import os
import core.program.cpp, core.program.python3

def make_program(source_path, lang):
    overrides = {
        "cpp": core.program.cpp.CppProgram,
        "python3": core.program.python3.Python3Program,
    }


    if lang not in overrides:
        raise ValueError(f"Unsupported language: {lang}")
    
    return overrides[lang](source_path)


def run_submission(user_sol_path, user_sol_lang, model_sol_path, model_sol_lang, checker_path, checker_lang, testcases):
    user_program = make_program(user_sol_path, user_sol_lang)
    model_program = make_program(model_sol_path, model_sol_lang)
    checker_program = make_program(checker_path, checker_lang)

    user_compile_result = user_program.compile()
    print(f"User compile result: {user_compile_result}")
    if user_compile_result.failure:
        return "Compilation Error", f"Submission failed to compile with return code {user_compile_result.return_code}.\nStandard Output: {user_compile_result.stdout}\nStandard Error: {user_compile_result.stderr}"

    model_program.compile()
    checker_program.compile()

    total_tests = len(testcases)
    for (number, tc) in enumerate(testcases, start=1):
        testcase, sample = tc
        user_result = user_program.execute(testcase)
        model_result = model_program.execute(testcase)
        
        if user_result.failure:
            return user_result.failure, f"Submission failed on test {number}/{total_tests} with return code {user_result.return_code}.\nStandard Output: {user_result.stdout}\nStandard Error: {user_result.stderr}", sample

        with open("user_output.txt", "w") as f:
            f.write(user_result.stdout)
        with open("model_output.txt", "w") as f:
            f.write(model_result.stdout)
        with open(f"testcase_{number}.txt", "w") as f:
            f.write(testcase)
        
        checker_result = checker_program.execute(None, args=["user_output.txt", "model_output.txt", f"testcase_{number}.txt"])
        if checker_result.failure:
            return "Wrong Answer", f"Checker failed on test {number}/{total_tests} with return code {checker_result.return_code}.\nStandard Output: {checker_result.stdout}\nStandard Error: {checker_result.stderr}", sample

    return "Accepted", f"{total_tests}/{total_tests} tests passed successfully.", True
