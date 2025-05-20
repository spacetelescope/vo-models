"""Pydantic-xml models for IVOA schema VORegistry 1.1"""

from typing import Literal, Optional

from pydantic_xml import attr, element

import vo_models.vodataservice as vs
import vo_models.voresource as vr
from vo_models.voregistry.types import ExtensionSearchSupport, OptionalProtocol

NSMAP = {
    "vr": "http://www.ivoa.net/xml/VOResource/v1.0",
    "vg": "http://www.ivoa.net/xml/VORegistry/v1.0",
    "vs": "http://www.ivoa.net/xml/VODataService/v1.1",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "ri": "http://www.ivoa.net/xml/RegistryInterface/v1.0",
}


class OAIHTTP(vr.Interface, nsmap=NSMAP):
    """A description of the standard OAI PMH interface using HTTP (GET or POST) queries."""

    type: Literal["vg:OAIHTTP"] = attr(ns="xsi", default="vg:OAIHTTP")


class OAISOAP(vr.WebService, nsmap=NSMAP):
    """A description of the standard OAI PMH interface using a SOAP Web Service interface."""

    type: Literal["vg:OAISOAP"] = attr(ns="xsi", default="vg:OAISOAP")


class Registry(vr.Service, tag="Resource", nsmap=NSMAP, ns="ri"):
    """A service that provides access to descriptions of resources.

    Parameters:
        full:
            (element) - If true, this registry attempts to collect all resource records known to the IVOA.
        managed_authority:
            (element) - An authority identifier managed by the registry.
        tableset:
            (element) - For registry interfaces with a user-visible table structure, tableset allows its declaration.
    """

    full: bool = element(ns="", nsmap={"": ""})
    type: Literal["vg:Registry"] = attr(ns="xsi", default="vg:Registry")
    managed_authority: Optional[list[vr.AuthorityID]] = element(
        tag="managedAuthority", default=[], ns="", nsmap={"": ""}
    )
    tableset: Optional[vs.TableSet] = element(tag="tableset", default=None, ns="", nsmap={"": ""})


class Harvest(vr.Capability, nsmap=NSMAP):
    """The capabilities of the Registry Harvest implementation.

    Parameters:
        max_records:
            (element) - The largest number of records that the registry search method will return.
        type:
            (attribute) - The type of the capability, which is always "vg:Harvest".
        standard_id:
            (attribute) - The standard ID of the capability, which is always "ivo://ivoa.net/std/Registry".
    """

    max_records: int = element(tag="maxRecords")
    type: Literal["vg:Harvest"] = attr(ns="xsi", default="vg:Harvest")
    standard_id: Literal["ivo://ivoa.net/std/Registry"] = attr(name="standardID", default="ivo://ivoa.net/std/Registry")


class Search(vr.Capability, nsmap=NSMAP):
    """The capabilities of the Registry Search implementation.

    Parameters:
        max_records:
            (element) - The largest number of records that the registry search method will return.
        type:
            (attribute) - The type of the capability, which is always "vg:Search".
        standard_id:
            (attribute) - The standard ID of the capability, which is always "ivo://ivoa.net/std/Registry".
        extension_search_support:
            (element) - (deprecated) Used in Registry Interfaces 1.0 to indicate what VOResource extensions a
            search interface supported.
        optional_protocol:
            (element) - (deprecated) Used in Registry Interfaces 1.0 to indicate search protocol extensions.
    """

    max_records: int = element(tag="maxRecords")
    type: Literal["vg:Search"] = attr(ns="xsi", default="vg:Search")
    standard_id: Literal["ivo://ivoa.net/std/Registry"] = attr(name="standardID", default="ivo://ivoa.net/std/Registry")
    extension_search_support: Optional[ExtensionSearchSupport] = element(tag="extensionSearchSupport", default=None)
    optional_protocol: Optional[list[OptionalProtocol]] = element(tag="optionalProtocol", default=[])


class Authority(vr.Resource, tag="Resource", nsmap=NSMAP, ns="ri"):
    """A naming authority; an assertion of control over a namespace represented by an authority identifier.

    type:
        (attribute) - The type of the authority, which is always "vg:Authority".
    managing_org:
        (element) - The organization that manages or owns this authority.
    """

    type: Literal["vg:Authority"] = attr(ns="xsi", default="vg:Authority")
    managing_org: vr.ResourceName = element(tag="managingOrg", default="", ns="", nsmap={"": ""})
