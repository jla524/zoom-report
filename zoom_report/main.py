"""
The main program to fetch and store attendance reports
"""
from zoom_report import Config
from zoom_report.command_line import Cli
from zoom_report.api.zoom import Zoom
from zoom_report.automate.attendance import get_report
from zoom_report.process.instances import get_meetings
from zoom_report.automate.storage import save_report
from zoom_report.logger.pkg_logger import Logger


def process_reports(meeting_id: str, recent: bool) -> None:
    """
    Write meeting instances for a given meeting ID to storage.
    :param meeting_id: a meeting ID to process
    :param recent: only retrieve recent instances
    :returns: None
    """
    meetings = get_meetings(meeting_id, recent)
    details = Zoom().get_meeting_details(meeting_id)
    if not meetings or not details or 'code' in details:
        Logger.error("Unable to process reports")
        return
    for meeting in meetings:
        report = get_report(meeting[0])
        if not report.empty:
            save_report(report, details, meeting)


def run() -> None:
    """
    Run process_reports using the command line arguments.
    :returns: None
    """
    cli = Cli()
    if cli.args.meeting is not None:
        Logger.info(f"Processing meeting ID {cli.args.meeting}")
        process_reports(cli.args.meeting, cli.args.recent)
    if cli.args.all:
        Logger.info("Processing stored meeting IDs...")
        with Config.meeting_id_file().open('r') as file:
            for meeting_id in file.read().splitlines():
                process_reports(meeting_id, cli.args.recent)
