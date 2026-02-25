"""
The main program to fetch and store attendance reports
"""
import sys
from pathlib import Path
from typing import List

from zoom_report import Config
from zoom_report.command_line import Cli
from zoom_report.logger.pkg_logger import Logger
from zoom_report.automate.storage import save_report
from zoom_report.automate.attendance import get_report
from zoom_report.process.meetings import get_instances, get_details


MAX_FILE_SIZE = 1024 * 1024  # 1MB limit


def validate_meeting_id_file(file_path: Path) -> None:
    """
    Validate that the meeting ID file exists and is within size limits.
    :param file_path: path to the meeting ID file
    :raises SystemExit: if validation fails
    """
    if not file_path.exists():
        Logger.error(f"Meeting ID file not found: {file_path}")
        sys.exit(1)
    try:
        file_size = file_path.stat().st_size
        if file_size > MAX_FILE_SIZE:
            Logger.error(f"Meeting ID file too large ({file_size} bytes, max {MAX_FILE_SIZE})")
            sys.exit(1)
        if file_size == 0:
            Logger.error("Meeting ID file is empty")
            sys.exit(1)
    except OSError as e:
        Logger.error(f"Cannot read meeting ID file: {e}")
        sys.exit(1)


def read_meeting_ids(file_path: Path) -> List[str]:
    """
    Read and parse meeting IDs from file, filtering out empty lines.
    :param file_path: path to the meeting ID file
    :returns: list of meeting IDs
    :raises SystemExit: if file cannot be read
    """
    try:
        with file_path.open("r") as file:
            return [
                line.strip()
                for line in file.read().splitlines()
                if line.strip()
            ]
    except OSError as e:
        Logger.error(f"Failed to read meeting ID file: {e}")
        sys.exit(1)


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
        meeting_id_file = Config.meeting_id_file()
        validate_meeting_id_file(meeting_id_file)
        meeting_ids = read_meeting_ids(meeting_id_file)
        if not meeting_ids:
            Logger.error("No valid meeting IDs found in file")
            sys.exit(1)
        Logger.info(f"Processing {len(meeting_ids)} meeting ID(s)...")
        for meeting_id in meeting_ids:
            if process_reports(meeting_id, days):
                report_saved = True
    else:
        report_saved = False
    if not report_saved:
        Logger.error("No records were written.")
        sys.exit(1)
