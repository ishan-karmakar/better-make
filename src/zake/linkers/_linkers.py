import abc
from enum import Enum
import json
import os
from ..dirs import CACHE_DIR
import hashlib
from ..step import PathStep
import logging

class LinkType(Enum):
    Executable = 1
    SharedLibrary = 2
    StaticLibrary = 3

class LinkStep(PathStep):
    def __init__(self, *inputs: PathStep):
        super().__init__()
        for inp in inputs:
            self.dependsOn(inp)
        self.flags = []
        self.inputs = inputs

    @abc.abstractmethod
    def execute(cmd):
        logging.info(f"Running {cmd}")
        return cmd

    def should_rerun(self):
        rerun = not os.path.isfile(self.get_path())
        if rerun:
            logging.debug(f"{self.get_path()} does not exist, must rerun this task")
        else:
            logging.debug(f"{self.get_path()} exists, no need to rerun this task")
        return rerun

    def add_flags(self, *flags: str):
        self.flags.extend(flags)

    def override_flags(self, *flags: str):
        self.flags = list(flags)

    def get_path(self):
        if not hasattr(self, "path"):
            self.path = os.path.join(CACHE_DIR, hashlib.sha256(json.dumps({
                'inputs': [s.get_path() for s in self.inputs],
                'flags': self.flags
            }).encode()).hexdigest())
        return self.path

class LinkerDetection(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def scan() -> bool:
        raise NotImplementedError
