#!/usr/bin/env python3
import sys
import attendance


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please enter a meeting id")
        sys.exit(1)
    meeting_id = sys.argv[1]
    file_name = attendance.fetch(meeting_id)
