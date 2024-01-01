"""VOSIAvailability pydantic-xml models."""

from typing import Optional

from pydantic_xml import BaseXmlModel, element

from vo_models.voresource.types import UTCTimestamp

NSMAP = {
    "": "http://www.ivoa.net/xml/VOSIAvailability/v1.0",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class Availability(BaseXmlModel, tag="availability", nsmap=NSMAP, skip_empty=True):
    """VOSI Availability complex type.

    Parameters:
        available (bool):
            (element) - Whether the service is currently available.
        up_since (UTCTimestamp):
            (element) - The instant at which the service last became available.
        down_at (UTCTimestamp):
            (element) - The instant at which the service is next scheduled to become unavailable.
        back_at (UTCTimestamp):
            (element) - The instant at which the service is scheduled to become available again after a period
            of unavailability.
        note (Optional[list[str]]):
            (element) - A textual note concerning availability.
    """

    available: bool = element(tag="available")
    up_since: Optional[UTCTimestamp] = element(tag="upSince", default=None)
    down_at: Optional[UTCTimestamp] = element(tag="downAt", default=None)
    back_at: Optional[UTCTimestamp] = element(tag="backAt", default=None)
    note: Optional[list[str]] = element(tag="note", default=None)
