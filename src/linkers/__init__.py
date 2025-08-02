import abc
from enum import Enum


class LinkType(Enum):
    Executable = 1
    SharedLibrary = 2
    StaticLibrary = 3

class LinkStep(abc.ABC):
    def __init__(self):
        self.flags = []

    def add_flags(self, *flags: str):
        self.flags.extend(flags)

    def override_flags(self, *flags: str):
        self.flags = list(flags)

class LinkerDetection(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def scan() -> bool:
        raise NotImplementedError