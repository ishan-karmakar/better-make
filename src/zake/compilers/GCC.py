import hashlib
import subprocess
import os
import json
import logging
from checksumdir import dirhash
from ..dirs import CACHE_DIR
from ..step import PathStep
from ._compilers import *
from ..config import parser
from .. import _common as common

if not common.check_arg_exists("cpp_path"):
    parser.add_argument("--cpp-path", nargs="?", help="C++ executable path")

class Compiler(CompilerDetection):
    class Step(CompileStep):
        def __init__(self, source: PathStep):
            super().__init__(source)
            self.flags = []
            self.include_dirs = []

        def execute(self):
            subprocess.run(CompileStep.execute(["g++", "-c", self.source.get_path(), "-o", self.get_path(), *self.flags, *('-I' + dir for dir in self.include_dirs)])).check_returncode()
        
        def should_rerun(self):
            rerun = not os.path.isfile(self.get_path())
            if rerun:
                logging.debug(f"{self.get_path()} doesn't exist, must rerun this task")
            else:
                logging.debug(f"{self.get_path()} exists, no need to rerun this task")
            return rerun

    @staticmethod
    def scan() -> bool:
        return common.check_exec(parser.parse_args().cpp_path, "g++", "g++")
