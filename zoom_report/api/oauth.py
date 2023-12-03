"""
Define function to request new access and refresh token for Zoom OAuth
"""
import base64
from http import HTTPStatus

import requests

from zoom_report import Config


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


def request_token(timeout: int = 10) -> str:
    """
    Request new access token from Zoom OAuth app
    :returns: a new access token
    """
    url = "https://zoom.us/oauth/token"
    encoded = encode(Config.zoom_client_id(), Config.zoom_client_secret())
    headers = {
        "Authorization": "Basic " + encoded,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    body = {"grant_type": "refresh_token", "refresh_token": Config.zoom_refresh_token()}
    response = requests.post(url, headers=headers, data=body, timeout=timeout)
    assert response.status_code == HTTPStatus.OK, response.text
    Config.update_refresh_token(response.json()["refresh_token"])
    return response.json()["access_token"]
