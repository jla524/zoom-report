#!/usr/bin/env python3
import sys
from pathlib import Path
from zoom_report.api.zoom import Zoom
from zoom_report.attendance import get_info, to_frame, combine_rejoins
from zoom_report.storage import upload_file, save_report
from zoom_report.common.helpers import get_uuids, encode_uuid
from zoom_report.logger.pkg_logger import Logger


def fetch_meeting_attendance(uuids) -> Path:
    paths = []
    for uuid in uuids:
        info = get_info(encode_uuid(uuid))
        if not info:
            Logger.info(f"Unable to retrieve {uuid}")
            continue
        info = to_frame(info)
        info = combine_rejoins(info)
        paths.append(save_report(info, uuid))
    return paths


def run():
    meeting_id = sys.argv[1]
    instances = Zoom().get_meeting_instances(meeting_id)
    meeting_uuids = get_uuids(instances)
    file_paths = fetch_meeting_attendance(meeting_uuids)
