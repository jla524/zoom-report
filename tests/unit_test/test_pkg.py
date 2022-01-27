"""
Ensure the package wide config is operating correctly
"""
from zoom_report import Config


def test_package():
    """
    Test package
    """
    assert Config.package() == 'zoom_report'


def test_env():
    """
    Test env
    """
    assert Config.env() == 'dev'
