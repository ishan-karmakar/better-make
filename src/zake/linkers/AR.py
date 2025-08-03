import os
import subprocess
import tempfile
import uuid
import linkers
import shutil
from step import PathStep
from . import _linkers as linkers

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
        return shutil.which("ar") is not None