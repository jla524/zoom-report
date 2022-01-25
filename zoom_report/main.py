from typing import Sequence
from datetime import date, timedelta
from zoom_report import Config
from zoom_report.command_line import Cli
from zoom_report.api.zoom import Zoom
from zoom_report.common.helpers import localize
from zoom_report.automate.attendance import get_report
from zoom_report.automate.storage import save_report


def localize_instances(instances: dict) -> Sequence:
    if not instances or 'meetings' not in instances:
        return []
    localized = [(meeting['uuid'], localize(meeting['start_time']))
                 for meeting in instances['meetings']]
    localized = sorted(localized, key=lambda x: x[1])
    return localized


def filter_instances(instances: list[tuple], days: int = 3) -> list[tuple]:
    if instances:
        date_format = Config.datetime_format().split(' ', maxsplit=1)[0]
        start_date = (date.today() - timedelta(days=days)) \
            .strftime(date_format)
        index = len(instances) - 1
        while instances[index][1] > start_date:
            index -= 1
        instances = instances[index+1:]
    return instances


def process_reports(meeting_id: str, recent: bool) -> None:
    instances = Zoom().get_meeting_instances(meeting_id)
    instances = localize_instances(instances)
    details = Zoom().get_meeting_details(meeting_id)
    if instances and details and 'code' not in details:
        if recent:
            instances = filter_instances(instances)
        for instance in instances:
            report = get_report(instance[0])
            if not report.empty:
                save_report(report, details, instance)


def run() -> None:
    cli = Cli()
    if cli.args.meeting is not None:
        process_reports(cli.args.meeting, cli.args.recent)
    if cli.args.all:
        with Config.meeting_id_file().open('r') as file:
            for meeting_id in file.read().splitlines():
                process_reports(meeting_id, cli.args.recent)
