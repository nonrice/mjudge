import core.program.program_base
from core.util.limited_subprocess import limited_subprocess
import subprocess
import os
class CppProgram(core.program.program_base.ProgramBase):
    """
    C++ program type.
    Provides methods for compiling and executing C++ programs.
    """

    def compile(self):
        self.exec_path = os.path.splitext(self.source_path)[0]
        compile_command = ["g++", "-std=c++17", self.source_path, "-o", self.exec_path]
        return limited_subprocess(compile_command, stdin=None, time_limit=20, memory_limit=1024)

    def execute(self, stdin: str, args: list[str] = None, time_limit: int = 2, memory_limit: int = 256, become_nobody: bool = False):
        execute_command = [self.exec_path]
        if args is not None:
            execute_command.extend(args)
        return limited_subprocess(execute_command, stdin=stdin, time_limit=time_limit, memory_limit=memory_limit, become_nobody=become_nobody)