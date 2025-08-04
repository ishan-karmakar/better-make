import shutil
import subprocess
from ..config import parser

def check_exec(arg, exe_name: str, text: str):
    path = shutil.which(arg or exe_name)
    if not path:
        return False
    return text in subprocess.run([path, "--version"], capture_output=True).stdout.decode()

def check_arg_exists(arg: str) -> bool:
    return arg in (action.dest for action in parser._actions)
