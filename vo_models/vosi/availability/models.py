"""VOSIAvailability pydantic-xml models."""

from typing import Optional

from pydantic_xml import BaseXmlModel, element

from vo_models.voresource.types import UTCTimestamp

NSMAP = {
    "": "http://www.ivoa.net/xml/VOSIAvailability/v1.0",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class Availability(BaseXmlModel, tag="availability", nsmap=NSMAP):
    """VOSI Availability complex type.

    Elements:
        available (bool):   Whether the service is currently available.
        upSince (datetime): The instant at which the service last became available.
        downAt (datetime):  The instant at which the service is next scheduled to become unavailable.
        backAt (datetime):  The instant at which the service is scheduled to become available again after a period
                            of unavailability.
        note (str):         A textual note concerning availability.
    """

    available: bool = element(tag="available")
    up_since: Optional[UTCTimestamp] = element(tag="upSince")
    down_at: Optional[UTCTimestamp] = element(tag="downAt")
    back_at: Optional[UTCTimestamp] = element(tag="backAt")
    note: Optional[list[str]] = element(tag="note")
