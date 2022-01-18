from urllib.parse import urljoin, quote_plus
import requests
from config import Config
from common.enums import Http
from api.jwt import renew_jwt_token
from logger.pkg_logger import Logger


class Zoom:
    _base_url = 'https://api.zoom.us/v2/.'

    def _send_request(self, route, params=None):
        url = urljoin(self._base_url, route)
        Logger.info(f"Sending request to {url}")
        token = Config.zoom_jwt_token()
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != Http.OK:
            Logger.info("The token has expired. Requesting a new token.")
            new_token = renew_jwt_token()
            headers = {'Authorization': f'Bearer {new_token}'}
            response = requests.get(url, headers=headers, params=params)
        return response.json()

    def get_meeting_details(self, meeting_id):
        Logger.info("Retrieving meeting details...")
        route = f'meetings/{meeting_id}'
        return self._send_request(route)

    def get_meeting_instances(self, meeting_id):
        Logger.info("Retrieving meeting instances...")
        route = f'past_meetings/{meeting_id}/instances'
        return self._send_request(route)

    def get_participants(self, meeting_uuid, next_page_token=None):
        Logger.info("Retrieving meeting participants...")
        route = f'report/meetings/{meeting_uuid}/participants'
        params = {'page_size': 300}
        if next_page_token:
            params.update({'next_page_token': next_page_token})
        return self._send_request(route, params)
