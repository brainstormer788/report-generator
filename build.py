import os
import shutil
import subprocess
import sys

MAIN_FILE = "ReportGenerator.py"
EXE_NAME = "ReportGenerator"


def clean_old_build():
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    spec_file = f"{EXE_NAME}.spec"

    if os.path.exists(spec_file):
        os.remove(spec_file)


def build_exe():
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--name",
        EXE_NAME,
        MAIN_FILE
    ]

    subprocess.check_call(cmd)


if __name__ == "__main__":
    clean_old_build()
    build_exe()