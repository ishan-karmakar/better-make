import os
import shutil
from ..dirs import OUT_DIR
from .path_step import PathStep


class InstallFile(PathStep):
    def __init__(self, name: str, file: PathStep):
        super().__init__()
        self.dependsOn(file)
        self.file = file
        self.path = os.path.join(OUT_DIR, name)
    
    def execute(self):
        shutil.copy(self.file.get_path(), self.path)

    def should_rerun(self) -> bool:
        return not os.path.exists(self.path)

    def get_path(self):
        return self.path