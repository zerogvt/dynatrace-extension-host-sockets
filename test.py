import subprocess
import re
import platform

if platform.system() == "Windows":
    result = subprocess.run('netstat -ano',
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            check=False)
    records = {}
    lines = result.stdout.strip().split("\n")
    for i, line in enumerate(lines):
        sline = line.lstrip()
        parts = re.split(r"\s+", sline)
        if len(parts)<2 or parts[0] not in ["TCP", "UDP"]:
            continue
        records[i] = sline
    print(records)
