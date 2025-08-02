import hashlib
import compilers
import shutil
import subprocess
import os
from step import PathStep

class Compiler(compilers.CompilerDetection):
    class CompileStep(PathStep, compilers.CompileStep):
        def __init__(self, source: PathStep):
            super().__init__()
            self.dependsOn(source)
            self.source = source
            self.flags = []
        
        def execute(self):
            self.path = self.get_output()
            subprocess.run(["g++", "-c", self.source.get_path(), "-o", self.path, *self.flags]).check_returncode()
        
        def should_rerun(self):
            return not os.path.isfile(self.get_output())

        def get_output(self):
            return hashlib.sha256("".join([self.source.get_path(), *self.flags]).encode(), usedforsecurity=False).hexdigest() + ".o"

        def add_include_dirs(self, *dirs: str):
            for dir in dirs:
                self.add_flags("-I" + dir)
        
        def get_path(self):
            return self.path

    @staticmethod
    def scan() -> bool:
        return shutil.which("g++") is not None
