import logging
from step import Step
import compilers

# KNOWN_LINKERS = [
#     linkers.GCC.Linker,
#     linkers.clang.Linker,
#     linkers.AR.Linker
# ]

# LinkStep: type[linkers.LinkStep] | None = None

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)

commands = {
    "build": Step()
}

# def scan_kits():
#     global LinkStep
#     for linker in KNOWN_LINKERS:
#         if linker.scan():
#             LinkStep = linker.LinkStep
#             break
    
# def register_command(name: str):
#     commands[name] = Step()
#     return commands[name]
compilers.scan_compilers()

# assert CompileStep
# assert LinkStep
# commands["build"].dependsOn(InstallFile("compiler", LinkStep(linkers.LinkType.Executable, CompileStep(FilePath("main.cpp")))))
# commands["build"]()
