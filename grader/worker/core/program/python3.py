import core.program.program_base
from core.util.limited_subprocess import limited_subprocess
from core.util.execution_result import ExecutionResult

class Python3Program(core.program.program_base.ProgramBase):
    def compile(self):
        return ExecutionResult(
            return_code=0,
            stdout="",
            stderr="",
            time=0,
            memory=0,
            failure=None
        )

    def execute(self, stdin: str, args: list[str] = None, time_limit: int = 2, memory_limit: int = 256):
        execute_command = ["python3", self.source_path]
        if args is not None:
            execute_command.extend(args)
        print("Executing command:", execute_command)
        return limited_subprocess(execute_command, stdin=stdin, time_limit=time_limit, memory_limit=memory_limit)