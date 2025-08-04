import os
import subprocess
import tempfile
import uuid
from ..step import PathStep
from . import _linkers as linkers
from ..config import parser
from .. import _common as common

if not common.check_arg_exists("linker_path"):
    parser.add_argument("--linker-path", help="Linker path", nargs="?")

class Linker(linkers.LinkerDetection):
    class Step(PathStep, linkers.LinkStep):
        def __init__(self, link_type: linkers.LinkType, *inputs: PathStep):
            super().__init__()
            assert link_type == linkers.LinkType.StaticLibrary
            for inp in inputs:
                self.dependsOn(inp)
            self.inputs = inputs

        def execute(self):
            self.path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
            subprocess.run(["ar", "rcs", self.path, *(f.get_path() for f in self.inputs), *self.flags]).check_returncode()
        
        def get_path(self) -> str:
            return self.path

    @staticmethod
    def scan() -> bool:
        return common.check_exec(parser.parse_args().linker_path, "ar", "GNU ar")