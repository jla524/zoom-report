"""
A wrapper around jwt
"""
from time import time

from authlib.jose import jwt

from zoom_report import Config


def renew_jwt_token(expires: int = 604800) -> str:
    """
    Generate a new JWT token
    :param expires: number of seconds before the token expires
    :returns: a new token
    """
    time_now = time()
    payload = {'aud': None,
               'iat': time_now,
               'exp': time_now + expires,
               'iss': Config.zoom_api_key()}

    header = {'alg': 'HS256'}
    api_secret = Config.zoom_api_secret()

    token = jwt.encode(header, payload, api_secret).decode('utf-8')
    Config.update_jwt_token(token)
    return token
