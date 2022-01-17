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

    def _send_request(self, route, params=None) -> dict:
        url = urljoin(self._base_url, route)
        token = Config.zoom_jwt_token()
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != Http.OK:
            Logger.info("The token has expired. Requesting a new token.")
            new_token = renew_jwt_token()
            headers = {'Authorization': f'Bearer {new_token}'}
            response = requests.get(url, headers=headers, params=params)
        return response.json()

    def get_meeting_instances(self) -> dict:
        route = f'past_meetings/{self._meeting_id}/instances'
        return self._send_request(route)

    def get_meeting_details(self) -> dict:
        route = f'meetings/{self._meeting_id}'
        return self._send_request(route)

    def get_participants(self, next_page_token=None) -> dict:
        route = f'report/meetings/{self._meeting_id}/participants'
        params = {'page_size': 300}
        if next_page_token:
            params.update({'next_page_token': next_page_token})
        return self._send_request(route, params)

    def get_past_participants(self, meeting_uuid) -> dict:
        route = f'past_meetings/{meeting_uuid}/participants'
        return self._send_request(route)
