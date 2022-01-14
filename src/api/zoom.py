from time import time
from typing import Optional
import requests
from authlib.jose import jwt
from config import Config


class Zoom:
    def __init__(self, id: str):
        self.id = id
        self.base_url = 'https://api.zoom.us/v2'
        self.reports_url = f'{self.base_url}/report/meetings'
        self.jwt_token_exp = 1209600  # Expires every 2 weeks
        self.jwt_token_algo = 'HS256'

    def _generate_new_token(self):
        time_now = time()
        payload = {
            'aud': None,
            'iat': time_now,
            'exp': time_now + self.jwt_token_exp,
            'iss': Config.zoom_api_key()
        }
        header = {'alg': self.jwt_token_algo}
        token = jwt.encode(header, payload, Config.zoom_api_secret())
        # update in .env too
        Config.update_jwt_token(token)
    
    def _send_request(self, params):
        url = f'{self.reports_url}/{self.id}/participants'
        headers = {'Authorization': f'Bearer {Config.zoom_jwt_token()}'}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            self._generate_new_token()
            headers = {'Authorization': f'Bearer {Config.zoom_jwt_token()}'}
            response = requests.get(url, headers=headers, params=params)
        return response

    def get_meeting_participants(self, next_page_token=None):
        params = {'page_size': 300}
        if next_page_token:
            params.update({'next_page_token': next_page_token})
        return self._send_request(params)