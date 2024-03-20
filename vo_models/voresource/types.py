"""VOResource Simple Types"""

import re
from datetime import datetime

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class UTCTimestamp(datetime):
    """A subclass of datetime to allow expanded handling of ISO formatted datetimes, and enforce
    the use of a Z identifier for UTC timezone in outputs

    """

    # This is the strict regex definition for VO datetimes from:
    # https://www.ivoa.net/documents/VOResource/20180625/REC-VOResource-1.1.html#tth_sEc2.2.4
    # vodt_regex = r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?Z?"

    # Expanded regex to accept Zulu but also +00:00 offset UTC times
    exp_utc_regex = r"(\d{4}-\d\d-\d\d(T|\s)\d\d:\d\d:\d\d(\.\d+)?)(Z|\+\d\d:\d\d)?"
    # Will match:
    # 2023-03-15T18:27:18.758 (UTC assumed - T separator)
    # 2023-03-15 18:27:18.758 (UTC assumed - space separator)
    # 2023-03-15T18:27:18.758Z (Zulu UTC - T separator)
    # 2023-03-15 18:27:18.758Z (Zulu UTC - space separator)
    # 2023-03-15T18:27:18.758+00:00 (UTC w/ offset - T separator)
    # 2023-03-15 18:27:18.758+00:00 (UTC w/ offset - space separator)

    # TODO: Python 3.11 datetime.fromisoformat() does accept a 'Z' indicated UTC time. Revisit this when upgrading.

    utc_regex_match = re.compile(exp_utc_regex)

    def __str__(self) -> str:
        return self.isoformat(sep="T", timespec="milliseconds")

    def _serialize(self) -> str:
        return self.isoformat(sep="T", timespec="milliseconds")

    # pylint: disable=unused-argument
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.datetime_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize,
                info_arg=False,
                return_schema=core_schema.str_schema(),
            ),
        )

    @classmethod
    def _validate(cls, value: str):
        """Validator that expands the pydantic datetime model to include Z UTC identifiers

        Args:
            value: datetime string. Comes from either a user's POST (destruction) or from the cache

        Returns:
            UTCTimestamp: VO-compliant datetime subclass
        """

        if isinstance(value, UTCTimestamp):
            return value

        if isinstance(value, datetime):
            return cls._validate(value.isoformat())

        if not isinstance(value, str):
            raise TypeError("String datetime required")

        value = value.upper()

        valid_utc = cls.utc_regex_match.fullmatch(value)
        if not valid_utc:
            # If there was no full match, reject it
            raise ValueError("Invalid VOResource ISO-8601 date format")

        # Grab only the date/time match and manually add a UTC offset for an aware python datetime object
        value = valid_utc.group(1) + "+00:00"

        return super().fromisoformat(value)

    @classmethod
    def fromisoformat(cls, date_string):
        return cls._validate(date_string)

    def isoformat(self, sep: str = "T", timespec: str = "milliseconds") -> str:
        """Overwrites the datetime isoformat output to use a Z UTC indicator

        Parameters:
            sep: Separator between date and time (default: 'T')
            timespec: Resolution of time to include (default: 'milliseconds')

        Returns:
            str: VO-compliant ISO-8601 datetime string
        """
        iso_dt = super().isoformat(sep=sep, timespec=timespec)
        return iso_dt.replace("+00:00", "Z")
