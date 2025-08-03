import logging
from step import Step
import compilers, linkers

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)

commands = {
    "build": Step()
}

# def register_command(name: str):
#     commands[name] = Step()
#     return commands[name]
compilers.scan_compilers()
linkers.scan_linkers()

# assert CompileStep
# assert LinkStep
# commands["build"].dependsOn(InstallFile("compiler", LinkStep(linkers.LinkType.Executable, CompileStep(FilePath("main.cpp")))))
# commands["build"]()
