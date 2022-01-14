from typing import Dict
from datetime import datetime
import pandas as pd
from api.zoom import Zoom
from config import Config


def get_participants(meeting_id):
    zoom = Zoom(meeting_id)
    response = zoom.get_meeting_participants()
    participants = response.json().get('participants')
    while token := response.json().get('next_page_token'):
        response = zoom.get_meeting_participants(next_page_token=token)
        participants += response.json().get('participants')
    return participants


def convert_to_frame(participants):
    df = pd.DataFrame(participants)
    for column in ['join_time', 'leave_time']:
        df[column] = pd.to_datetime(df[column]) \
            .dt.tz_convert(Config.timezone())
    df.sort_values(['id', 'name', 'join_time'], inplace=True)
    return df


def combine_rejoins(df):
    output_df = df.groupby(['id', 'name', 'user_email']) \
        .agg({"duration": ['sum'], 'join_time': ['min'], 'leave_time': ['max']}) \
        .reset_index() \
        .rename(columns={"duration": "total_duration"})
    output_df.columns = output_df.columns.get_level_values(0)
    output_df.total_duration = round(output_df.total_duration / 3600, 2)
    return output_df


def save_attendence(output_df, id):
    date = datetime.today().date()
    output_dir = Config.output_dir()
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f'{id}_{date}.csv'
    output_df.to_csv(output_file, index=False)
    return output_file


def fetch(meeting_id):
    data = get_participants(meeting_id)
    if data is None:
        print("Attendance data is not available")
        return
    data = convert_to_frame(data)
    data = combine_rejoins(data)
    return save_attendence(data, meeting_id)