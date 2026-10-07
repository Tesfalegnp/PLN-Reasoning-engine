#!/usr/bin/env python3
"""
agri-pln-metta: Test Runner and Orchestrator
Discovers and executes all MeTTa test suites and verifies output.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def find_metta_executable():
    # 1. System PATH
    import shutil
    p = shutil.which("metta")
    if p:
        return p
    # 2. Known local virtualenv paths
    candidates = [
        "/home/hope/Projects/pln_engin_project/.venv-metta/bin/metta",
        str(Path.home() / ".cargo/bin/metta"),
        str(Path.home() / ".local/bin/metta"),
    ]
    for c in candidates:
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return "metta"

def run_metta_test(metta_bin, test_file, project_root):
    rel_path = os.path.relpath(test_file, project_root)
    # Run from the test file's directory so relative modules resolve correctly
    cwd = os.path.dirname(test_file)
    cmd = [metta_bin, os.path.basename(test_file)]
    
    start_time = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        duration = time.time() - start_time
        
        stdout = proc.stdout
        stderr = proc.stderr
        
        has_error = (proc.returncode != 0) or ("(Error" in stdout) or ("Exception" in stdout) or ("Failed to resolve" in stdout)
        
        return {
            "file": rel_path,
            "passed": not has_error,
            "duration": duration,
            "stdout": stdout,
            "stderr": stderr,
            "returncode": proc.returncode
        }
    except Exception as e:
        return {
            "file": rel_path,
            "passed": False,
            "duration": time.time() - start_time,
            "stdout": "",
            "stderr": str(e),
            "returncode": -1
        }

def main():
    project_root = Path(__file__).parent.resolve()
    metta_bin = find_metta_executable()
    
    print("=" * 80)
    print(" agri-pln-metta: Automated Test Runner")
    print(f" MeTTa Runtime: {metta_bin}")
    print(f" Workspace Root: {project_root}")
    print("=" * 80)
    
    test_dir = project_root / "tests"
    test_files = sorted(list(test_dir.glob("test_*.metta")))
    
    if not test_files:
        print(f"[-] No test files found in {test_dir}")
        sys.exit(1)
        
    passed_count = 0
    failed_count = 0
    results = []
    
    for tf in test_files:
        res = run_metta_test(metta_bin, str(tf), str(project_root))
        results.append(res)
        if res["passed"]:
            passed_count += 1
            status = "\033[92mPASS\033[0m" if sys.stdout.isatty() else "PASS"
        else:
            failed_count += 1
            status = "\033[91mFAIL\033[0m" if sys.stdout.isatty() else "FAIL"
            
        print(f" [{status}] {res['file']} ({res['duration']:.2f}s)")
        if not res["passed"]:
            print("   --- Output ---")
            if res["stdout"]:
                print(f"   STDOUT: {res['stdout'][:500]}")
            if res["stderr"]:
                print(f"   STDERR: {res['stderr'][:500]}")
            print("   --------------")
            
    print("=" * 80)
    print(f"Summary: {passed_count} passed, {failed_count} failed out of {len(test_files)} total test suites.")
    print("=" * 80)
    
    if failed_count > 0:
        sys.exit(1)
    else:
        print("All test suites passed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
