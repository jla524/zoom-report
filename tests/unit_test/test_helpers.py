"""
Ensure the helper functions are working properly
"""
from zoom_report.common.helpers import encode_uuid, handle_api_status


def test_encode_uuid() -> None:
    """
    Test to see if encode_uuid double encodes UUIDs correctly
    """
    uuid_pairs = {
        "/ajXp12QmuoKj485875==": "%252FajXp12QmuoKj485875%253D%253D",
        "ajXp12Quo//Kj485875==": "ajXp12Quo%252F%252FKj485875%253D%253D",
        "ajXp12QmutoKj485875==": "ajXp12QmutoKj485875==",
    }
    for uuid, encoded in uuid_pairs.items():
        assert encode_uuid(uuid) == encoded


def test_handle_api_status() -> None:
    """
    Test to see if handle_api_status handles API statuses correctly
    """
    for bad_status in ("SKIPPED", "INVALID"):
        assert handle_api_status({"status": bad_status}) is False
    for good_status in ("", "SUCCESS", "OK"):
        assert handle_api_status({"status": good_status}) is True
