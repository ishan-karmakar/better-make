import logging
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
            if link_type == linkers.LinkType.SharedLibrary:
                self.flags.extend(("-shared", "-fPIC"))
            elif link_type == linkers.LinkType.StaticLibrary:
                logging.error("Static library linking is not supported with Clang. Use the AR linker instead")
        
        def link_library(self, name: str):
            self.add_flags("-l" + name)
        
        def execute(self):
            path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
            subprocess.run(["clang++", *(f.get_path() for f in self.inputs), "-o", path, *self.flags]).check_returncode()
            self.path = path
        
        def get_path(self):
            return self.path
    
    @staticmethod
    def scan() -> bool:
        return shutil.which("clang++") is not None