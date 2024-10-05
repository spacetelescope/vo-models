"""VOResource Simple Types"""

import re
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Annotated

from pydantic import Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

# pylint: disable=too-few-public-methods


if TYPE_CHECKING:
    UTCTimestamp = Annotated[datetime, ...]
else:
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


class UTCDateTime(str):
    """A date stamp that can be given to a precision of either a day (type
    xs:date) or seconds (type xs:dateTime). Where only a date is given,
    it is to be interpreted as the span of the day on the UTC timezone
    if such distinctions are relevant."""


class ValidationLevel(Enum):
    """
    The allowed values for describing the resource descriptions and interfaces.
    """

    VALUE_0 = 0
    """
    The resource has a description that is stored in a registry. This level does not imply a compliant description.
    """
    VALUE_1 = 1
    """
    In addition to meeting the level 0 definition, the resource description conforms syntactically to this standard
    and to the encoding scheme used.
    """
    VALUE_2 = 2
    """
    In addition to meeting the level 1 definition, the resource description refers to an existing resource that has
    demonstrated to be functionally compliant.
    """
    VALUE_3 = 3
    """
    In addition to meeting the level 2 definition, the resource description has been inspected by a human and judged
    to comply semantically to this standard as well as meeting any additional minimum quality criteria (e.g., providing
    values for important but non-required metadata) set by the human inspector.
    """
    VALUE_4 = 4
    """
    In addition to meeting the level 3 definition, the resource description meets additional quality criteria set by
    the human inspector and is therefore considered an excellent description of the resource. Consequently, the resource
    is expected to operate well as part of a VO application or research study.
    """


AuthorityID = Annotated[
    str, Field(pattern=r"[\w\d][\w\d\-_\.!~\*'\(\)\+=]{2,}", description="The authority identifier for the resource.")
]

ResourceKey = Annotated[
    str,
    Field(
        pattern=r"[\w\d\-_\.!~\*'\(\)\+=]+(/[\w\d\-_\.!~\*'\(\)\+=]+)*",
        description="The resource key for the resource.",
    ),
]

IdentifierURI = Annotated[
    str,
    Field(
        pattern=r"ivo://[\w\d][\w\d\-_\.!~\*'\(\)\+=]{2,}(/[\w\d\-_\.!~\*'\(\)\+=]+(/[\w\d\-_\.!~\*'\(\)\+=]+)*)?",
        description="A reference to a registry record.",
    ),
]
