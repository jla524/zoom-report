"""
The main program to fetch and store attendance reports
"""
import sys

from zoom_report import Config
from zoom_report.command_line import Cli
from zoom_report.process.meetings import get_instances, get_details
from zoom_report.automate.attendance import get_report
from zoom_report.automate.storage import save_report
from zoom_report.logger.pkg_logger import Logger


def process_reports(meeting_id: str, n_days: int) -> bool:
    """
    Write meeting instances for a given meeting ID to storage.
    :param meeting_id: a meeting ID to process
    :param n_days: number of days from today to filter on
    :returns: True if at least one report is saved and False otherwise
    """
    assert n_days <= 365, "Cannot retrieve data more than a year ago."
    instances = get_instances(meeting_id, n_days)
    details = get_details(meeting_id)
    if not instances or not details:
        Logger.warn("Instances not found or ID is invalid.")
        return False
    saved = False
    for (uuid, start_time) in instances:
        report = get_report(uuid)
        details["uuid"] = uuid
        details["start_time"] = start_time
        if save_report(meeting_id, details, report):
            saved = True
    return saved


def run() -> None:
    """
    Run process_reports using the command line arguments.
    :returns: None
    """
    cli = Cli()
    days = 2 if cli.args.backfill else 1 if cli.args.recent else 365
    if cli.args.meeting is not None:
        Logger.info(f"Processing meeting ID {cli.args.meeting}.")
        report_saved = process_reports(cli.args.meeting, days)
    elif cli.args.all:
        Logger.info("Processing stored meeting IDs...")
        report_saved = False
        with Config.meeting_id_file().open("r") as file:
            meeting_ids = file.read().splitlines()
        for meeting_id in meeting_ids:
            if process_reports(meeting_id, days):
                report_saved = True
    else:
        report_saved = False
    if not report_saved:
        Logger.error("No records were written.")
        sys.exit(1)
