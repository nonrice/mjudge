import os, pwd, grp, traceback, sys
import subprocess
import resource
import tempfile
import core.util.execution_result

def limited_subprocess(command, stdin, time_limit, memory_limit, become_nobody=False):
    def set_limit_preexec():
        try:
            os.setsid()
            time_limit_ceil = int(time_limit + 1)
            mem_bytes = memory_limit * 1024 * 1024
            if become_nobody:
                resource.setrlimit(resource.RLIMIT_NPROC, (50, 50)) # because jvm is a btch. I would do 1 if i could
            resource.setrlimit(resource.RLIMIT_CPU, (time_limit_ceil, time_limit_ceil))
            resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))

            if become_nobody:
                pw_record = pwd.getpwnam("nobody")
                os.setgid(pw_record.pw_gid)
                os.setuid(pw_record.pw_uid)

        except Exception as e:
            with open("/tmp/preexec_error.log", "w") as f:
                traceback.print_exc(file=f)
            sys.exit(1)

    with tempfile.NamedTemporaryFile(delete=False) as tmp_time:
        time_output_path = tmp_time.name

    if become_nobody:
        # Give rwx perms to time output file for other (so nobody user)
        os.chmod(time_output_path, 0o666)

    time_command = ["/usr/bin/time", "-v", "-o", time_output_path]
    
    # Erasing database url from subprocess bc it contains the credentials lmao
    env_var_blacklist = {"DATABASE_URL"}
    clean_env = {k: v for k, v in os.environ.items() if k not in env_var_blacklist}

    usage_before = resource.getrusage(resource.RUSAGE_CHILDREN)

    try:
        result = subprocess.run(
            time_command + command,
            input=stdin,
            text=True,
            capture_output=True,
            preexec_fn=set_limit_preexec,
            timeout=time_limit,
            env=clean_env,
        )
        usage_after = resource.getrusage(resource.RUSAGE_CHILDREN)

        # Parse memory usage from /usr/bin/time output
        max_rss_kb = -1
        try:
            with open(time_output_path, "r") as f:
                for line in f:
                    if "Maximum resident set size" in line:
                        max_rss_kb = int(line.strip().split(":")[1].strip())
                        break
        except Exception as e:
            max_rss_kb = -1  # fallback if time output can't be read

        cpu_time = (usage_after.ru_utime + usage_after.ru_stime) - (usage_before.ru_utime + usage_before.ru_stime)

    except subprocess.TimeoutExpired:
        return core.util.execution_result.ExecutionResult(
            return_code=-1,
            stdout="",
            stderr="",
            time=time_limit,
            memory=-1,
            failure="Time Limit Exceeded"
        )
    except Exception as e:
        return core.util.execution_result.ExecutionResult(
            return_code=-1,
            stdout="",
            stderr=str(e),
            time=-1,
            memory=-1,
            failure="Runtime Error"
        )
    finally:
        os.remove(time_output_path)

    if result.returncode != 0:
        return core.util.execution_result.ExecutionResult(
            return_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            time=cpu_time,
            memory=max_rss_kb,
            failure="Runtime Error"
        )

    if cpu_time > time_limit:
        return core.util.execution_result.ExecutionResult(
            return_code=-1,
            stdout="",
            stderr="",
            time=time_limit,
            memory=max_rss_kb,
            failure="Time Limit Exceeded"
        )

    return core.util.execution_result.ExecutionResult(
        return_code=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
        time=cpu_time,
        memory=max_rss_kb,
        failure=None
    )
