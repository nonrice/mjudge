import os
from core.util.execution_result import ExecutionResult

class ProgramBase:
    def __init__(self, source_path: os.PathLike):
        self.source_path = source_path

    def compile(self)->ExecutionResult:
        raise NotImplementedError("Subclasses must implement this method.")
    
    def execute(self, stdin: str, args: list[str] = None, time_limit: int = 1, memory_limit: int=256, become_nobody: bool=False)->ExecutionResult:
        # just pass become_nobody directly into limited_subprocess
        raise NotImplementedError("Subclasses must implement this method.")
    