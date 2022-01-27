"""
Ensure the singletons are working properly
"""
from zoom_report import Config
from zoom_report.logger.pkg_logger import LoggerLoader, Logger


def test_logger_loader_singleton():
    """
    Test to see if logger loader is a singleton
    """
    loader1 = LoggerLoader().load()
    loader2 = LoggerLoader().load()
    assert id(loader1) == id(loader2)


def test_logger__singleton():
    """
    Test to see if logger is a singleton
    """
    log1 = Logger()
    log2 = Logger()
    assert id(log1) == id(log2)


def test_config_singleton():
    """
    Test to see if config is a singleton
    """
    cfg1 = Config()
    cfg2 = Config()
    assert id(cfg1) == id(cfg2)
