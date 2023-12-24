import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

url = "https://zoom.us/oauth/authorize?"
params = {
    "response_type": "code",
    "redirect_uri": "https://www.example.com",
    "client_id": config["ZOOM_CLIENT_ID"],
}

url += "&".join(f"{k}={v}" for k, v in params.items())
print("Visit this url on your browser: ", url, sep="\n")
