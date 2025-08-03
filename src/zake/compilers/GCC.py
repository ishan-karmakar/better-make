import hashlib
import compilers
import shutil
import subprocess
import os
from dirs import CACHE_DIR
from step import PathStep

class Compiler(compilers.CompilerDetection):
    class CompileStep(PathStep, compilers.CompileStep):
        def __init__(self, source: PathStep):
            super().__init__()
            self.dependsOn(source)
            self.source = source
            self.flags = []
        
        def execute(self):
            subprocess.run(["g++", "-c", self.source.get_path(), "-o", self.path, *self.flags]).check_returncode()
        
        def should_rerun(self):
            self.path = self.get_output()
            return not os.path.isfile(self.path)

        def get_output(self):
            return os.path.join(CACHE_DIR, hashlib.sha256("".join([self.source.get_path(), *self.flags]).encode(), usedforsecurity=False).hexdigest() + ".o")

        def add_include_dirs(self, *dirs: str):
            for dir in dirs:
                self.add_flags("-I" + dir)
        
        def get_path(self):
            return self.path

    @staticmethod
    def scan() -> bool:
        return shutil.which("g++") is not None
