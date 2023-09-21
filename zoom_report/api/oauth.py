import base64

import requests

from zoom_report import Config
from zoom_report.common.enums import Http


def encode(client_id, client_secret):
    """
    Base64-encode client ID and client secret, separated with colon
    :param client_id: Zoom OAuth client ID
    :param client_secret: Zoom OAuth client secret
    :returns: a base64-encoded string
    """
    if not client_id or not client_secret:
        return ""
    data = f"{client_id}:{client_secret}"
    data = data.encode("ascii")
    data = base64.b64encode(data)
    data = data.decode("ascii")
    return data


def request_token() -> str:
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
    body = {
        "grant_type": "refresh_token",
        "refresh_token": Config.zoom_refresh_token(),
    }
    response = requests.post(url, headers=headers, data=body)
    assert response.status_code == Http.OK, response.text
    Config.update_refresh_token(response.json()["refresh_token"])
    return response.json()["access_token"]
