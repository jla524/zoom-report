import requests
from authlib.jose import jwt
from config import Config
from common.enums import Http
from jwt import renew_jwt_token


class Zoom:
    _base_url = 'https://api.zoom.us/v2/'

    def __init__(self, meeting_id: str):
        self._meeting_id = meeting_id
 
    def _send_request(self,url, params=None):
        token = Config.zoom_jwt_token()
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != Http.OK:
            print("The token is invalid or expired.")
            print("Requesting a new token.")
            new_token = renew_jwt_token()
            headers = {'Authorization': f'Bearer {new_token}'}
            response = requests.get(url, headers=headers, params=params)
        return response

    def get_meeting_details(self):
        url = f'{self._base_url}/meetings/{self._meeting_id}'
        return self._send_request(url).json()

    def get_participants(self, next_page_token=None):
        url = f'{self._base_url}/report/{self._meeting_id}/participants'
        params = {'page_size': 300}
        if next_page_token:
            params.update({'next_page_token': next_page_token})
        return self._send_request(url, params).json()
