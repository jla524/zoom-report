#!/usr/bin/env python3
import sys
from pathlib import Path
from storage import upload_file
from attendance import get_info, convert_to_frame, combine_rejoins, save_report
from meetings import get_instances, get_uuids
from logger.pkg_logger import Logger


def fetch_meeting_attendance(_id) -> Path:
    info = get_info(_id)
    if not info:
        Logger.info("Attendance data is not available.")
        return None
    info = convert_to_frame(info)
    info = combine_rejoins(info)
    return save_report(info, _id)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        Logger.error("Please enter a meeting id")
        sys.exit(1)
    meeting_id = sys.argv[1]
    file_path = fetch_meeting_attendance(meeting_id)
    upload_file(file_path)
