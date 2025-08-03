import hashlib
import os
import subprocess

from ..dirs import CACHE_DIR
from ._compilers import *
from ..step import PathStep
from ..config import parser
from .._common import check_exec

parser.add_argument("--cpp-path", nargs="?", help="C++ executable path")

class Compiler(CompilerDetection):
    class Step(PathStep, CompileStep):
        def __init__(self, source: PathStep):
            super().__init__()
            self.source = source
            self.flags = []
        
        def execute(self):
            subprocess.run(["clang++", "-c", self.source.get_path(), "-o", self.path, *self.flags]).check_returncode()
        
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
        return check_exec(parser.parse_args().cpp_path, "clang++", "clang")