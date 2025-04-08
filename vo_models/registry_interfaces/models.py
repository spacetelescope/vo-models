"""VORegistryInterfaces v1.0 Pydantic-XML models"""
from pydantic import model_validator
from pydantic_xml import BaseXmlModel, attr, element

import vo_models.voresource as vr

NSMAP = {
    "ri": "http://www.ivoa.net/xml/RegistryInterface/v1.0",
    "vr": "http://www.ivoa.net/xml/VOResource/v1.0",
}


class Resource(vr.Resource, ns="ri", nsmap=NSMAP):
    """A description of a single resource."""


class VOResources(BaseXmlModel):
    """A container for one or more resource descriptions or identifier references to resources.

    Parameters:
        resource:
            (element) - One or more resource descriptions.
        identifier:
            (element) - One or more identifier references to resources.
        from:
            (attribute) - The starting number of resources to return.
        number_returned:
            (attribute) - The number of resources returned in the response.
        more:
            (attribute) - Indicates whether there are more resources available.
    """

    resource: list[Resource] = element(tag="Resource", default=[])
    identifier: list[vr.IdentifierURI] = element(tag="identifier", default=[])

    # positive ints
    from_: int = attr(name="from", alias="from", gt=0)
    number_returned: int = attr(name="numberReturned", gt=0)
    more: bool = attr(name="more")

    @model_validator(mode="before")
    @classmethod
    def check_resource_or_identifier(cls, values):
        """Ensure that either 'resource' or 'identifier' is provided."""
        if values.get("resource") and values.get("identifier"):
            raise ValueError("Either 'resource' or 'identifier' must be provided.")
        return values
