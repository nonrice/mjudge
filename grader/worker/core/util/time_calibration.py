import os
from core.util.limited_subprocess import limited_subprocess

def get_time_multiplier(command, expected_time):
    """
    Runs a command to get the time multiplier for calibration.
    
    Args:
        command (list): The command to run.
        expected_time (float): The expected time in seconds.
    
    Returns:
        float: The time multiplier.
    """
    result = limited_subprocess(command, stdin=None, time_limit=expected_time + 10, memory_limit=1024)
    
    if result.failure:
        raise RuntimeError(f"Calibration failed: {result}")
    
    return result.time / expected_time if expected_time > 0 else 1.0


# cpp is roughly 5x as fast as py. So we want 5e8 in 2s so we'll calibrate with 1e8 python operations
def get_time_multiplier_python3_1e8_2000():
    command = ["python3", "-c", "total=0\nfor i in range(10_000_000):\n a=i%10\n b=i%7\n c=(a*b+3)%13\n total+=c if c<5 else -(c-5)\nprint(total)"]
    return get_time_multiplier(command, 2.0)

# def get_time_multiplier_python3_1e8_2000():
#     code = (
#         "arr = [0]*1000; total = 0; "
#         "for i in range(int(1e8)): "
#         " index = i % 1000; arr[index] = (arr[index] + i) % 1000; "
#         " val = arr[index]; total = total + val if val < 500 else total - val; "
#         "print(total)"
#     )
#     command = ["python3", "-c", code]
#     return get_time_multiplier(command, 2.0)

