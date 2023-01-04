"""
Ensure the helper functions are working properly
"""
from zoom_report.common.helpers import encode_uuid, localize


def test_encode_uuid() -> None:
    """
    Test to see if encode_uuid double encodes UUIDs correctly
    """
    uuids = {
        "/ajXp12QmuoKj485875==": "%252FajXp12QmuoKj485875%253D%253D",
        "ajXp12Quo//Kj485875==": "ajXp12Quo%252F%252FKj485875%253D%253D",
        "ajXp12QmutoKj485875==": "ajXp12QmutoKj485875==",
    }
    for uuid, encoded in uuids.items():
        assert encode_uuid(uuid) == encoded


def test_localize() -> None:
    """
    Test to see if localize converts to local time correctly
    """
    utc_time = "1994-11-05T13:15:30Z"
    localized_time = ["1994-11-05 04:15:30", "1994-11-05 05:15:30"]
    assert localize(utc_time) in localized_time
