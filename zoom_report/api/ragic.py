"""
A wrapper for the Ragic API
"""
from http import HTTPStatus

import requests

from zoom_report import Config
from zoom_report.common.enums import Cogv
from zoom_report.common.helpers import JSON
from zoom_report.logger.pkg_logger import Logger


class Ragic:
    """
    Use the requests library to talk to the Ragic API
    """

    __base_url = "https://na3.ragic.com"

    @staticmethod
    def validate_data(data: JSON) -> bool:
        """
        Ensure the payload data is in the proper format.
        :param data: a dict with payload data to validate
        :returns: True if data is valid and False otherwise
        """
        if not isinstance(data, dict):
            return False
        for key, value in data.items():
            if not (isinstance(key, (str, int)) and isinstance(value, (str, int, float))):
                return False
        return True

    def __send_data(self, api_route: str, data: JSON, timeout: int = 10) -> requests.Response:
        """
        Send data to the specified API route.
        :param api_route: an API route in Ragic
        :param data: data to be sent to Ragic
        :returns: a response from Ragic
        """
        if not self.validate_data(data):
            raise TypeError("Payload type check failed.")

        url = f"{self.__base_url}/{api_route}"
        api_key = Config.ragic_api_key()
        headers = {"Authorization": f"Basic {api_key}"}
        response = requests.post(url, data=data, headers=headers, timeout=timeout)
        if response.status_code == HTTPStatus.OK:
            Logger.info(f"Data sent to {url}.")
        return response

    def write_attendance(self, attendance_info: JSON) -> JSON:
        """
        Write attendance data to Ragic.
        :param attendance_info: attendance info from Zoom
        :returns: response data from Ragic
        """
        payload = {
            Cogv.MEETING_NUMBER: attendance_info["uuid"],
            Cogv.TOPIC: attendance_info["topic"],
            Cogv.START_TIME: attendance_info["start_time"],
            Cogv.MEETING_ID: attendance_info["meeting_id"],
        }
        route = Config.ragic_attendance_route()
        return self.__send_data(route, payload).json()

    def write_participants(self, uuid: str, participant_info: JSON) -> JSON:
        """
        Write participants data to Ragic.
        :param uuid: a UUID of the meeting
        :param participants_info: participants info from Zoom
        :returns: response data from Ragic
        """
        payload = {
            Cogv.SUB_MEETING_NUMBER: uuid,
            Cogv.NAME: participant_info["name"],
            Cogv.EMAIL: participant_info["user_email"],
            Cogv.JOIN_TIME: participant_info["join_time"],
            Cogv.LEAVE_TIME: participant_info["leave_time"],
            Cogv.TOTAL_DURATION: participant_info["total_duration"],
        }
        route = Config.ragic_participants_route()
        return self.__send_data(route, payload).json()
