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
            if not (isinstance(key, str)
                    and isinstance(value, (str, int, float))):
                return False
        return True

    def _send_data(self, api_route: str, data: dict) -> requests.Response:
        if not self._validate_data(data):
            raise TypeError("Payload type check failed.")
        url = f'{self._base_url}/{api_route}'
        api_key = Config.ragic_api_key()
        headers = {'Authorization': f'Basic {api_key}'}
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == Http.OK:
            Logger.info(f"Data sent to {url}.")
        return response

    def write_attendance(self, attendance_info: dict) -> dict:
        payload = {Cogv.MEETING_NUMBER: attendance_info['uuid'],
                   Cogv.TOPIC: attendance_info['topic'],
                   Cogv.START_TIME: attendance_info['start_time'],
                   Cogv.MEETING_ID: attendance_info['meeting_id']}
        route = Config.ragic_attendance_route()
        return self._send_data(route, payload).json()

    def write_participants(self, uuid: str, participant_info: dict) -> dict:
        payload = {Cogv.SUB_MEETING_NUMBER: uuid,
                   Cogv.NAME: participant_info['name'],
                   Cogv.EMAIL: participant_info['user_email'],
                   Cogv.JOIN_TIME: participant_info['join_time'],
                   Cogv.LEAVE_TIME: participant_info['leave_time'],
                   Cogv.TOTAL_DURATION: participant_info['total_duration']}
        route = Config.ragic_participants_route()
        return self._send_data(route, payload).json()
