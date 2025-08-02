import logging
import os
import shutil
import subprocess
import tempfile
import uuid
import compilers
from step import PathStep

class Compiler(compilers.CompilerDetection):
    class CompileStep(PathStep, compilers.CompileStep):
        def __init__(self, source: PathStep):
            super().__init__()
            self.source = source
            self.flags = []
        
        def execute(self):
            path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
            subprocess.run(["clang++", "-c", self.source.get_path(), *self.flags, "-o", path]).check_returncode()
            self.path = path
            logging.info(f"Compiled {self.source.get_path()}")

        def add_include_dirs(self, *dirs: str):
            for dir in dirs:
                self.flags.append("-I" + dir)
        
        def get_path(self):
            return self.path
    
    @staticmethod
    def scan() -> bool:
        return shutil.which("clang++") is not None