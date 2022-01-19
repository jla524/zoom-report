#!/usr/bin/env python3
import sys
from pathlib import Path
from zoom_report.api.zoom import Zoom
from zoom_report.common.helpers import get_meeting_info, encode_uuid
from zoom_report.attendance import get_info, to_frame, combine_rejoins
from zoom_report.storage import upload_file, save_report, write_records
from zoom_report.logger.pkg_logger import Logger


def fetch_all_attendance(basic_info, details) -> Path:
    report_paths = []
    for uuid, start_time in basic_info[:2]:
        info = get_info(encode_uuid(uuid))
        if not info:
            Logger.info(f"Unable to retrieve {uuid}")
            continue
        info = to_frame(info, details['timezone'])
        info = combine_rejoins(info)
        info['uuid'] = uuid
        info['start_time'] = start_time
        info['meeting_id'] = details['id']
        info['topic'] = details['topic']
        report_paths.append(save_report(info, uuid))
    return report_paths


def run():
    meeting_id = sys.argv[1]
    instances = Zoom().get_meeting_instances(meeting_id)
    meeting_details = Zoom().get_meeting_details(meeting_id)
    meeting_info = get_meeting_info(instances)
    file_paths = fetch_all_attendance(meeting_info, meeting_details)
    for file_path in file_paths:
        write_records(file_path)
