import sys
import subprocess as sp
from zoom_report import Config


def run_analyzer() -> None:
    path = Config.base_dir() / Config.package()
    try:
        sp.run(f'mypy {path}', check=True, shell=True)
    except sp.CalledProcessError as error:
        print(error)
        sys.exit(1)
