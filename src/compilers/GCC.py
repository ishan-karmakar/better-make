import compilers
import shutil
import subprocess
import tempfile
import uuid
import logging
import os
from step import PathStep

class Compiler(compilers.CompilerDetection):
    class CompileStep(PathStep, compilers.CompileStep):
        def __init__(self, filename: str):
            super().__init__()
            self.filename = filename
            self.flags = []
        
        def execute(self):
            self.path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
            subprocess.run(["g++", "-c", self.filename, "-o", self.path, *self.flags]).check_returncode()
            logging.info(f"Compiled {self.filename}")
        
        def add_include_dirs(self, *dirs: str):
            for dir in dirs:
                self.add_flags("-I" + dir)
        
        def get_path(self):
            return self.path

    @staticmethod
    def scan() -> bool:
        return shutil.which("g++") is not None
