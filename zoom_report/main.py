#!/usr/bin/env python3
import sys
from pathlib import Path
from zoom_report.api.zoom import Zoom
from zoom_report.attendance import get_info, to_frame, combine_rejoins
from zoom_report.storage import upload_file, save_report
from zoom_report.common.helpers import get_meeting_info, encode_uuid
from zoom_report.logger.pkg_logger import Logger


def fetch_all_attendance(details) -> Path:
    paths = []
    for uuid, start_time in details:
        info = get_info(encode_uuid(uuid))
        if not info:
            Logger.info(f"Unable to retrieve {uuid}")
            continue
        info = to_frame(info)
        info = combine_rejoins(info)
        info['uuid'] = uuid
        info['start_time'] = start_time
        paths.append(save_report(info, uuid))
    return paths


def run():
    meeting_id = sys.argv[1]
    instances = Zoom().get_meeting_instances(meeting_id)
    meeting_details = get_meeting_info(instances)
    file_paths = fetch_all_attendance(meeting_details)
