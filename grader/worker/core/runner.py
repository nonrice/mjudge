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

    user_compile_return_code, user_compile_stdout, user_compile_stderr = user_program.compile()
    if user_compile_return_code != 0:
        return "Compilation Error", f"Submission failed to compile with return code {user_compile_return_code}.\nStandard Output: {user_compile_stdout}\nStandard Error: {user_compile_stderr}"

    model_program.compile()
    checker_program.compile()

    total_tests = len(testcases)
    for (number, testcase) in enumerate(testcases, start=1):
        user_return_code, user_stdout, user_stderr = user_program.execute(testcase)
        model_return_code, model_stdout, model_stderr = model_program.execute(testcase)
        
        if user_return_code != 0:
            return "Runtime Error", f"Submission failed on test {number}/{total_tests} with return code {user_return_code}.\nStandard Output: {user_stdout}\nStandard Error: {user_stderr}"

        with open("user_output.txt", "w") as f:
            f.write(user_stdout)
        with open("model_output.txt", "w") as f:
            f.write(model_stdout)
        
        checker_return_code, checker_stdout, checker_stderr = checker_program.execute(None, args=["user_output.txt", "model_output.txt"])
        if checker_return_code != 0:
            return "Wrong Answer", f"Checker failed on test {number}/{total_tests} with return code {checker_return_code}.\nStandard Output: {checker_stdout}\nStandard Error: {checker_stderr}"

    return "Accepted", f"{total_tests}/{total_tests} tests passed successfully." 
