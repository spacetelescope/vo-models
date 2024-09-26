"""VOSICapabilities pydantic-xml models."""

from typing import Optional, Union

from pydantic_xml import BaseXmlModel, element

from vo_models.tapregext.models import TableAccess
from vo_models.voresource.models import Capability

NSMAP = {
    "vosi": "http://www.ivoa.net/xml/VOSICapabilities/v1.0",
    "": "http://www.ivoa.net/xml/VOResource/v1.0",
    "vs": "http://www.ivoa.net/xml/VODataService/v1.0",
    "tr": "http://www.ivoa.net/xml/TAPRegExt/v1.0",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class VOSICapabilities(BaseXmlModel, tag="capabilities", ns="vosi", nsmap=NSMAP):
    """A listing of capabilities supported by a service

    Parameters:
        capability:
            (element) - A capability supported by the service.
                A protocol-specific capability is included by specifying a vr:Capability sub-type via an xsi:type
                attribute on this element.
    """

    capability: Optional[list[Union[Capability | TableAccess]]] = element(tag="capability", default_factory=list)
