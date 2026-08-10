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
    if subp.returncode != 0:
        success = False
        print(f"Error executing file: {pyfile} (exit {subp.returncode})", file=sys.stderr)
        if subp.stderr:
            print(subp.stderr.decode(), file=sys.stderr)
        if subp.stdout:
            print(subp.stdout.decode(), file=sys.stderr)
        continue
    with open(p.stem, "wb+") as f:
        f.write(subp.stdout)
    if subp.stderr:
        # Generators may log warnings on stderr; surface them but keep success
        # tied to exit code (the contract for "did this script work?").
        print(f"stderr from {pyfile}:", file=sys.stderr)
        print(subp.stderr.decode(), file=sys.stderr)
if not success:
    sys.exit(1)
