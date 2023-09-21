import base64

import requests

from zoom_report import Config
from zoom_report.common.enums import Http


def encode(client_id, client_secret):
    s = f"{client_id}:{client_secret}"
    s = s.encode("ascii") 
    s = base64.b64encode(s)
    s = s.decode("ascii")
    return s


def request_token():
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
