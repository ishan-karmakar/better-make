import abc
from ..step import PathStep
import os
from ..dirs import CACHE_DIR
import hashlib
import json
from checksumdir import dirhash

class CompileStep(PathStep):
    def __init__(self, source):
        super().__init__()
        self.dependsOn(source)
        self.source = source
        self.flags = []
        self.include_dirs = []

    # Low level method to add arbitary flags
    def add_flags(self, *flags: str):
        self.flags.extend(flags)

    # Low level method to completely replace flags
    def override_flags(self, *flags: str):
        self.flags = list(flags)

    @abc.abstractmethod
    def execute(cmd):
        logging.info(f"Running {cmd}")
        return cmd

    # High level method to add include directories
    @abc.abstractmethod
    def add_include_dirs(self, *dirs: str):
        for dir in dirs:
            self.include_dirs.append(dir)

    def get_path(self):
        if not hasattr(self, "path"):
            self.path = os.path.join(CACHE_DIR, hashlib.sha256(json.dumps({
                'source': self.source.get_path(),
                'flags': self.flags,
                'include_hash': [dirhash(dir, 'sha256') for dir in self.include_dirs]
            }).encode(), usedforsecurity=False).hexdigest() + '.o')
        return self.path

class CompilerDetection(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def scan() -> bool:
        raise NotImplementedError
