import abc
import binascii
import hashlib
import os
import shutil

class Step:
    def __init__(self):
        self.dependencies = []
        self.run = False
        self.changed = False

    def dependsOn(self, step):
        self.dependencies.append(step)
        return self
    
    def execute(self):
        pass

    # Child steps should implement this for caching.
    # For example, a compiler step would look at the update time of the input file and check if it is past the created/update time of output file
    # Child steps don't have to worry about dependencies. That is handled by the generic Step class
    def should_rerun(self) -> bool:
        return False

    def __call__(self):
        if self.run:
            return
        
        for dep in self.dependencies:
            dep()

        # We consider this task changed if any of the dependencies had to rerun or step itself needs to rerun
        self.changed = any(dep.changed for dep in self.dependencies) or self.should_rerun()
        if self.changed:
            self.execute()
            self.run = True

# Specialization of a Step that outputs a file
class PathStep(Step):
    @abc.abstractmethod
    def get_path(self) -> str:
        pass

class FilePath(PathStep):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.output = hashlib.sha256(self.filename.encode(), usedforsecurity=False).hexdigest() + os.path.splitext(filename)[1]

    def execute(self):
        shutil.copy(self.filename, self.output)

    def should_rerun(self) -> bool:
        try:
            with open(self.output, "rb") as outf:
                out_checksum = binascii.crc32(outf.read())
        except FileNotFoundError:
            return True
        
        with open(self.filename, "rb") as inf:
            return not binascii.crc32(inf.read()) == out_checksum

    def get_path(self) -> str:
        return self.output