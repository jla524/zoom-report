"""
A wrapper for the Zoom API
"""
from typing import Optional, Any
from urllib.parse import urljoin
from http import HTTPStatus

import requests

from zoom_report.api.oauth import request_token
from zoom_report.logger.pkg_logger import Logger

JSON = dict[str, Any]


class Zoom:
    """
    Use the requests library to talk to the Zoom API
    """

    __base_url = "https://api.zoom.us/v2/."

    def __init__(self):
        self.token = request_token()

    def __send_request(
        self, route: str, params: Optional[JSON] = None, timeout: int = 10
    ) -> requests.Response:
        url = urljoin(self.__base_url, route)
        Logger.info(f"Sending request to {url}")
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        if response.status_code != HTTPStatus.OK:
            Logger.warn("An error has occured when sending request.")
        return response

    def get_meeting_instances(self, meeting_id: str) -> dict:
        """
        Retrieve all meeting instances of a given meeting ID
        :params meeting_id: a meeting ID to retrieve
        :returns: response data from Zoom
        """
        Logger.info("Retrieving meeting instances...")
        route = f"past_meetings/{meeting_id}/instances"
        return self.__send_request(route).json()

    def get_meeting_details(self, meeting_id: str) -> dict:
        """
        Retrieve all meeting details of a given meeting ID
        :params meeting_id: a meeting ID to retrieve
        :returns: response data from Zoom
        """
        Logger.info("Retrieving meeting details...")
        route = f"meetings/{meeting_id}"
        return self.__send_request(route).json()

    def get_participants(self, meeting_uuid: str, next_page_token: Optional[str] = None) -> JSON:
        """
        Retrieve all meeting participants of a given meeting ID
        :params meeting_id: a meeting ID to retrieve
        :returns: response data from Zoom
        """
        Logger.info("Retrieving meeting participants...")
        route = f"report/meetings/{meeting_uuid}/participants"
        params = {"page_size": "300"}

        if next_page_token:
            params.update({"next_page_token": next_page_token})
        response = self.__send_request(route, params)
        if response.status_code == HTTPStatus.NOT_FOUND:
            Logger.error("Unable to retrieve meeting {meeting_uuid}")
            return {}
        return response.json()
