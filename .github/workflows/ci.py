from glob import glob
import subprocess
from pathlib import Path

for pyfile in glob("*.py"):
    subp = subprocess.run(["python3",pyfile],capture_output=True)
    p = Path(pyfile)
    with open(p.stem,"wb+") as f:
        f.write(subp.stdout)
        print(subp.stderr)
