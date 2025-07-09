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

def trunc_output(output, max_length=1000):
    output_string = str(output)
    if len(output_string) > max_length:
        return output_string[:max_length] + f"\n... String truncated to {max_length} characters.\n"
    return output_string

def wipe_perms(path):
    # Given a path, recursively set the "other" and "group" permissions to ---
    for root, dirs, files in os.walk(path):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o700)
        for f in files:
            os.chmod(os.path.join(root, f), 0o700)

def run_submission(user_sol_path, user_sol_lang, model_sol_path, model_sol_lang, checker_path, checker_lang, testcases, time_limit=2, memory_limit=256):
    time_multiplier = core.util.time_calibration.get_time_multiplier_python3_1e8_2000()
    time_limit = time_limit * time_multiplier
    print(f"Time multiplier: {time_multiplier}, Adjusted time limit: {time_limit} seconds")

    user_program = make_program(user_sol_path, user_sol_lang)
    model_program = make_program(model_sol_path, model_sol_lang)
    checker_program = make_program(checker_path, checker_lang)

    model_program.compile()
    checker_program.compile()

    wipe_perms("/tmp")
    # user sol source still needs rwx
    os.chmod(user_sol_path, 0o666)

    user_compile_result = user_program.compile()
    print(f"User compile result: {user_compile_result}")
    if user_compile_result.failure:
        return "Compilation Error", f"Submission failed to compile with return code {user_compile_result.return_code}.\nStandard Output:\n{user_compile_result.stdout}\nStandard Error:\n{user_compile_result.stderr}", True, -1, -1

    max_time=0
    max_memory=0

    total_tests = len(testcases)
    for (number, tc) in enumerate(testcases, start=1):
        testcase, sample = tc
        user_result = user_program.execute(testcase, time_limit=time_limit, memory_limit=memory_limit, become_nobody=True)
        model_result = model_program.execute(testcase, time_limit=time_limit, memory_limit=memory_limit)

        max_time = max(max_time, int(1000 * (user_result.time/time_multiplier)))
        max_memory = max(max_memory, user_result.memory)
        print(f"Test {number}/{total_tests}: User time: {user_result.time}, Memory: {user_result.memory}, Return code: {user_result.return_code}")
        
        if user_result.failure:
            return user_result.failure, f"Submission failed on test {number}/{total_tests} with return code {user_result.return_code}.\nTest Case:\n{trunc_output(testcase)}\nStandard Output:\n{trunc_output(user_result.stdout)}\nStandard Error:\n{trunc_output(user_result.stderr)}", sample, max_time, max_memory

        with open("/tmp/user_output.txt", "w") as f:
            f.write(user_result.stdout)
        with open("/tmp/model_output.txt", "w") as f:
            f.write(model_result.stdout)
        with open(f"/tmp/testcase_{number}.txt", "w") as f:
            f.write(testcase)
        
        checker_result = checker_program.execute(None, args=["/tmp/user_output.txt", "/tmp/model_output.txt", f"/tmp/testcase_{number}.txt"])
        if checker_result.failure:
            return "Wrong Answer", f"Checker failed on test {number}/{total_tests} with return code {trunc_output(checker_result.return_code)}.\nTest Case:\n{trunc_output(testcase)}\nUser Standard Output:\n{trunc_output(user_result.stdout)}\nJury Standard Output:\n{trunc_output(model_result.stdout)}\nChecker Standard Output:\n{trunc_output(checker_result.stdout)}\nChecker Standard Error: {trunc_output(checker_result.stderr)}", sample, max_time, max_memory
        
        # these should still have r perms for other, so need to remove or clear them
        os.remove("/tmp/user_output.txt")
        os.remove("/tmp/model_output.txt")
        os.remove(f"/tmp/testcase_{number}.txt")

    return "Accepted", f"{total_tests}/{total_tests} tests passed successfully.", True, max_time, max_memory
