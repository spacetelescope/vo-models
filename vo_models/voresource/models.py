"""Pydantic-xml models for IVOA schema VOResource-v1.1.xsd"""
import datetime
from typing import Literal, Optional

from pydantic import field_validator, networks
from pydantic_xml import BaseXmlModel, attr, element

from vo_models.voresource.types import IdentifierURI, UTCTimestamp, ValidationLevel

# pylint: disable=no-self-argument
# pylint: disable=too-few-public-methods

NSMAP = {
    "vr": "http://www.ivoa.net/xml/VOResource/v1.0",
    "xs": "http://www.w3.org/2001/XMLSchema",
    "vm": "http://www.ivoa.net/xml/VOMetadata/v0.1",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class Validation(BaseXmlModel, nsmap=NSMAP):
    """A validation stamp combining a validation level and the ID of the validator.

    Parameters:
        validated_by:
            (attr) - The IVOA ID of the registry or organisation that assigned the validation level.
    """

    value: ValidationLevel

    validated_by: networks.AnyUrl = attr(
        name="validatedBy",
    )

    @field_validator("value", mode="before")
    def _validate_value(cls, values):
        """Ensure value is a ValidationLevel instance"""
        if isinstance(values, str):
            if values.isdigit():
                return ValidationLevel(int(values))
        return values


class ResourceName(BaseXmlModel, nsmap=NSMAP):
    """The name of a potentially registered resource.

    That is, the entity referred to may have an associated identifier.

    Parameters:
        ivo_id:
            (attr) - The IVOA identifier for the resource referred to.
        value:
            (content) - The name of the resource.
    """

    value: str
    ivo_id: Optional[IdentifierURI] = attr(name="ivo-id", default=None)


class Date(BaseXmlModel, nsmap=NSMAP):
    """A string indicating what the date refers to.

    The value of role should be taken from the vocabulary maintained at http://www.ivoa.net/rdf/voresource/date_role.

    Parameters:
        value: The date and time of the event.
        role:
            (attr) - A string indicating what the date refers to.
    """

    value: UTCTimestamp
    role: Optional[str] = attr(
        name="role",
        default="representative",
    )


class Source(BaseXmlModel, nsmap=NSMAP):
    """A bibliographic reference from which the present resource is derived or extracted.

    Parameters:
        value: The bibliographic reference.
        format:
            (attr) - The reference format.
            Recognized values include "bibcode", referring to a standard astronomical bibcode
            (http://cdsweb.u-strasbg.fr/simbad/refcode.html).
    """

    value: networks.AnyUrl
    format: Optional[str] = attr(name="format", default=None)


class Rights(BaseXmlModel, nsmap=NSMAP):
    """A statement of usage conditions.

    This will typically include a license, which should be given as a full string
    (e.g., Creative Commons Attribution 3.0 International). Further free-text information, e.g., on how to attribute or
    on embargo periods is allowed.

    Parameters:
        value: The statement of usage conditions.
        rights_uri:
            (attr) - A URI identifier for a license
    """

    value: str
    rights_uri: Optional[networks.AnyUrl] = attr(name="rightsURI", default=None)


class AccessURL(BaseXmlModel, nsmap=NSMAP):
    """The URL (or base URL) that a client uses to access the service.

    Parameters:
        value: The URL (or base URL) that a client uses to access the service.
        use:
            (attr) - A flag indicating whether this should be interpreted as a base URL, a full URL, or a URL to a
            directory that will produce a listing of files.
    """

    value: networks.AnyUrl

    use: Literal["full", "base", "dir"] = attr(name="use")


class MirrorURL(BaseXmlModel, nsmap=NSMAP):
    """A URL of a mirror (i.e., a functionally identical additional service interface) to

    Parameters:
        value: A URL of a mirror
        title:
            (attr) - A terse, human-readable phrase indicating the function or location of this mirror, e.g.,
            "Primary Backup" or "European Mirror".
    """

    value: networks.AnyUrl
    title: Optional[str] = attr(name="title", default=None)


class Contact(BaseXmlModel, nsmap=NSMAP):
    """Information allowing establishing contact, e.g., for purposes of support.

    Parameters:
        ivo_id:
            (attr) - An IVOA identifier for the contact (typically when it is an organization).
        name:
            (element) - The name or title of the contact person.
                This can be a person's name, e.g. “John P. Jones” or a group, “Archive Support Team”.
        address:
            (element) - The contact mailing address.
                All components of the mailing address are given in one string,
                e.g. “3700 San Martin Drive, Baltimore, MD 21218 USA”.
        email:
            (element) - The contact email address.
        telephone:
            (element) - The contact telephone number.
                Complete international dialing codes should be given, e.g. “+1-410-338-1234”.
        alt_identifier:
            (element) - A reference to this entitiy in a non-IVOA identifier scheme, e.g., orcid.
                Always use a URI form including a scheme here.
    """

    ivo_id: Optional[IdentifierURI] = attr(name="ivo_id", default=None)

    name: ResourceName = element(tag="name")
    address: Optional[str] = element(tag="address", default=None)
    email: Optional[str] = element(tag="email", default=None)
    telephone: Optional[str] = element(tag="telephone", default=None)
    alt_identifier: Optional[list[networks.AnyUrl]] = element(tag="altIdentifier", default_factory=list)

    @field_validator("name", mode="before")
    def _validate_name(cls, values):
        """Ensure name is a ResourceName instance"""
        if isinstance(values, str):
            return ResourceName(value=values)
        return values


class Creator(BaseXmlModel, nsmap=NSMAP):
    """The entity (e.g. person or organisation) primarily responsible for creating something

    Parameters:
        ivo_id:
            (attr) - An IVOA identifier for the creator (typically when it is an organization).
        name:
            (element) - The name or title of the creating person or organisation
            Users of the creation should use this name in
            subsequent credits and acknowledgements.
            This should be exactly one name, preferably last name
            first (as in "van der Waals, Johannes Diderik").
        logo:
            (element) - URL pointing to a graphical logo, which may be used to help identify the information source.
        alt_identifier:
            (element) - A reference to this entitiy in a non-IVOA identifier scheme, e.g., orcid. Always use a URI form
            including a scheme here.
    """

    ivo_id: Optional[IdentifierURI] = attr(name="ivo_id", default=None)

    name: ResourceName = element(tag="name")
    logo: Optional[networks.AnyUrl] = element(tag="logo", default=None)
    alt_identifier: Optional[list[networks.AnyUrl]] = element(tag="altIdentifier", default_factory=list)

    @field_validator("name", mode="before")
    def _validate_name(cls, values):
        """Ensure name is a ResourceName instance"""
        if isinstance(values, str):
            return ResourceName(value=values)
        return values


class Relationship(BaseXmlModel, nsmap=NSMAP):
    """A description of the relationship between one resource and one or more other resources.

    Parameters:
        relationship_type:
            (element) - The named type of relationship
                The value  of relationshipType should be taken from the vocabulary at
                http://www.ivoa.net/rdf/voresource/relationship_type.
        related_resource:
            (element) - the name of resource that this resource is related to.
    """

    relationship_type: str = element(tag="relationshipType")

    related_resource: list[ResourceName] = element(tag="relatedResource")


class SecurityMethod(BaseXmlModel, nsmap=NSMAP):
    """A description of a security mechanism.

    This type only allows one to refer to the mechanism via a URI.  Derived types would allow for more metadata.

    Parameters:
        standard_id:
            (attr) - A URI identifier for a standard security mechanism.
    """

    standard_id: Optional[networks.AnyUrl] = attr(name="standardID", default=None)


class Curation(BaseXmlModel, nsmap=NSMAP):
    """Information regarding the general curation of a resource

    Parameters:
        publisher:
            (element) - Entity (e.g. person or organisation) responsible for making the resource available
        creator:
            (element) - The entity/ies (e.g. person(s) or organisation) primarily responsible for creating the content
            or constitution of the resource.
        contributor:
            (element) - Entity responsible for contributions to the content of the resource
        date:
            (element) - Date associated with an event in the life cycle of the resource.
        version:
            (element) - Label associated with creation or availablilty of a version of a resource.
        contact:
            (element) - Information that can be used for contacting someone with regard to this resource.
    """

    publisher: ResourceName = element(tag="publisher")
    creator: Optional[list[Creator]] = element(tag="creator", default_factory=list)
    contributor: Optional[list[ResourceName]] = element(tag="contributor", default_factory=list)
    date: Optional[list[Date]] = element(tag="date", default_factory=list)
    version: Optional[str] = element(tag="version", default=None)
    contact: list[Contact] = element(tag="contact")


class Content(BaseXmlModel, nsmap=NSMAP):
    """Information regarding the general content of a resource

    Parameters:
        subject:
            (element) - A topic, object type, or other descriptive keywords about the resource.
                Terms for Subject should be drawn from the Unified Astronomy Thesaurus (http://astrothesaurus.org).
        description:
            (element) - An account of the nature of the resource.
        source:
            (element) - A bibliographic reference from which the present resource is derived or extracted.
        reference_url:
            (element) - URL pointing to a human-readable document describing this resource.
        type:
            (element) - Nature or genre of the content of the resource.
                Values for type should be taken from the controlled vocabulary
                http://www.ivoa.net/rdf/voresource/content_type
        content_level:
            (element) - Description of the content level or intended audience.
                Values for contentLevel should be taken from the controlled vocabulary
                http://www.ivoa.net/rdf/voresource/content_level.
        relationship:
            (element) - a description of a relationship to another resource.
    """

    subject: list[str] = element(tag="subject")
    description: str = element(tag="description")
    source: Optional[Source] = element(tag="source", default=None)
    reference_url: networks.AnyUrl = element(tag="referenceURL")
    type: Optional[list[str]] = element(tag="type", default_factory=list)
    content_level: Optional[list[str]] = element(tag="contentLevel", default_factory=list)
    relationship: Optional[list[Relationship]] = element(tag="relationship", default_factory=list)


class Interface(BaseXmlModel, tag="interface", nsmap=NSMAP):
    """A description of a service interface.

    Since this type is abstract, one must use an Interface subclass to describe an actual interface denoting
    it via xsi:type.

    Additional interface subtypes (beyond WebService and WebBrowser) are defined in the VODataService schema.

    Parameters:
        version:
            (attr) - The version of a standard interface specification that this interface complies with.
        role:
            (attr) - A tag name that identifies the role the interface plays in the particular capability.
        type:
            (attr) - The xsi:type of the interface.
        access_url:
            (element) - The URL (or base URL) that a client uses to access the service.
        mirror_url:
            (element) - A (base) URL of a mirror of this interface.
        security_method:
            (element) - The mechanism the client must employ to authenticate to the service.
        test_querystring:
            (element) - Test data for exercising the service.
    """

    version: Optional[str] = attr(name="version", default=None)
    role: Optional[str] = attr(name="role", default=None)
    type: Optional[str] = attr(name="type", default=None, ns="xsi")

    access_url: list[AccessURL] = element(tag="accessURL")
    mirror_url: Optional[list[MirrorURL]] = element(tag="mirrorURL", default_factory=list)
    security_method: Optional[list[SecurityMethod]] = element(tag="securityMethod", default_factory=list)
    test_querystring: Optional[str] = element(tag="testQueryString", default=None)


class WebBrowser(Interface, nsmap=NSMAP):
    """A (form-based) interface intended to be accesed interactively by a user via a web browser."""

    type: Literal["vr:WebBrowser"] = attr(name="type", default="vr:WebBrowser", ns="xsi")


class WebService(Interface, nsmap=NSMAP):
    """A Web Service that is describable by a WSDL document.

    The accessURL element gives the Web Service's endpoint URL.

    Parameters:
        wsdl_url:
            (element) - The location of the WSDL that describes this Web Service.
    """

    type: Literal["vr:WebService"] = attr(name="type", default="vr:WebService", ns="xsi")

    wsdl_url: Optional[list[networks.AnyUrl]] = element(tag="wsdlURL", default_factory=list)


class Resource(BaseXmlModel, nsmap=NSMAP):
    """Any entity or component of a VO application that is describable and
                        identifiable by an IVOA Identifier.

    Parameters:
        created:
            (attr) - The UTC date and time this resource metadata description was created.
        updated:
            (attr) - The UTC date this resource metadata description was last updated.
        status:
            (attr) - A tag indicating whether this resource is believed to be still actively maintained.
        version:
            (attr) - The VOResource XML schema version against which this instance was written.
        validation_level:
            (element) - A numeric grade describing the quality of the resource description, when applicable, to be used
            to indicate the confidence an end-user can put in the resource as part of a VO application or research
            study.
        title:
            (element) - The full name given to the resource
        short_name:
            (element) - A short name or abbreviation given to the resource.
            One word or a few letters is recommended.  No more than sixteen characters are allowed.
        identifier:
            (element) - Unambiguous reference to the resource conforming to the IVOA standard for identifiers
        alt_identifier:
            (element) - A reference to this resource in a non-IVOA identifier scheme, e.g., DOI or bibcode.
        curation:
            (element) - Information regarding the general curation of the resource
        content:
            (element) - Information regarding the general content of the resource
    """

    created: UTCTimestamp = attr(name="created")
    updated: UTCTimestamp = attr(name="updated")
    status: Literal["active", "inactive", "deleted"] = attr(name="status")
    version: Optional[str] = attr(name="version", default=None)

    validation_level: Optional[list[Validation]] = element(tag="validationLevel", default_factory=list)
    title: str = element(tag="title")
    short_name: Optional[str] = element(tag="shortName", default=None)
    identifier: networks.AnyUrl = element(tag="identifier")
    alt_identifier: Optional[list[networks.AnyUrl]] = element(tag="altIdentifier", default_factory=list)
    curation: Curation = element(tag="curation")
    content: Content = element(tag="content")

    @field_validator("created", "updated")
    def _validate_timestamps(cls, values):
        """Ensure that the created and updated timestamps are not in the future"""
        if values > datetime.datetime.now(datetime.timezone.utc):
            raise ValueError(f"{values} timestamp must not be in the future")
        return values

    @field_validator("short_name")
    def _validate_short_name(cls, values):
        """Ensure that the short name is no more than 16 characters"""
        if values and len(values) > 16:
            raise ValueError("Short name must be no more than 16 characters")
        return values


class Organisation(Resource, nsmap=NSMAP):
    """A named group of one or more persons brought together to pursue participation in VO applications.

    Parameters:
        facility:
            (element) - The observatory or facility used to collect the data contained or managed by this resource.
        instrument:
            (element) - The instrument used to collect the data contained or managed by a resource.

    """

    facility: Optional[list[ResourceName]] = element(tag="facility", default_factory=list)
    instrument: Optional[list[ResourceName]] = element(tag="instrument", default_factory=list)


class Capability(BaseXmlModel, tag="capability", nsmap=NSMAP):
    """A description of what the service does (in terms of context-specific behavior), and how to use it
    (in terms of an interface)

    Parameters:
        standard_id:
            (attr) - A URI identifier for a standard service.
        type:
            (attr) - A protocol-specific capability is included by specifying a vr:Capability sub-type via an xsi:type
            attribute on this model.
        validation_level:
            (element) - A numeric grade describing the quality of the capability description and interface, when
            applicable, to be used to indicate the confidence an end-user can put in the resource as part of a
            VO application or research study.
        description:
            (element) - A human-readable description of what this capability provides as part of the over-all service.
        interface:
            (element) - A description of how to call the service to access this capability.
    """

    standard_id: networks.AnyUrl = attr(name="standardID")
    type: Optional[str] = attr(name="type", default=None, ns="xsi")

    validation_level: Optional[list[Validation]] = element(tag="validationLevel", default_factory=list)
    description: Optional[str] = element(tag="description", default=None)
    interface: Optional[list[Interface]] = element(tag="interface", default_factory=list)


class Service(Resource, nsmap=NSMAP):
    """A resource that can be invoked by a client to perform some action on its behalf.

    Parameters:
        rights:
            (element) - Information about rights held in and over the resource.
        capability:
            (element) - A description of a general capability of the service and how to use it.
    """

    rights: Optional[list[Rights]] = element(tag="rights", default_factory=list)
    capability: Optional[list[Capability]] = element(tag="capability", default_factory=list)
