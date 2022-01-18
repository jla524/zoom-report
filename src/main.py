#!/usr/bin/env python3
import sys
from pathlib import Path
from api.zoom import Zoom
from attendance import get_info, convert_to_frame, combine_rejoins
from storage import upload_file, save_report
from common.helpers import get_uuids, encode_uuid
from logger.pkg_logger import Logger


def fetch_meeting_attendance(uuids) -> Path:
    paths = []
    for uuid in uuids:
        info = get_info(encode_uuid(uuid))
        if not info:
            Logger.info(f"Unable to retrieve {uuid}")
            continue
        info = convert_to_frame(info)
        info = combine_rejoins(info)
        paths.append(save_report(info, uuid))
    return paths


if __name__ == "__main__":
    if len(sys.argv) < 2:
        Logger.error("Please enter a meeting id")
        sys.exit(1)
    meeting_id = sys.argv[1]
    instances = Zoom().get_meeting_instances(meeting_id)
    meeting_uuids = get_uuids(instances)
    file_paths = fetch_meeting_attendance(meeting_uuids)
