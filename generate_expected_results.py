#!/usr/bin/env python3
"""A utility script that runs every test program with the system compiler and records its return code and output"""

import json
from pathlib import Path
import subprocess
from typing import Any

results : dict[str, dict[str, Any]]= {}

ROOT_DIR = Path(__file__).parent

# iterate over all valid programs
for prog in ROOT_DIR.glob("chapter*/valid/**/*.c"):
    if "libraries" in prog.parts:
        continue # TODO
    # compile the program
    # TODO this is copied from TestBase
    path_str = str(prog)
    try:
        subprocess.run(["gcc", "-Wno-incompatible-library-redeclaration"] + [path_str] + ["-o", prog.stem],
                        check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(e.stderr) from e


    exe = Path.joinpath(ROOT_DIR, prog.stem)
    # run the program
    try:
        result = subprocess.run([exe], check=False, text=True, capture_output=True)
        if result.stderr:
            raise RuntimeError(result.stderr)
        
        result_dict: dict[str, Any] = {"return_code": result.returncode}
        if result.stdout:
            result_dict["stdout"] = result.stdout
        
        results[path_str] = result_dict
    finally:
        # delete executable
        Path.unlink(exe)


with open("expected_results.json", "w") as f:
    json.dump(results, f)