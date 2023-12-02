import base64
import requests
from dotenv import dotenv_values


def encode(client_id, client_secret):
    s = f"{client_id}:{client_secret}"
    s = s.encode("ascii")
    s = base64.b64encode(s)
    s = s.decode("ascii")
    return s


config = dotenv_values(".env")
url = "https://zoom.us/oauth/token"
headers = {
    "Authorization": "Basic " + encode(config["ZOOM_CLIENT_ID"], config["ZOOM_CLIENT_SECRET"]),
    "Content-Type": "application/x-www-form-urlencoded",
}
body = {"grant_type": "refresh_token", "refresh_token": config["ZOOM_REFRESH_TOKEN"]}
response = requests.post(url, headers=headers, data=body)
print(response.status_code)
print(response.text)
