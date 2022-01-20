import pandas as pd
from zoom_report import Config
from zoom_report.common.helpers import encode_uuid
from zoom_report.api.zoom import Zoom
from zoom_report.logger.pkg_logger import Logger


def get_info(uuid: str) -> list[dict]:
    Logger.info("Retrieving attendance info...")
    zoom = Zoom()
    response = zoom.get_participants(uuid)
    participants = response.get('participants')
    while token := response.get('next_page_token'):
        response = zoom.get_participants(uuid, next_page_token=token)
        participants += response.get('participants')
    return participants


def to_frame(info: dict, timezone: str) -> pd.DataFrame:
    Logger.info("Converting attendance info to DataFrame...")
    frame = pd.DataFrame(info)
    for column in ['join_time', 'leave_time']:
        frame[column] = pd.to_datetime(frame[column]) \
            .dt.tz_convert(timezone) \
            .dt.strftime(Config.datetime_format())
    frame['user_email'] = frame['user_email'].fillna('')
    frame.sort_values(['id', 'name', 'join_time'], inplace=True)
    return frame


def combine_rejoins(frame: pd.DataFrame) -> pd.DataFrame:
    Logger.info("Combining rejoins...")
    frame = frame.groupby(['id', 'name', 'user_email']) \
        .agg({'duration': 'sum', 'join_time': 'min', 'leave_time': 'max'}) \
        .reset_index() \
        .rename(columns={'duration': 'total_duration'})
    frame.columns = frame.columns.get_level_values(0)
    frame.total_duration = round(frame.total_duration / 60, 2)
    return frame


def get_report(uuid: str, timezone: str) -> pd.DataFrame:
    attendance = get_info(encode_uuid(uuid))
    if attendance is None:
        Logger.info(f"Unable to retrieve {uuid}")
        return pd.DataFrame()
    attendance = to_frame(attendance, timezone)
    return combine_rejoins(attendance)
