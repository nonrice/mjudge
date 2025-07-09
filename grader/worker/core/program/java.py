import core.program.program_base
from core.util.limited_subprocess import limited_subprocess
import subprocess
import os
import shutil
class JavaProgram(core.program.program_base.ProgramBase):
    def compile(self):
        self.prog_path = os.path.join(os.path.dirname(self.source_path), "Main.java")
        self.class_path = os.path.join(os.path.dirname(self.source_path), "Main.class")
        shutil.copy(self.source_path, self.prog_path)
        compile_command = ["javac", self.prog_path]
        return limited_subprocess(compile_command, stdin=None, time_limit=20, memory_limit=1024*10) # javac/JVM allocates a lot of virtual memory

    def execute(self, stdin: str, args: list[str] = None, time_limit: int = 2, memory_limit: int = 256, become_nobody: bool = False):
        execute_command = [
            "java",
            f"-Xmx{memory_limit}m", # Bc virtual mem alloc, you can't limit java with rlimit. But you can at jvm level
            "-Xms16m",
            "-XX:MaxMetaspaceSize=64m",
            "-XX:ReservedCodeCacheSize=32m",
            "-XX:+UseSerialGC",
            "-cp",
            os.path.dirname(self.class_path),
            "Main"
        ]
        if args is not None:
            execute_command.extend(args)
        return limited_subprocess(execute_command, stdin=stdin, time_limit=time_limit, memory_limit=1024*10, become_nobody=become_nobody)