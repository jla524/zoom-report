from time import time
from typing import Optional
import requests
from authlib.jose import jwt
from config import Config
from common.enums import Http


class Zoom:
    _base_url = 'https://api.zoom.us/v2/report/meetings/'

    def __init__(self, id: str):
        self.id = id

    def _generate_new_token(self):
        time_now = time()
        payload = {
            'aud': None,
            'iat': time_now,
            'exp': time_now + Config.jwt_token_expire(),
            'iss': Config.zoom_api_key()
        }
        header = {'alg': Config.jwt_token_algo()}
        token = jwt.encode(header, payload, Config.zoom_api_secret())
        Config.update_jwt_token(token.decode('utf-8'))
    
    def _send_request(self, params):
        url = f'{self._base_url}/{self.id}/participants'
        headers = {'Authorization': f'Bearer {Config.zoom_jwt_token()}'}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != Http.OK:
            print("The JWT token is invalid or expired.")
            print("Requesting a new token.")
            self._generate_new_token()
            headers = {'Authorization': f'Bearer {Config.zoom_jwt_token()}'}
            response = requests.get(url, headers=headers, params=params)
        return response

    def get_meeting_participants(self, next_page_token=None):
        params = {'page_size': 300}
        if next_page_token:
            params.update({'next_page_token': next_page_token})
        return self._send_request(params)