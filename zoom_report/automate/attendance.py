"""
Retrieve Zoom attendance data
"""
import pandas as pd

from zoom_report import Config
from zoom_report.logger.pkg_logger import Logger
from zoom_report.common.helpers import JSON, encode_uuid
from zoom_report.process.meetings import get_info


def convert_to_frame(info: list[JSON]) -> pd.DataFrame:
    """
    Convert participants info to DataFrame format with localized timestamps.
    :param info: participants info from Zoom
    :returns: participants DataFrame with localized timestamps
    """
    Logger.info("Converting attendance info to DataFrame...")
    frame = pd.DataFrame(info)
    for column in ["join_time", "leave_time"]:
        frame[column] = (
            pd.to_datetime(frame[column])
            .dt.tz_convert(Config.timezone())
            .dt.strftime(Config.datetime_format())
        )
    frame["user_email"] = frame["user_email"].fillna("")
    frame.sort_values(["id", "name", "join_time"], inplace=True)
    return frame


def combine_rejoins(frame: pd.DataFrame) -> pd.DataFrame:
    """
    Combine participants info when a duplicate is found.
    :param frame: participants DataFrame
    :returns: participants DataFrame with combined durations and timestamps
    """
    Logger.info("Combining rejoins...")
    frame = (
        frame.groupby(["id", "name", "user_email"])
        .agg({"duration": "sum", "join_time": "min", "leave_time": "max"})
        .reset_index()
        .rename(columns={"duration": "total_duration"})
    )
    frame.columns = frame.columns.get_level_values(0)
    frame.total_duration = round(frame.total_duration / 60, 2)
    return frame


def get_report(uuid: str) -> pd.DataFrame:
    """
    Retrieve an attendance report for a given UUID.
    :param uuid: a meeting UUID to retrieve info from
    :returns: participants DataFrame with aggregated metrics
    """
    attendance = get_info(encode_uuid(uuid))
    if not attendance:
        Logger.info(f"Unable to retrieve meeting with UUID {uuid}.")
        return pd.DataFrame()
    attendance = convert_to_frame(attendance)
    attendance = combine_rejoins(attendance)
    return attendance
