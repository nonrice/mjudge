import core.program.program_base

class Python3Program(core.program.program_base.ProgramBase):
    """
    Python 3 program type.
    Provides methods for compiling and executing C++ programs.
    """

    def compile(self):
        return 0, "", ""

    def execute(self, stdin: str, args: list[str] = None):
        import subprocess
        execute_command = ["python3", self.source_path]
        if args is not None:
            execute_command.extend(args)
        result = subprocess.run(execute_command, input=stdin, text=True, capture_output=True)
        return result.returncode, result.stdout, result.stderr