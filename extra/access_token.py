"""
Request OAuth access token from Zoom
"""
import sys
import base64

from dotenv import dotenv_values, find_dotenv
import requests

from zoom_report import Config
from zoom_report.common.helpers import with_retry, parse_response_json
from zoom_report.logger.pkg_logger import Logger


def encode(client_id: str, client_secret: str) -> str:
    """Base64-encode client credentials."""
    if not client_id or not client_secret:
        return ""
    return base64.b64encode(f"{client_id}:{client_secret}".encode("ascii")).decode("ascii")


@with_retry(max_retries=3, base_delay=1.0)
def request_access_token(client_id: str, client_secret: str, auth_code: str) -> requests.Response:
    """Request OAuth access token from Zoom."""
    url = "https://zoom.us/oauth/token"
    encoded = encode(client_id, client_secret)
    if not encoded:
        raise ValueError("Missing client credentials")
    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = {
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": "https://www.example.com"
    }
    return requests.post(url, headers=headers, params=body, timeout=10)


def main():
    """Request access token from Zoom OAuth."""
    try:
        env_path = find_dotenv()
        if not env_path:
            Logger.error("Could not find .env file")
            sys.exit(1)
        config = dotenv_values(env_path)
        auth_code = config.get("ZOOM_AUTHORIZATION_CODE")
        if not auth_code:
            Logger.error("Missing ZOOM_AUTHORIZATION_CODE in .env")
            sys.exit(1)
        client_id = Config.zoom_client_id()
        client_secret = Config.zoom_client_secret()
        if not client_id or not client_secret:
            Logger.error("Missing client credentials in config")
            sys.exit(1)
        response = request_access_token(client_id, client_secret, auth_code)
        data = parse_response_json(response, default={}, context="access_token_request")
        if "access_token" in data:
            Logger.info("Successfully obtained access token")
            print(f"Access token: {data['access_token']}")
            if "refresh_token" in data:
                print(f"Refresh token: {data['refresh_token']}")
        else:
            Logger.error(f"Failed to get access token: {data}")
            sys.exit(1)
    except Exception as e:
        Logger.error(f"Failed to get access token: {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
