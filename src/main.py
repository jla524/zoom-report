#!/usr/bin/env python3
import sys
import attendance
import storage
from logger.pkg_logger import Logger


if __name__ == "__main__":
    if len(sys.argv) < 2:
        Logger.error("Please enter a meeting id")
        sys.exit(1)
    meeting_id = sys.argv[1]
    file_path = attendance.fetch(meeting_id)
    storage.upload_file(file_path)
