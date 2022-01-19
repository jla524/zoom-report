from urllib.parse import urljoin
import requests
from zoom_report import Config
from zoom_report.common.enums import Http
from zoom_report.api.jwt import renew_jwt_token
from zoom_report.logger.pkg_logger import Logger


class Zoom:
    _base_url = 'https://api.zoom.us/v2/.'

    def _send_request(self, route, params=None):
        url = urljoin(self._base_url, route)
        Logger.info(f"Sending request to {url}")
        token = Config.zoom_jwt_token()
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == Http.UNAUTHORIZED:
            Logger.info("The token has expired. Requesting a new token.")
            new_token = renew_jwt_token()
            headers = {'Authorization': f'Bearer {new_token}'}
            response = requests.get(url, headers=headers, params=params)
        elif response.status_code != Http.OK:
            Logger.info("An error has occured when sending request.")
        return response

    def get_meeting_instances(self, meeting_id):
        Logger.info("Retrieving meeting instances...")
        route = f'past_meetings/{meeting_id}/instances'
        return self._send_request(route).json()

    def get_meeting_details(self, meeting_id):
        Logger.info("Retrieving meeting details...")
        route = f'meetings/{meeting_id}'
        return self._send_request(route).json()

    def get_participants(self, meeting_uuid, next_page_token=None):
        Logger.info("Retrieving meeting participants...")
        route = f'report/meetings/{meeting_uuid}/participants'
        params = {'page_size': 300}
        if next_page_token:
            params.update({'next_page_token': next_page_token})
        response = self._send_request(route, params)
        if response.status_code == Http.NOT_FOUND:
            Logger.error("Unable to retrieve meeting {meeting_uuid}")
            return None
        return response.json()
