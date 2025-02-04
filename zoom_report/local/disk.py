from pathlib import Path

import pandas as pd

from zoom_report import Config
from zoom_report.logger.pkg_logger import Logger


def generate_filepath(topic: str, uuid: str, start_time: str) -> Path:
    """
    Generate a file path using a topic, start time, and UUID.
    :param topic: topic of an instance
    :param uuid: UUID of an instance
    :param start_time: start time of an instance
    :returns: a generated file path
    """
    Logger.info("Generating file name...")
    output_dir = Config.output_dir()
    output_dir.mkdir(exist_ok=True)
    timestamp = start_time.split(" ")[0]
    topic = topic.replace(" ", "-").replace("/", "-")
    uuid = uuid.replace("/", "-")
    file_name = f"{timestamp}_{topic}_{uuid}.csv"
    output_file = output_dir / file_name
    return output_file


def save_to_disk(frame: pd.DataFrame, file_path: Path) -> None:
    """
    Save a given DataFrame as a CSV file.
    :param frame: a DataFrame to save as a CSV file
    :param file_path: a file path for the CSV file
    :returns: None
    """
    Logger.info("Saving report as CSV...")
    frame.to_csv(file_path, index=False)
    Logger.info("Report saved in " + str(file_path))
