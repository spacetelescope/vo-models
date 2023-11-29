"""Definitions for useful VO objects"""

import re
from datetime import datetime
from typing import Optional

from pydantic_xml import BaseXmlModel, computed_attr


class VODateTime(datetime):
    """A subclass of datetime to allow expanded handling of ISO formatted datetimes, and enforce
    the use of a Z identifier for UTC timezone in outputs

    """

    # This is the strict regex definition for VO datetimes from:
    # https://www.ivoa.net/documents/VOResource/20180625/REC-VOResource-1.1.html#tth_sEc2.2.4
    # vodt_regex = r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?Z?"

    # Expanded regex to accept Zulu but also +00:00 offset UTC times
    exp_vodt_regex = r"(\d{4}-\d\d-\d\d(T|\s)\d\d:\d\d:\d\d(\.\d+)?)(Z|\+\d\d:\d\d)?"
    # Will match:
    # 2023-03-15T18:27:18.758 (UTC assumed - T separator)
    # 2023-03-15 18:27:18.758 (UTC assumed - space separator)
    # 2023-03-15T18:27:18.758Z (Zulu UTC - T separator)
    # 2023-03-15 18:27:18.758Z (Zulu UTC - space separator)
    # 2023-03-15T18:27:18.758+00:00 (UTC w/ offset - T separator)
    # 2023-03-15 18:27:18.758+00:00 (UTC w/ offset - space separator)

    # TODO: Python 3.11 datetime.fromisoformat() does accept a 'Z' indicated UTC time. Revisit this when upgrading.

    vodt_regex_match = re.compile(exp_vodt_regex)

    def __str__(self) -> str:
        return self.isoformat(sep="T", timespec="milliseconds")

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(pattern=cls.exp_vodt_regex)

    @classmethod
    def validate(cls, value: str):
        """Validator that expands the pydantic datetime model to include Z UTC identifiers

        Args:
            value (str): datetime string. Comes from either a user's POST (destruction) or from the cache

        Returns:
            VODateTime: VO-compliant datetime subclass
        """
        if isinstance(value, VODateTime):
            # For compatibility with ProcMemCache, where the datetime is never serialized.
            return value

        if not isinstance(value, str):
            raise TypeError("String datetime required")

        value = value.upper()

        valid_vodt = cls.vodt_regex_match.fullmatch(value)
        if not valid_vodt:
            # If there was no full match, reject it
            raise ValueError("Invalid VOResource ISO-8601 date format")

        # Grab only the date/time match and manually add a UTC offset for an aware python datetime object
        value = valid_vodt.group(1) + "+00:00"

        return super().fromisoformat(value)

    @classmethod
    def fromisoformat(cls, date_string):
        return cls.validate(date_string)

    def isoformat(self, sep: str = "T", timespec: str = "milliseconds") -> str:
        """Overwrites the datetime isoformat output to use a Z UTC indicator

        Returns:
            str: VO-compliant ISO-8601 datetime string
        """
        iso_dt = super().isoformat(sep=sep, timespec=timespec)
        return iso_dt.replace("+00:00", "Z")


class NillableElement(BaseXmlModel, skip_empty=True, nsmap={"xsi": "http://www.w3.org/2001/XMLSchema-instance"}):
    """An element that can be 'nillable' in XML.

    If no value is provided, the element will be rendered as <element xsi:nil="true" />.
    """

    value: Optional[str] = None

    @computed_attr(name="nil", ns="xsi")
    def nil(self) -> Optional[str]:
        """If the value is None, return 'true'."""
        if self.value is None:
            return "true"
        else:
            return None
