import abc
from enum import Enum

class CompileStep(abc.ABC):
    def __init__(self):
        self.flags = []

    # Low level method to add arbitary flags
    def add_flags(self, *flags: str):
        self.flags.extend(flags)

    # Low level method to completely replace flags
    def override_flags(self, *flags: str):
        self.flags = list(flags)

    # High level method to add include directories
    @abc.abstractmethod
    def add_include_dirs(self, *dirs: str):
        raise NotImplementedError

class CompilerDetection(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def scan() -> bool:
        raise NotImplementedError
