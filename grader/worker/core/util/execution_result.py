class ExecutionResult:
    def __init__(self, return_code: int, stdout: str, stderr: str, time: float, memory: int, failure: str = None):
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        self.time = time
        self.memory = memory
        self.failure = failure

    def is_successful(self) -> bool:
        return self.return_code == 0 and self.failure is None

    def __repr__(self):
        return (f"ExecutionResult(returncode={self.return_code}, "
                f"time={self.time}, memory={self.memory}, "
                f"failure={self.failure}), "
                f"stdout={self.stdout!r}, stderr={self.stderr!r}"
                )
