from . import GCC, clang, AR
from ._linkers import LinkType

KNOWN_LINKERS = [
    GCC.Linker,
    clang.Linker,
    AR.Linker
]

Step = None

def scan_linkers():
    global Step
    for linker in KNOWN_LINKERS:
        if linker.scan():
            Step = linker.Step
            break