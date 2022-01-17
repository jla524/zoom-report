import json
import requests
from base64 import b64encode
#from common.enums import Http

# TODO: store in config
client_id = '4XTCe1A8RxqJuCHRIn1qTg'
client_secret = 'yvevn8oFAsx4oOGcb7XH8xk5vMqqfw6t'
code = '07fYkzYfc5_5QGDEnc9T4eFMW0qRmccwA'

class OAuth2:
    def request_auth(self):
        url = 'https://zoom.us/oauth/authorize'
        params = {'response_type': 'code',
                  'redirect_uri': 'https://example.com',
                  'client_id': client_id}
        response = requests.get(url, params=params)
        if not response.history:
            return ''
        return response.history[-1].url #.split('/')[-1]

    def request_token(self):
        url = 'https://zoom.us/oauth/token'
        auth = f'{client_id}:{client_secret}'.encode('ascii')
        auth = b64encode(auth).decode('ascii')
        headers = {'Authorization': f'Basic {auth}',
                   'Content-Type': 'application/x-www-form-urlencoded'}
        params = {'grant_type': 'authorization_code',
                  'code': code,
                  'redirect_uri': 'https://example.com'}
        response = requests.post(url, headers=headers, params=params)
        if response.status_code != 200:
            return ''
        return json.loads(response.text).get('access_token', '')
