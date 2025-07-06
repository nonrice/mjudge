import os
from core.util.execution_result import ExecutionResult

class ProgramBase:
    """
    Base class for all program types.
    Provides a common interface for program execution and result retrieval.
    """

    def __init__(self, source_path: os.PathLike):
        self.source_path = source_path

    def compile(self)->ExecutionResult:
        """
        Execute the program with the given arguments.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    def execute(self, stdin: str, args: list[str] = None)->ExecutionResult:
        """
        Execute the program with the given arguments.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    