import logging
import shutil
import sys
import binascii

import compilers.GCC
import linkers.GCC
import compilers.clang
import linkers.clang
import linkers.AR
import compilers
import linkers
from step import Step, PathStep, FilePath

KNOWN_COMPILERS = [
    compilers.GCC.Compiler,
    compilers.clang.Compiler
]

KNOWN_LINKERS = [
    linkers.GCC.Linker,
    linkers.clang.Linker,
    linkers.AR.Linker
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

def scan_kits():
    global CompileStep, LinkStep
    for compiler in KNOWN_COMPILERS:
        if compiler.scan():
            CompileStep = compiler.CompileStep
            break

    for linker in KNOWN_LINKERS:
        if linker.scan():
            LinkStep = linker.LinkStep
            break
    
def register_command(name: str):
    commands[name] = Step()
    return commands[name]

scan_kits()

assert CompileStep
assert LinkStep
commands["build"].dependsOn(LinkStep(CompileStep(FilePath("main.cpp"))))
# commands["build"].dependsOn(InstallFile("compiler", LinkStep(CompileStep(FilePath("main.cpp")))))
commands["build"]()
