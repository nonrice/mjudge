import os
from core.util.limited_subprocess import limited_subprocess

# Idea is: benchmark program is expected to run at x secs, but runs on y secs in the environemtn
# So multiply the time limit by y/x to set a limit at "x secs" for the program
def get_time_multiplier(command, expected_time):
    result = limited_subprocess(command, stdin=None, time_limit=expected_time + 10, memory_limit=1024)
    
    if result.failure:
        raise RuntimeError(f"Calibration failed: {result}")
    
    return result.time / expected_time if expected_time > 0 else 1.0


# cpp is roughly 5x as fast as py. So we want 5e8 in 2s meaning we'll calibrate with 1e8 python operations
# Ideally the calibration would be 5e8 cpp ops at 2s but this is simpler
def get_time_multiplier_python3_1e8_2000():
    command = ["python3", "-c", "total=0\nfor i in range(10_000_000):\n a=i%10\n b=i%7\n c=(a*b+3)%13\n total+=c if c<5 else -(c-5)\nprint(total)"]
    return get_time_multiplier(command, 2.0)


