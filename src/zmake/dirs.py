import os
import sys

PROJECT_DIR = sys.path[0]
CACHE_DIR = os.path.join(PROJECT_DIR, ".cache")
OUT_DIR = os.path.join(PROJECT_DIR, "build")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
