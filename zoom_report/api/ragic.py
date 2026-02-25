"""
A wrapper for the Ragic API
"""
from http import HTTPStatus
from typing import Optional

import requests

from zoom_report import Config
from zoom_report.common.enums import Cogv
from zoom_report.common.helpers import JSON, parse_response_json, with_retry
from zoom_report.logger.pkg_logger import Logger

REQUEST_TIMEOUT = 60


class Ragic:
    """
    Use the requests library to talk to the Ragic API
    """

    __base_url = "https://na3.ragic.com"
    __headers = {"Authorization": f"Basic {Config.ragic_api_key()}"}

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
            if not (isinstance(key, (str, int)) and isinstance(value, (str, int, float, list))):
                return False
        return True

    @with_retry(max_retries=3, base_delay=1.0)
    def __get_data(
        self, api_route: str, params: Optional[JSON] = None, timeout: int = REQUEST_TIMEOUT
    ) -> requests.Response:
        """
        Get data from the specified API route.
        :param api_route: an API route in Ragic
        :param params: parameters for the request
        :param timeout: timeout the request after n seconds
        :returns: a response from Ragic
        """
        if params and not self.validate_data(params):
            raise TypeError("Payload type check failed.")
        url = f"{self.__base_url}/{api_route}"
        response = requests.get(url, headers=self.__headers, params=params, timeout=timeout)
        return response

    @with_retry(max_retries=3, base_delay=1.0)
    def __send_data(
        self, api_route: str, data: JSON, timeout: int = REQUEST_TIMEOUT
    ) -> requests.Response:
        """
        Send data to the specified API route.
        :param api_route: an API route in Ragic
        :param data: data to be sent to Ragic
        :param timeout: timeout the request after n seconds
        :returns: a response from Ragic
        """
        if not self.validate_data(data):
            raise TypeError("Payload type check failed.")
        url = f"{self.__base_url}/{api_route}"
        response = requests.post(url, headers=self.__headers, data=data, timeout=timeout)
        if response.status_code == HTTPStatus.OK:
            Logger.info(f"Data sent to {url}.")
        return response

    def write_attendance(self, attendance_info: JSON) -> JSON:
        """
        Write attendance data to Ragic.
        :param attendance_info: attendance info from Zoom
        :returns: response data from Ragic
        """
        route = Config.ragic_attendance_route()
        payload = {
            Cogv.MEETING_NUMBER: attendance_info["uuid"],
            Cogv.TOPIC: attendance_info["topic"],
            Cogv.START_TIME: attendance_info["start_time"],
            Cogv.MEETING_ID: attendance_info["meeting_id"],
        }
        response = self.__send_data(route, payload)
        return parse_response_json(response, default={}, context="write_attendance")

    def read_participants(self, uuid: str) -> JSON:
        """
        Read participant data from Ragic.
        :param uuid: a UUID of the meeting
        :returns: participants data from Ragic
        """
        route = Config.ragic_participants_route()
        filters = [f"{Cogv.SUB_MEETING_NUMBER},eq,{uuid}"]
        response = self.__get_data(route, params={"where": filters})
        return parse_response_json(response, default={}, context="read_participants")

    def write_participant(self, uuid: str, participant_info: JSON) -> JSON:
        """
        Write participant data to Ragic.
        :param uuid: a UUID of the meeting
        :param participants_info: participants info from Zoom
        :returns: response data from Ragic
        """
        route = Config.ragic_participants_route()
        payload = {
            Cogv.SUB_MEETING_NUMBER: uuid,
            Cogv.NAME: participant_info["name"],
            Cogv.EMAIL: participant_info["user_email"],
            Cogv.JOIN_TIME: participant_info["join_time"],
            Cogv.LEAVE_TIME: participant_info["leave_time"],
            Cogv.TOTAL_DURATION: participant_info["total_duration"],
        }
        response = self.__send_data(route, payload)
        return parse_response_json(response, default={}, context="write_participant")
