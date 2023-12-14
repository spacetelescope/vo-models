"""Availability VOSI Schema using Pydantic-XML models"""

from typing import Optional

from pydantic_xml import BaseXmlModel, element
from vo_models.xml.voresource.types import UTCTimestamp

NSMAP = {
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "": "http://www.ivoa.net/xml/VOSIAvailability/v1.0",
}


class Availability(BaseXmlModel, tag="availability", nsmap=NSMAP):
    """Availability VOSI element"""

    available: bool = element(tag="available")
    up_since: Optional[UTCTimestamp] = element(tag="upSince", default=None)
    down_at: Optional[UTCTimestamp] = element(tag="downAt", default=None)
    back_at: Optional[UTCTimestamp] = element(tag="backAt", default=None)
    note: Optional[list[str]] = element(tag="note", default=None)
