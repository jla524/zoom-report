from pathlib import Path
from datetime import datetime
import pandas as pd
from api.zoom import Zoom
from config import Config
from logger.pkg_logger import Logger


def get_info(meeting_id) -> dict:
    zoom = Zoom(meeting_id)
    response = zoom.get_participants()
    participants = response.get('participants')
    while token := response.get('next_page_token'):
        response = zoom.get_participants(next_page_token=token)
        participants += response.get('participants')
    return participants


def convert_to_frame(info) -> pd.DataFrame:
    frame = pd.DataFrame(info)
    for column in ['join_time', 'leave_time']:
        frame[column] = pd.to_datetime(frame[column]) \
            .dt.tz_convert(Config.timezone())
    frame.sort_values(['id', 'name', 'join_time'], inplace=True)
    return frame


def combine_rejoins(frame) -> pd.DataFrame:
    frame = frame.groupby(['id', 'name', 'user_email']) \
        .agg({'duration': ['sum'],
              'join_time': ['min'],
              'leave_time': ['max']}) \
        .reset_index() \
        .rename(columns={"duration": "total_duration"})
    frame.columns = frame.columns.get_level_values(0)
    frame.total_duration = round(frame.total_duration / 60, 2)
    return frame


def save_report(df, meeting_id) -> Path:
    date = datetime.today().date()
    output_dir = Config.output_dir()
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f'{meeting_id}_{date}.csv'
    df.to_csv(output_file, index=False)
    Logger.info("File writtten to " + str(output_file))
    return output_file
