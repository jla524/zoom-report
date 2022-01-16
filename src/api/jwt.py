from time import time
from config import Config


def renew_jwt_token() -> str:
    time_now = time()
    payload = {'aud': None,
               'iat': time_now,
               'exp': time_now + Config.jwt_token_expire(),
               'iss': Config.zoom_api_key()}
    header = {'alg': Config.jwt_token_algo()}
    api_secret = Config.zoom_api_secret()
    token = jwt.encode(header, payload, api_secret).decode('utf-8')
    Config.update_jwt_token(token)
    return token
