import hashlib
import logging
import os
import subprocess
import json
from ..dirs import CACHE_DIR
from ..step import PathStep
from . import _linkers as linkers
from .. import _common as common
from ..config import parser

if not common.check_arg_exists("linker_path"):
    parser.add_argument("--linker-path", help="Linker path", nargs="?")

class Linker(linkers.LinkerDetection):
    class Step(PathStep, linkers.LinkStep):
        def __init__(self, link_type: linkers.LinkType, *inputs: PathStep):
            super().__init__()
            for inp in inputs:
                self.dependsOn(inp)
            self.inputs = inputs
            self.flags = []
            self.link_type = link_type
            if link_type == linkers.LinkType.SharedLibrary:
                self.flags.extend(("-shared", "-fPIC"))
            elif link_type == linkers.LinkType.StaticLibrary:
                logging.error("G++ does not support static library linking. Use the AR linker instead")
        
        def link_library(self, name: str):
            self.add_flags("-l" + name)
        
        def execute(self):
            self.path = self.get_output()
            subprocess.run(["g++", *(f.get_path() for f in self.inputs), "-o", self.path, *self.flags]).check_returncode()
        
        def should_rerun(self) -> bool:
            self.path = self.get_output()
            return not os.path.isfile(self.path)
        
        def get_output(self):
            return os.path.join(CACHE_DIR, hashlib.sha256(json.dumps({
                "sources": [f.get_path() for f in self.inputs],
                "flags": self.flags
            }).encode(), usedforsecurity=False).hexdigest())

        def get_path(self):
            return self.path

    @staticmethod
    def scan() -> bool:
        return common.check_exec(parser.parse_args().linker_path, "g++", "g++")
