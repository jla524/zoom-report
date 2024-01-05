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
