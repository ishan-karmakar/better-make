from .step import Step
from . import config

commands = {
    "build": Step(),
    "clean": Step()
}

def register_command(name: str):
    commands[name] = Step()
    return commands[name]