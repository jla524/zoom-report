from urllib.parse import urljoin
import requests
from config import Config
from common.enums import Http
from api.jwt import renew_jwt_token
from logger.pkg_logger import Logger


class Zoom:
    _base_url = 'https://api.zoom.us/v2/.'

    def __init__(self, meeting_id: str):
        self._meeting_id = meeting_id

    def _send_request(self, url, params=None) -> requests.Response:
        token = Config.zoom_jwt_token()
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != Http.OK:
            Logger.info("The token is invalid or expired.")
            Logger.info("Requesting a new token.")
            new_token = renew_jwt_token()
            headers = {'Authorization': f'Bearer {new_token}'}
            response = requests.get(url, headers=headers, params=params)
        return response

    def get_meeting_details(self) -> dict:
        route = f'meetings/{self._meeting_id}'
        url = urljoin(self._base_url, route)
        return self._send_request(url).json()

    def get_participants(self, next_page_token=None) -> dict:
        route = f'report/meetings/{self._meeting_id}/participants'
        url = urljoin(self._base_url, route)
        params = {'page_size': 300}
        if next_page_token:
            params.update({'next_page_token': next_page_token})
        return self._send_request(url, params).json()
