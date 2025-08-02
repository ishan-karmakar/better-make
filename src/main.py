import logging
import shutil

import compilers.GCC
import linkers.GCC
import compilers.clang
import linkers.clang
import compilers
import linkers
from step import Step, PathStep

KNOWN_COMPILERS = [
    compilers.GCC.Compiler,
    compilers.clang.Compiler
]

KNOWN_LINKERS = [
    linkers.GCC.Linker,
    linkers.clang.Linker
]

CompileStep: type[compilers.CompileStep] | None = None
LinkStep: type[linkers.LinkStep] | None = None

logging.basicConfig() 
logging.root.setLevel(logging.NOTSET)

commands = {
    "build": Step()
}

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

def scan_kits():
    global CompileStep, LinkStep
    for compiler in KNOWN_COMPILERS:
        if compiler.scan():
            CompileStep = compiler.CompileStep
            break

    for linker in KNOWN_LINKERS:
        if linker.scan():
            LinkStep = linker.LinkStep

init_project("toy-compiler")
scan_kits()
assert CompileStep and LinkStep
commands["build"].dependsOn(InstallFile("compiler", LinkStep(
    linkers.LinkType.Executable,
    CompileStep("main.cpp")
)))
commands["build"]()
