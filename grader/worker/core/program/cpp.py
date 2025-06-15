import program_base

class CppProgram(program_base.ProgramBase):
    """
    C++ program type.
    Provides methods for compiling and executing C++ programs.
    """

    def compile(self):
        import subprocess
        compile_command = ["g++", self.source_path, "-o", self.source_filename.replace('.cpp', '')]
        result = subprocess.run(compile_command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Compilation failed: {result.stderr}")

    def execute(self, stdin: str):
        import subprocess
        execute_command = [self.source_filename.replace('.cpp', '')]
        result = subprocess.run(execute_command, input=stdin, text=True, capture_output=True)
        return result.stdout