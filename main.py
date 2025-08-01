import subprocess
from enum import Enum
import abc
import logging
import uuid
import os
import tempfile
import shutil

KNOWN_CXX_COMPILERS = ("g++",)
KNOWN_C_COMPILERS = ("gcc",)

logging.basicConfig() 
logging.root.setLevel(logging.NOTSET)

class Languages(Enum):
    C = 1
    CPP = 2

class Step:
    def __init__(self):
        self.dependencies = []
        self.run = False

    def dependsOn(self, step):
        self.dependencies.append(step)
        return self
    
    def execute(self):
        pass

    def __call__(self):
        for dep in self.dependencies:
            dep()
        if not self.run:
            self.execute()
            self.run = True

class PathStep(Step):
    @abc.abstractmethod
    def get_path(self) -> str:
        pass

commands = {
    "build": Step()
}

class Compile(PathStep):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.flags = []

    def execute(self):
        path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        subprocess.run(["g++", "-c", self.filename, *self.flags, "-o", path]).check_returncode()
        self.path = path
        logging.info(f"Compiled {self.filename}")

    def add_flags(self, *flags: str):
        self.flags.extend(flags)

    def override_flags(self, *flags: str):
        self.flags = list(flags)

    def add_include_dirs(self, *dirs: str):
        for dir in dirs:
            self.flags.append("-I" + dir)
    
    def get_path(self):
        return self.path

class Link(PathStep):
    class Type(Enum):
        Executable = 1
        Library = 2

    def __init__(self, link_type: Type, *inputs: PathStep):
        super().__init__()
        for inp in inputs:
            self.dependsOn(inp)
        self.inputs = inputs
        self.flags = []

    def link_library(self, name: str):
        self.add_flags("-l" + name)

    def add_flags(self, *flags: str):
        self.flags.extend(flags)

    def override_flags(self, *flags: str):
        self.flags = list(flags)

    def execute(self):
        path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        subprocess.run(["g++", *(f.get_path() for f in self.inputs), "-o", path, *self.flags])
        self.path = path
    
    def get_path(self):
        return self.path

class InstallFile(PathStep):
    def __init__(self, name: str, file: PathStep):
        super().__init__()
        self.dependsOn(file)
        self.file = file
        self.path = name
    
    def execute(self):
        shutil.copy(self.file.get_path(), self.path)
    
    def get_path(self):
        return self.path

def init_project(name: str):
    pass

def scan_compilers():
    pass

init_project("toy-compiler")
commands["build"].dependsOn(InstallFile("compiler", Link(
    Link.Type.Executable,
    Compile("main.cpp")
)))
commands["build"]()
