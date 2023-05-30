import subprocess
import sys

subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["idna", "os", "pygame"]
options = {
    'build_exe': {
        'packages': packages
    },
}

setup(
    name = "Aspen Davis",
    options = options,
    version = "0.1",
    description = "A basic multimedia digital library",
    executables = executables
)
