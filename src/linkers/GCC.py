import os
import shutil
import subprocess
import tempfile
import uuid
import linkers
from step import PathStep

class Linker(linkers.LinkerDetection):
    class LinkStep(PathStep, linkers.LinkStep):
        def __init__(self, link_type: linkers.LinkType, *inputs: PathStep):
            super().__init__()
            for inp in inputs:
                self.dependsOn(inp)
            self.inputs = inputs
            self.flags = []
        
        def link_library(self, name: str):
            self.add_flags("-l" + name)
        
        def execute(self):
            path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
            subprocess.run(["g++", *(f.get_path() for f in self.inputs), "-o", path, *self.flags])
            self.path = path
        
        def get_path(self):
            return self.path

    @staticmethod
    def scan() -> bool:
        return shutil.which("g++") is not None