import requests
from zoom_report import Config
from zoom_report.common.enums import Http, Cogv
from zoom_report.logger.pkg_logger import Logger


class Ragic:
    _base_url = 'https://na3.ragic.com'

    def _validate_data(self, data: dict) -> bool:
        if not isinstance(data, dict):
            return False
        for key, value in data.items():
            if not isinstance(value, (str, int, float)):
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
        if response.status_code == Http.OK:
            Logger.info(f"Data sent to {url}.")
        return response
