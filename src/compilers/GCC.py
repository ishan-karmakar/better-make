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
            self.path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
            self.cmdline = [
                "g++",
                "-c",
                self.filename,
                "-o",
                self.path
            ]
        
        def execute(self):
            subprocess.run(self.cmdline).check_returncode()
            logging.info(f"Compiled {self.filename}")
        
        def add_include_dirs(self, *dirs: str):
            for dir in dirs:
                self.cmdline.append("-I" + dir)
        
        def get_path(self):
            return self.path

    @staticmethod
    def scan() -> bool:
        return shutil.which("g++") is not None
