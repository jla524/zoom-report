from enum import Enum


class Http():
    OK = 200
    CREATED = 201
    BAD = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404


class Cogv(Enum):
    MEETING_NUMBER = 1009850
    TOPIC = 1009851
    USER_NAME = 1009863
    USER_EMAIL = 1009864
    DURATION = 1009865
    MEETING_ID = 1009871
    END_TIME = 1009867
    PART = 1009868
    NO = 1009852
    NAME = 1009853
    EMAIL = 1009869
    TOTAL_DURATION = 1009855
    JOIN_TIME = 1009856
    LEAVE_TIME = 1009857

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
