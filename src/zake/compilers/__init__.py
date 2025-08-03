from . import GCC, clang

KNOWN_COMPILERS = [
    GCC.Compiler,
    clang.Compiler
]

Step = None

def scan_compilers():
    global Step
    for compiler in KNOWN_COMPILERS:
        if compiler.scan():
            Step = compiler.Step
            break
    assert Step