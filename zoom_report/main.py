#!/usr/bin/env python3
from pathlib import Path
from zoom_report.command_line import Cli
from zoom_report.api.zoom import Zoom
from zoom_report.common.helpers import get_meeting_info, localize
from zoom_report.attendance import get_report
from zoom_report.storage import save_report, upload_report, write_records


def fetch_all_attendance(basic_info, details) -> Path:
    for uuid, start_time in basic_info:
        report = get_report(uuid, details['timezone'])
        if report.empty:
            continue
        start_time = localize(start_time)
        path = save_report(report, details['topic'], start_time, uuid)
        upload_report(path)
        additional_info = {'uuid': uuid,
                           'start_time': start_time,
                           'topic': details['topic'],
                           'meeting_id': details['id']}
        write_records(path, additional_info)


def run() -> None:
    cli = Cli()
    if cli.args.all:
        instances = Zoom().get_meeting_instances(cli.args.meeting_id)
        meeting_info = get_meeting_info(instances)
        meeting_details = Zoom().get_meeting_details(cli.args.meeting_id)
        fetch_all_attendance(meeting_info, meeting_details)
