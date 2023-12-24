import base64
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
url = "https://zoom.us/oauth/token"


def encode(client_id, client_secret):
    s = f"{client_id}:{client_secret}"
    s = s.encode("ascii")
    s = base64.b64encode(s)
    s = s.decode("ascii")
    return s


secret = "Basic " + encode(config["ZOOM_CLIENT_ID"], config["ZOOM_CLIENT_SECRET"])
headers = {"Authorization": secret, "Content-Type": "application/x-www-form-urlencoded"}
body = {"code": config["ZOOM_AUTHORIZATION_CODE"], "grant_type": "authorization_code", "redirect_uri": "https://www.example.com"}

response = requests.post(url, headers=headers, params=body)
print(response.status_code, response.text)
