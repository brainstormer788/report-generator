import os
import shutil
import subprocess
import sys

MAIN_FILE = "ReportGenerator.py"
EXE_NAME = "ReportGenerator"


def clean():
    """
    Remove previous build artifacts
    """

    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    spec_file = f"{EXE_NAME}.spec"

    if os.path.exists(spec_file):
        os.remove(spec_file)


def install_dependencies():
    """
    Install required packages
    """

    packages = [
        "pyinstaller",
        "pandas",
        "openpyxl",
        "odfpy"
    ]

    for package in packages:
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            package
        ])


def build_exe():
    """
    Build Windows executable
    """

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",

        "--onefile",
        "--windowed",
        "--clean",

        "--hidden-import=odf.opendocument",
        "--hidden-import=odf.element",
        "--hidden-import=odf.table",

        "--name",
        EXE_NAME,

        MAIN_FILE
    ]

    subprocess.check_call(cmd)


def show_result():

    exe_path = os.path.join(
        "dist",
        f"{EXE_NAME}.exe"
    )

    print("\n" + "=" * 50)

    if os.path.exists(exe_path):
        print("BUILD SUCCESSFUL")
        print(f"Executable: {exe_path}")
    else:
        print("BUILD FINISHED")
        print("Check dist folder")

    print("=" * 50)


def main():

    if not os.path.exists(MAIN_FILE):
        raise FileNotFoundError(
            f"{MAIN_FILE} not found"
        )

    clean()

    install_dependencies()

    build_exe()

    show_result()


if __name__ == "__main__":
    main()