import os
import core.program.cpp, core.program.python3, core.program.java
import core.util.time_calibration

def make_program(source_path, lang):
    overrides = {
        "cpp": core.program.cpp.CppProgram,
        "python3": core.program.python3.Python3Program,
        "java": core.program.java.JavaProgram,
    }


    if lang not in overrides:
        raise ValueError(f"Unsupported language: {lang}")
    
    return overrides[lang](source_path)


def run_submission(user_sol_path, user_sol_lang, model_sol_path, model_sol_lang, checker_path, checker_lang, testcases, time_limit=2, memory_limit=256):
    time_multiplier = core.util.time_calibration.get_time_multiplier_python3_1e8_2000()
    time_limit = time_limit * time_multiplier
    print(f"Time multiplier: {time_multiplier}, Adjusted time limit: {time_limit} seconds")

    user_program = make_program(user_sol_path, user_sol_lang)
    model_program = make_program(model_sol_path, model_sol_lang)
    checker_program = make_program(checker_path, checker_lang)

    user_compile_result = user_program.compile()
    print(f"User compile result: {user_compile_result}")
    if user_compile_result.failure:
        return "Compilation Error", f"Submission failed to compile with return code {user_compile_result.return_code}.\nStandard Output: {user_compile_result.stdout}\nStandard Error: {user_compile_result.stderr}", -1, -1

    model_program.compile()
    checker_program.compile()

    max_time=0
    max_memory=0

    total_tests = len(testcases)
    for (number, tc) in enumerate(testcases, start=1):
        testcase, sample = tc
        user_result = user_program.execute(testcase, time_limit=time_limit, memory_limit=memory_limit)
        model_result = model_program.execute(testcase, time_limit=time_limit, memory_limit=memory_limit)

        max_time = max(max_time, int(1000 * (user_result.time/time_multiplier)))
        max_memory = max(max_memory, user_result.memory)
        print(f"Test {number}/{total_tests}: User time: {user_result.time}, Memory: {user_result.memory}, Return code: {user_result.return_code}")
        
        if user_result.failure:
            return user_result.failure, f"Submission failed on test {number}/{total_tests} with return code {user_result.return_code}.\nTest Case:\n{testcase}\nStandard Output:\n{user_result.stdout}\nStandard Error:\n{user_result.stderr}", sample, max_time, max_memory

        with open("user_output.txt", "w") as f:
            f.write(user_result.stdout)
        with open("model_output.txt", "w") as f:
            f.write(model_result.stdout)
        with open(f"testcase_{number}.txt", "w") as f:
            f.write(testcase)
        
        checker_result = checker_program.execute(None, args=["user_output.txt", "model_output.txt", f"testcase_{number}.txt"])
        if checker_result.failure:
            return "Wrong Answer", f"Checker failed on test {number}/{total_tests} with return code {checker_result.return_code}.\nTest Case:\n{testcase}\nUser Standard Output:\n{user_result.stdout}\nJury Standard Output:\n{model_result.stdout}\nChecker Standard Output:\n{checker_result.stdout}\nChecker Standard Error: {checker_result.stderr}", sample, max_time, max_memory

    return "Accepted", f"{total_tests}/{total_tests} tests passed successfully.", True, max_time, max_memory
