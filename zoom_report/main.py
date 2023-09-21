"""
The main program to fetch and store attendance reports
"""
from zoom_report import Config
from zoom_report.command_line import Cli
from zoom_report.process.meetings import get_instances, get_details
from zoom_report.automate.attendance import get_report
from zoom_report.automate.storage import save_report
from zoom_report.logger.pkg_logger import Logger


def process_reports(meeting_id: str, recent: bool) -> None:
    """
    Write meeting instances for a given meeting ID to storage.
    :param meeting_id: a meeting ID to process
    :param recent: only retrieve recent instances
    :returns: None
    """
    instances = get_instances(meeting_id, recent)
    details = get_details(meeting_id)
    if not instances or not details:
        Logger.warn("Instances not found or ID is invalid.")
        return
    for instance in instances:
        if len(instance) != 2:
            Logger.error("Expected two elements in instance")
            continue
        report = get_report(instance[0])
        save_report(report, details, instance)


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
        with Config.meeting_id_file().open("r") as file:
            for meeting_id in file.read().splitlines():
                process_reports(meeting_id, cli.args.recent)
