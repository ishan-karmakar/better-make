import shutil
import subprocess

def check_exec(arg, exe_name: str, text: str):
    path = shutil.which(arg or exe_name)
    if not path:
        return False
    return text in subprocess.run([path, "--version"], capture_output=True).stdout.decode()