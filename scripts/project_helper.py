"""
Define functions as project scripts that can be run via pyproject.toml
"""
import sys
import subprocess as sp
from zoom_report import Config


def run_analyzer() -> None:
    """
    Run mypy static type checker
    """
    path = Config.base_dir() / Config.package()
    try:
        sp.run(f"mypy {path}", check=True, shell=True)
    except sp.CalledProcessError as error:
        print(error)
        sys.exit(1)


def run_linter() -> None:
    """
    Run pylint static code analysis
    """
    path = Config.base_dir() / Config.package()
    try:
        sp.run(f"pylint {path}", check=True, shell=True)
    except sp.CalledProcessError as error:
        print(error)
        sys.exit(1)


def run_tests() -> None:
    """
    Run unit tests with pytest
    """
    try:
        sp.run("pytest --capture=tee-sys", check=True, shell=True)
    except sp.CalledProcessError as error:
        print(error)
        sys.exit(1)
