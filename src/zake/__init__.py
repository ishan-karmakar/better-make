from .step import Step

commands = {
    "build": Step()
}

# def register_command(name: str):
#     commands[name] = Step()
#     return commands[name]

# assert CompileStep
# assert LinkStep
# commands["build"].dependsOn(InstallFile("compiler", LinkStep(linkers.LinkType.Executable, CompileStep(FilePath("main.cpp")))))
# commands["build"]()
