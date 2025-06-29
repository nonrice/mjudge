import os
import subprocess
import resource
import core.util.execution_result

def limited_subprocess(command, stdin, time_limit, memory_limit):
    def set_limit_preexec():
        os.setsid()
        time_limit_ceil = int(time_limit + 1)
        resource.setrlimit(resource.RLIMIT_CPU, (time_limit_ceil, time_limit_ceil))
        resource.setrlimit(resource.RLIMIT_AS, (memory_limit * 1024 * 1024, memory_limit * 1024 * 1024))

    usage_before = resource.getrusage(resource.RUSAGE_CHILDREN)
    try:
        result = subprocess.run(
            command,
            input=stdin,
            text=True,
            capture_output=True,
            preexec_fn=set_limit_preexec,
            timeout=time_limit
        )

        usage_after = resource.getrusage(resource.RUSAGE_CHILDREN)

        cpu_time = (usage_after.ru_utime + usage_after.ru_stime) - (usage_before.ru_utime + usage_before.ru_stime)
        max_rss = usage_after.ru_maxrss
        max_rss_kb = max_rss
        if os.uname().sysname == "Darwin":  # macOS reports in bytes
            max_rss_kb = max_rss / 1024
        
    except subprocess.TimeoutExpired as e:
        return core.util.execution_result.ExecutionResult(
            return_code=-1,
            stdout="",
            stderr="",
            time=time_limit,
            memory=-1,
            failure="Time limit exceeded"
        )
    except Exception as e:
        return core.util.execution_result.ExecutionResult(
            return_code=-1,
            stdout="",
            stderr=str(e),
            time=-1,
            memory=-1,
            failure="Runtime error"
        )
    
    if result.returncode != 0:
        return core.util.execution_result.ExecutionResult(
            return_code = result.returncode,
            stdout = result.stdout,
            stderr = result.stderr,
            time = cpu_time,
            memory = max_rss_kb,
            failure = "Runtime error"
        )

    
    if cpu_time > time_limit:
        return core.util.execution_result.ExecutionResult( 
            return_code = -1,
            stdout = "",
            stderr = "",
            time = time_limit,
            memory = -1,
            failure = "Time limit exceeded"
        )

    return core.util.execution_result.ExecutionResult( 
        return_code = result.returncode,
        stdout = result.stdout,
        stderr = result.stderr,
        time = cpu_time,
        memory = max_rss_kb,
        failure = None
    )


