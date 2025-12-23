"""
Helper functions
"""
from typing import Any, Optional
from urllib.parse import quote_plus

import requests

from zoom_report.logger.pkg_logger import Logger

JSON = dict[str, Any]
Instance = tuple[str, str]


def encode_uuid(uuid: str) -> str:
    """
    Double encode a given UUID if it starts with / or contains //.
    :param uuid: a UUID to encode
    :returns: an encoded UUID
    """
    if uuid.startswith("/") or "//" in uuid:
        uuid = quote_plus(quote_plus(uuid))
    return uuid


def handle_api_status(response: requests.Response, api_description: Optional[str] = None) -> bool:
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
        Logger.error(response["msg"])
        return False
    return True
