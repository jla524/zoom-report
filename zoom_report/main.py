from zoom_report import Config
from zoom_report.command_line import Cli
from zoom_report.api.zoom import Zoom
from zoom_report.common.helpers import localize
from zoom_report.attendance import get_report
from zoom_report.storage import save_report


def get_localized_instances(instances: list[dict]) -> list[tuple]:
    if not instances or 'meetings' not in instances:
        return []
    localized = [(meeting['uuid'], localize(meeting['start_time']))
                 for meeting in instances['meetings']]
    localized = sorted(localized, key=lambda x: x[1])
    return localized


def process_reports(meeting_id) -> None:
    instances = Zoom().get_meeting_instances(meeting_id)
    instances = get_localized_instances(instances)
    meeting_details = Zoom().get_meeting_details(meeting_id)
    for instance in instances:
        report = get_report(instance[0], meeting_details['timezone'])
        if not report.empty:
            save_report(report, instance, meeting_details)


def run() -> None:
    cli = Cli()
    if cli.args.all:
        with Config.meeting_id_file().open('r') as file:
            for meeting_id in file.read().splitlines():
                process_reports(meeting_id)
    if cli.args.meeting is not None:
        process_reports(cli.args.meeting)
