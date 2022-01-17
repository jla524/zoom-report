import requests
from config import Config
from logger.pkg_logger import Logger


class Ragic:
    _base_url = 'https://na3.ragic.com'

    def _validate_data(self, data: dict) -> bool:
        for key, value in data.items():
            if not (isinstance(key, str) and isinstance(value, str)):
                return False
        return True

    def send_data(self, data: dict) -> requests.Response:
        if not self._validate_data(data):
            Logger.error("Data is invalid. Unable to write to Ragic.")
            return None
        url = f'{self._base_url}/{Config.ragic_form_dir()}'
        api_key = Config.ragic_api_key()
        headers = {'Authorization': f'Basic {api_key}'}
        response = requests.post(url, data=data, headers=headers)
        return response
