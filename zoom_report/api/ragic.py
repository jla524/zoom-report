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

    def __get_data(self, api_route: str, params: JSON, timeout: int = 10) -> requests.Response:
        """
        Get data from the specified API route.
        :param api_route: an API route in Ragic
        :param params: parameters for the request
        :param timeout: timeout the request after n seconds
        :returns: a response from Ragic
        """
        if not self.validate_data(params):
            raise TypeError("Payload type check failed.")
        url = f"{self.__base_url}/{api_route}"
        response = requests.get(url, headers=self.__headers, params=params, timeout=timeout)
        return response

    def __send_data(self, api_route: str, data: JSON, timeout: int = 10) -> requests.Response:
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

    def __record_exists(self, api_route: str, data: JSON, keys: list[str]) -> bool:
        """
        Check if a record exists in the API route.
        :param api_route: an API route in Ragic
        :param data: data to be sent to Ragic
        :param timeout: timeout the request after n seconds
        :param keys: a list of keys to use for duplicate checking
        :returns: True if the record exists and False otherwise
        """
        if not self.validate_data(data):
            raise TypeError("Payload type check failed.")
        filters = [f"{key},eq,{data[key]}" for key in keys]
        result = self.__get_data(api_route, params={"where": filters}).json()
        return bool(result)

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
        if self.__record_exists(route, payload, [Cogv.MEETING_NUMBER, Cogv.TOPIC]):
            Logger.warn(f"Record exists in {route}, skipping write.")
            return {}
        return self.__send_data(route, payload).json()

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
        if self.__record_exists(route, payload, [Cogv.SUB_MEETING_NUMBER, Cogv.NAME]):
            Logger.warn(f"Record exists in {route}, skipping write.")
            return {}
        return self.__send_data(route, payload).json()
