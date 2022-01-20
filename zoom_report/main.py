#!/usr/bin/env python3
import sys
from pathlib import Path
from zoom_report.command_line import Cli
from zoom_report.api.zoom import Zoom
from zoom_report.common.helpers import get_meeting_info, encode_uuid, localize
from zoom_report.attendance import get_info, to_frame, combine_rejoins
from zoom_report.storage import save_report, upload_report, write_records
from zoom_report.logger.pkg_logger import Logger


def fetch_all_attendance(basic_info, details) -> Path:
    for uuid, start_time in basic_info:
        attendance = get_info(encode_uuid(uuid))
        if attendance is None:
            Logger.info(f"Unable to retrieve {uuid}")
            continue
        attendance = to_frame(attendance, details['timezone'])
        attendance = combine_rejoins(attendance)
        path = save_report(attendance, details['topic'], uuid)
        upload_report(path)
        additional_info = {'uuid': uuid,
                           'start_time': localize(start_time),
                           'topic': details['topic'],
                           'meeting_id': details['id']}
        write_records(path, additional_info)


def run() -> None:
    cli = Cli()
    if cli.args.all:
        instances = Zoom().get_meeting_instances(cli.args.meeting_id)
        meeting_details = Zoom().get_meeting_details(cli.args.meeting_id)
        meeting_info = get_meeting_info(instances)
        fetch_all_attendance(meeting_info, meeting_details)
