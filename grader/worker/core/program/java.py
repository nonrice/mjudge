import core.program.program_base
from core.util.limited_subprocess import limited_subprocess
import subprocess
import os
class JavaProgram(core.program.program_base.ProgramBase):
    def compile(self):
        compile_command = ["javac", self.source_path]
        return limited_subprocess(compile_command, stdin=None, time_limit=20, memory_limit=1024)

    def execute(self, stdin: str, args: list[str] = None, time_limit: int = 2, memory_limit: int = 256):
        execute_command = ["java", "Main"]
        if args is not None:
            execute_command.extend(args)
        return limited_subprocess(execute_command, stdin=stdin, time_limit=time_limit, memory_limit=memory_limit)