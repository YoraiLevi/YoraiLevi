import sys
from glob import glob
import subprocess
from pathlib import Path
import platform
py_exec = "py.exe" if platform.system() == "Windows" else "python3"
success = True
for pyfile in glob("*.py"):
    subp = subprocess.run([py_exec, pyfile], capture_output=True)
    p = Path(pyfile)
    with open(p.stem, "wb+") as f:
        f.write(subp.stdout)
        if subp.stderr:
            success = False
            print(f"Error executing file: {pyfile}", file=sys.stderr)
            print(subp.stderr.decode(), file=sys.stderr)
if not success:
    sys.exit(1)
