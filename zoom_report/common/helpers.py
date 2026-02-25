"""
Helper functions
"""
import time
from functools import wraps
from typing import Any, Optional
from urllib.parse import quote_plus

import requests

from zoom_report.logger.pkg_logger import Logger

JSON = dict[str, Any]
Instance = tuple[str, str]


RETRYABLE_STATUSES = {429, 500, 502, 503, 504}
RETRYABLE_EXCEPTIONS = (
    requests.exceptions.ConnectionError,
    requests.exceptions.Timeout,
)


def with_retry(max_retries: int = 3, base_delay: float = 1.0):
    """
    Decorator to add retry logic with exponential backoff.
    Retries on HTTP 429, 500, 502, 503, 504 or connection/timeout errors.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    if isinstance(result, requests.Response):
                        if result.status_code in RETRYABLE_STATUSES:
                            delay = base_delay * (2 ** attempt)
                            Logger.warn(f"Request failed (status {result.status_code}), retrying in {delay}s (attempt {attempt + 1}/{max_retries})")
                            time.sleep(delay)
                            continue
                    return result
                except RETRYABLE_EXCEPTIONS as e:
                    delay = base_delay * (2 ** attempt)
                    Logger.warn(f"Request failed ({type(e).__name__}), retrying in {delay}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def encode_uuid(uuid: str) -> str:
    """
    Double encode a given UUID if it starts with / or contains //.
    :param uuid: a UUID to encode
    :returns: an encoded UUID
    """
    if uuid.startswith("/") or "//" in uuid:
        uuid = quote_plus(quote_plus(uuid))
    return uuid


def handle_api_status(response: JSON, api_description: Optional[str] = None) -> bool:
    """
    Parse status message from API response and decide if it's safe to continue.
    :param response: an API response
    :return: a boolean value
    """
    if not api_description:
        api_description = "calling the API"
    if response.get("status", "") == "SKIPPED":
        Logger.warn("Update has been skipped.")
        return False
    if response.get("status", "") == "INVALID":
        Logger.warn(f"An error occurred when {api_description}.")
        Logger.error(response.get("msg", "Unknown error."))
        return False
    return True
