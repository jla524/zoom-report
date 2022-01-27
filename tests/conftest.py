"""
Define fixture for function and unit module tests
"""
from typing import Generator
import pytest
import zoom_report


@pytest.fixture()
def pkg_test() -> Generator:
    """
    Test version
    """
    yield zoom_report
