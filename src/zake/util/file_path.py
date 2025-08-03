import binascii
import hashlib
import os
import shutil
from zake.dirs import CACHE_DIR
from zake.step import PathStep

class FilePath(PathStep):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.output = os.path.join(CACHE_DIR, hashlib.sha256(self.filename.encode(), usedforsecurity=False).hexdigest() + os.path.splitext(filename)[1])

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