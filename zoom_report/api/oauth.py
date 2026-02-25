"""
Define function to request new access and refresh token for Zoom OAuth
"""
import base64
from http import HTTPStatus

import requests

from zoom_report import Config
from zoom_report.logger.pkg_logger import Logger


def encode(client_id, client_secret):
    """
    Base64-encode client ID and client secret, separated with colon
    :param client_id: Zoom OAuth client ID
    :param client_secret: Zoom OAuth client secret
    :returns: a base64-encoded string
    """
    if not client_id or not client_secret:
        return ""
    secret = f"{client_id}:{client_secret}".encode("ascii")
    encoded = base64.b64encode(secret).decode("ascii")
    return encoded


def make_token_request(encoded: str, refresh_token: str, timeout: int) -> requests.Response:
    """
    Make the HTTP POST request to Zoom OAuth endpoint.
    :param encoded: base64-encoded credentials
    :param refresh_token: Zoom refresh token
    :param timeout: request timeout in seconds
    :returns: HTTP response object
    :raises: requests.exceptions.RequestException on network errors
    """
    url = "https://zoom.us/oauth/token"
    headers = {
        "Authorization": "Basic " + encoded,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    body = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    return requests.post(url, headers=headers, data=body, timeout=timeout)


def handle_http_error(response: requests.Response) -> None:
    """
    Check HTTP response status and raise exception on error.
    :param response: HTTP response object
    :raises: requests.exceptions.HTTPError if status is not OK
    """
    if response.status_code != HTTPStatus.OK:
        Logger.error(f"OAuth request failed with status {response.status_code}: {response.text}")
        raise requests.exceptions.HTTPError(
            f"OAuth request failed: {response.status_code}",
            response=response
        )


def parse_token_response(response: requests.Response) -> dict:
    """
    Parse OAuth response and validate required fields.
    :param response: HTTP response object
    :returns: parsed JSON data
    :raises: ValueError if response is invalid or missing required fields
    """
    try:
        data = response.json()
    except ValueError as e:
        Logger.error(f"Invalid JSON response from OAuth: {e}")
        raise ValueError("Invalid OAuth response: not valid JSON") from e
    if "access_token" not in data:
        Logger.error("OAuth response missing access_token")
        raise ValueError("Invalid OAuth response: missing access_token")
    if "refresh_token" not in data:
        Logger.error("OAuth response missing refresh_token")
        raise ValueError("Invalid OAuth response: missing refresh_token")
    return data


def request_token(timeout: int = 10) -> str:
    """
    Request new access token from Zoom OAuth app.
    :returns: a new access token
    :raises: requests.exceptions.RequestException on network errors
    :raises: ValueError on invalid response
    :raises: requests.exceptions.HTTPError on HTTP error status
    """
    encoded = encode(Config.zoom_client_id(), Config.zoom_client_secret())
    if not encoded:
        Logger.error("Cannot encode OAuth credentials: missing client_id or client_secret")
        raise ValueError("Missing OAuth credentials")
    refresh_token = Config.zoom_refresh_token()
    if not refresh_token:
        Logger.error("Missing refresh token")
        raise ValueError("Missing refresh token")
    try:
        response = make_token_request(encoded, refresh_token, timeout)
    except requests.exceptions.RequestException as e:
        Logger.error(f"Network error during OAuth token request: {e}")
        raise
    handle_http_error(response)
    data = parse_token_response(response)
    Config.update_refresh_token(data["refresh_token"])
    return data["access_token"]
