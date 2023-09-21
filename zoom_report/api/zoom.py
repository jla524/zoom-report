"""
A wrapper for the Zoom API
"""
from typing import Optional, Any
from urllib.parse import urljoin

import requests

from zoom_report.common.enums import Http
from zoom_report.api.oauth import request_token
from zoom_report.logger.pkg_logger import Logger


class Zoom:
    """
    Use the requests library to talk to the Zoom API
    """

    _base_url = "https://api.zoom.us/v2/."

    def __init__(self):
        self.token = request_token()

    def _send_request(self, route, params=None):
        url = urljoin(self._base_url, route)
        Logger.info(f"Sending request to {url}")
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != Http.OK:
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
        return self._send_request(route).json()

    def get_meeting_details(self, meeting_id: str) -> dict:
        """
        Retrieve all meeting details of a given meeting ID
        :params meeting_id: a meeting ID to retrieve
        :returns: response data from Zoom
        """
        Logger.info("Retrieving meeting details...")
        route = f"meetings/{meeting_id}"
        return self._send_request(route).json()

    def get_participants(
        self, meeting_uuid: str, next_page_token: Optional[str] = None
    ) -> dict[str, Any]:
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
        response = self._send_request(route, params)

        if response.status_code == Http.NOT_FOUND:
            Logger.error("Unable to retrieve meeting {meeting_uuid}")
            return {}
        return response.json()
