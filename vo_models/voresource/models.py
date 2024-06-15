"""Pydantic-xml models for IVOA schema VOResource-v1.1.xsd"""
import datetime
from typing import Literal, Optional

from pydantic import field_validator, networks
from pydantic_xml import BaseXmlModel, attr, element

from vo_models.voresource.types import IdentifierURI, UTCTimestamp, ValidationLevel

# pylint: disable=no-self-argument
# pylint: disable=too-few-public-methods

NSMAP = {
    "xml": "http://www.w3.org/XML/1998/namespace",
    "": "http://www.w3.org/2001/XMLSchema",
    "xs": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "vr": "http://www.ivoa.net/xml/VOResource/v1.0",
    "vm": "http://www.ivoa.net/xml/VOMetadata/v0.1",
}


class Validation(BaseXmlModel, tag="validation", nsmap=NSMAP):
    """A validation stamp combining a validation level and the ID of the validator.

    Parameters:
        value: (ValidationLevel): The validation level.
        validated_by: (networks.AnyUrl):
            (attr) - The IVOA ID of the registry or organisation that assigned the validation level.
    """

    value: ValidationLevel

    validated_by: networks.AnyUrl = attr(
        name="validatedBy",
    )


class ResourceName(BaseXmlModel, nsmap=NSMAP):
    """The name of a potentially registered resource.

    That is, the entity referred to may have an associated identifier.

    Parameters:
        value: (str): The name of the resource.
        ivo_id: (Optional[IdentifierURI]):
            (attr) - The IVOA identifier for the resource referred to.
    """

    value: str
    ivo_id: Optional[IdentifierURI] = attr(name="ivo-id", default=None)


class Date(BaseXmlModel, tag="date", nsmap=NSMAP):
    """A string indicating what the date refers to.

    The value of role should be taken from the vocabulary maintained at http://www.ivoa.net/rdf/voresource/date_role.
    This includes the traditional and deprecated strings “creation”, indicating the date that the resource itself was
    created, and “update”, indicating when the resource was updated last, and the default value, “representative”,
    meaning the date is a rough representation of the time coverage of the resource. The preferred terms from that
    vocabulary are the DataCite Metadata terms. It is expected that the vocabulary will be kept synchronous with the
    corresponding list of terms in the DataCite Metadata schema.

    Parameters:
        value: (UTCTimestamp): The date and time of the event.
        role: (Optional[str]):
            (attr) - A string indicating what the date refers to.
    """

    value: UTCTimestamp
    role: Optional[str] = attr(
        name="role",
        default="representative",
    )


class Source(BaseXmlModel, tag="source", nsmap=NSMAP):
    """

    Parameters:
        value: (networks.AnyUrl): A bibliographic reference from which the present resource is derived or extracted.
        format: (Optional[str]):
            (attr) - The reference format.

                Recognized values include "bibcode", referring to a standard astronomical bibcode
                (http://cdsweb.u-strasbg.fr/simbad/refcode.html).
    """

    value: str
    format: Optional[str] = attr(name="format", default=None)


class Rights(BaseXmlModel, tag="rights", nsmap=NSMAP):
    """A statement of usage conditions.

    This will typically include a license, which should be given as a full string
    (e.g., Creative Commons Attribution 3.0 International). Further free-text information, e.g., on how to attribute or
    on embargo periods is allowed.

    Parameters:
        value: (str): The statement of usage conditions.
        rights_uri: (Optional[networks.AnyUrl]):
            (attr) - A URI identifier for a license
    """

    value: str
    rights_uri: Optional[networks.AnyUrl] = attr(name="rightsURI", default=None)


class AccessURL(BaseXmlModel, tag="accessURL", nsmap=NSMAP):
    """The URL (or base URL) that a client uses to access the service.

    Parameters:
        value: (networks.AnyUrl): The URL (or base URL) that a client uses to access the service.
        use: (Literal["full", "base", "dir"]):
            (attr) - A flag indicating whether this should be interpreted as a base URL, a full URL, or a URL to a
            directory that will produce a listing of files.

                Allowed values are:

                "full" - Assume a full URL--that is, one that can be invoked directly without alteration.
                "base" - Assume a base URL--that is, one requiring an extra portion to be appended before being invoked.
                "dir" - Assume URL points to a directory that will return a listing of files.
    """

    value: networks.AnyUrl

    use: Literal["full", "base", "dir"] = attr(name="use")


class MirrorURL(BaseXmlModel, tag="mirrorURL", nsmap=NSMAP):
    """A URL of a mirror (i.e., a functionally identical additional service interface) to a service.

    Parameters:
        value: (networks.AnyUrl): A URL of a mirror
        title: (Optional[str]):
            (attr) - A terse, human-readable phrase indicating the function or location of this mirror, e.g.,
            "Primary Backup" or "European Mirror".
    """

    value: networks.AnyUrl
    title: Optional[str] = attr(name="title", default=None)


class Contact(BaseXmlModel, tag="contact", nsmap=NSMAP):
    """Information allowing establishing contact, e.g., for purposes of support.

    Parameters:
        ivo_id: (Optional[Type]):
            (attr) - An IVOA identifier for the contact (typically when it is an organization).
        name: (ResourceName):
            (element) - The name or title of the contact person.

                This can be a person's name, e.g. “John P. Jones” or a group, “Archive Support Team”.
        address: (Optional[str]):
            (element) - The contact mailing address

                All components of the mailing address are given in one string, e.g.
                “3700 San Martin Drive, Baltimore, MD 21218 USA”.
        email: (Optional[str]):
            (element) - The contact email address
        telephone: (Optional[str]):
            (element) - The contact telephone number

                Complete international dialing codes should be given, e.g.
                “+1-410-338-1234”.
        alt_identifier: (Optional[list[str] | str]):
            (element) - A reference to this entitiy in a non-IVOA identifier scheme, e.g., orcid.

                Always use a URI form including a scheme here.
    """

    ivo_id: Optional[IdentifierURI] = attr(name="ivo-id")

    name: ResourceName = element(tag="name")
    address: Optional[str] = element(tag="address", default=None)
    email: Optional[str] = element(tag="email", default=None)
    telephone: Optional[str] = element(tag="telephone", default=None)
    alt_identifier: Optional[list[str]] = element(tag="altIdentifier", default_factory=list)

    @field_validator("name", mode="before")
    def _validate_name(cls, value):
        """Ensure that name is a ResourceName or convert it to one."""
        if isinstance(value, str):
            value = ResourceName(value=value)
        return value

    @field_validator("alt_identifier", mode="before")
    def _validate_alt_identifier(cls, value):
        """Ensure that the alt_identifier is a list of strings."""
        if isinstance(value, str):
            value = [value]


class Creator(BaseXmlModel, tag="creator", nsmap=NSMAP):
    """The entity (e.g. person or organisation) primarily responsible for creating something

    Parameters:
        ivo_id: (Optional[IdentifierURI]):
            (attr) - An IVOA identifier for the creator (typically when it is an organization).
        name: (ResourceName):
            (element) - The name or title of the creating person or organisation.

                Users of the creation should use this name in subsequent credits and acknowledgements.
                This should be exactly one name, preferably last name first (as in "van der Waals, Johannes Diderik").
        logo: (Optional[networks.AnyUrl]):
            (element) - URL pointing to a graphical logo, which may be used to help identify the information source.
        alt_identifier: (Optional[list[networks.AnyUrl]]):
            (element) - A reference to this entitiy in a non-IVOA identifier scheme, e.g., orcid.

                Always use a URI form including a scheme here.
    """

    ivo_id: Optional[IdentifierURI] = attr(name="ivo-id", default=None)

    name: ResourceName = element(tag="name")
    logo: Optional[networks.AnyUrl] = element(tag="logo", default=None)
    alt_identifier: Optional[list[networks.AnyUrl]] = element(tag="altIdentifier", default_factory=list)

    @field_validator("name", mode="before")
    def _validate_name(cls, value):
        """Ensure that name is a ResourceName or convert it to one."""
        if isinstance(value, str):
            value = ResourceName(value=value)
        return value

    @field_validator("alt_identifier", mode="before")
    def _validate_alt_identifier(cls, value):
        """Ensure that the alt_identifier is a list of strings."""
        if isinstance(value, str):
            value = [value]


class Relationship(BaseXmlModel, tag="relationship", nsmap=NSMAP):
    """A description of the relationship between one resource and one or more other resources.

    Parameters:
        relationship_type: (str):
            (element) - The named type of relationship

                The value  of relationshipType should be taken from the vocabulary at
                http://www.ivoa.net/rdf/voresource/relationship_type.
        related_resource: (list[ResourceName]):
            (element) - the name of resource that this resource is related to.
    """

    relationship_type: str = element(tag="relationshipType")

    related_resource: list[ResourceName] = element(tag="relatedResource")

    @field_validator("related_resource", mode="before")
    def _validate_related_resource(cls, value):
        """Ensure that the related_resource is a list of ResourceNames."""
        if isinstance(value, str):
            value = [ResourceName(value=value)]
        elif isinstance(value, ResourceName):
            value = [value]
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, str):
                    value[index] = ResourceName(value=item)
        return value


class SecurityMethod(BaseXmlModel, tag="securityMethod", nsmap=NSMAP):
    """A description of a security mechanism.

    This type only allows one to refer to the mechanism via a URI.  Derived types would allow for more metadata.

    Parameters:
        standard_id: (Optional[networks.AnyUrl]):
            (attr) - A URI identifier for a standard security mechanism.

                This provides a unique way to refer to a security specification standard. The use of an IVOA identifier
                here implies that a VOResource description of the standard is registered and accessible.
    """

    standard_id: Optional[networks.AnyUrl] = attr(name="standardID", default=None)


class Curation(BaseXmlModel, tag="curation", nsmap=NSMAP):
    """Information regarding the general curation of a resource

    Parameters:
        publisher: (ResourceName):
            (element) - Entity (e.g. person or organisation) responsible for making the resource available
        creator: (Optional[list[Creator]]):
            (element) - The entity/ies (e.g. person(s) or organisation) primarily responsible for creating the content
            or constitution of the resource.

                This is the equivalent of the author of a publication.
        contributor: (Optional[list[ResourceName]]):
            (element) - Entity responsible for contributions to the content of the resource
        date: (Optional[list[Date]]):
            (element) - Date associated with an event in the life cycle of the resource.

                This will typically be associated with the creation or  availability (i.e., most recent release or
                version) of the resource.  Use the role attribute to clarify.
        version: (Optional[str]):
            (element) - Label associated with creation or availablilty of a version of a resource.
        contact: (list[Contact]):
            (element) - Information that can be used for contacting someone with regard to this resource.
    """

    publisher: ResourceName = element(tag="publisher")
    creator: Optional[list[Creator]] = element(tag="creator", default_factory=list)
    contributor: Optional[list[ResourceName]] = element(tag="contributor", default_factory=list)
    date: Optional[list[Date]] = element(tag="date", default_factory=list)
    version: Optional[str] = element(tag="version", default=None)
    contact: list[Contact] = element(tag="contact")

    @field_validator("publisher", mode="before")
    def _validate_publisher(cls, value):
        """Ensure that publisher is a ResourceName or convert it to one."""
        if isinstance(value, str):
            value = ResourceName(value=value)
        return value

    @field_validator("creator", mode="before")
    def _validate_creator(cls, value):
        """Ensure that creator is a list of Creators."""
        if isinstance(value, Creator):
            value = [value]
        return value

    @field_validator("contributor", mode="before")
    def _validate_contributor(cls, value):
        """Ensure that contributor is a list of ResourceNames."""
        if isinstance(value, str):
            value = [ResourceName(value=value)]
        elif isinstance(value, ResourceName):
            value = [value]
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, str):
                    value[index] = ResourceName(value=item)
        return value

    @field_validator("date", mode="before")
    def _validate_date(cls, value):
        """Ensure that date is a list of Dates."""
        if not isinstance(value, list):
            value = [value]
        return value

    @field_validator("contact", mode="before")
    def _validate_contact(cls, value):
        """Ensure that contact is a list of Contacts."""
        if not isinstance(value, list):
            value = [value]
        return value


class Content(BaseXmlModel, tag="content", nsmap=NSMAP):
    """Information regarding the general content of a resource

    Parameters:
        subject: (list[str]):
            (element) - A topic, object type, or other descriptive keywords about the resource.
            Terms for Subject should be drawn from the Unified Astronomy Thesaurus (http://astrothesaurus.org).
        description: (str):
            (element) - An account of the nature of the resource.

                The description may include but is not limited to an abstract, table of contents, reference to a
                graphical representation of content or a free-text account of the content.
        source: (Optional[Source]):
            (element) - A bibliographic reference from which the present resource is derived or extracted.

                This is intended to point to an article in the published literature. An ADS Bibcode is recommended as a
                value when available.
        reference_url: (networks.AnyUrl):
            (element) - URL pointing to a human-readable document describing this resource.
        type: (Optional[list[str]]):
            (element) - Nature or genre of the content of the resource.

                Values for type should be taken from the controlled vocabulary
                http://www.ivoa.net/rdf/voresource/content_type
        content_level: (Optional[list[str]]):
            (element) - Description of the content level or intended audience.

                Values for contentLevel should be taken from the controlled vocabulary
                http://www.ivoa.net/rdf/voresource/content_level.
        relationship: (Optional[list[Relationship]]):
            (element) - a description of a relationship to another resource.
    """

    subject: list[str] = element(tag="subject")
    description: str = element(tag="description")
    source: Optional[Source] = element(tag="source", default=None)
    reference_url: networks.AnyUrl = element(tag="referenceURL")
    type: Optional[list[str]] = element(tag="type", default=None)
    content_level: Optional[list[str]] = element(tag="contentLevel", default_factory=list)
    relationship: Optional[list[Relationship]] = element(tag="relationship", default_factory=list)

    @field_validator("subject", mode="before")
    def _validate_subject(cls, value):
        """Ensure that subject is a list of strings."""
        if isinstance(value, str):
            value = [value]
        return value

    @field_validator("source", mode="before")
    def _validate_source(cls, value):
        """Ensure that source is a Source or convert it to one."""
        if isinstance(value, str):
            value = Source(value=value)
        return value

    @field_validator("type", mode="before")
    def _validate_type(cls, value):
        """Ensure that type is a list of strings."""
        if isinstance(value, str):
            value = [value]
        return value

    @field_validator("content_level", mode="before")
    def _validate_content_level(cls, value):
        """Ensure that content_level is a list of strings."""
        if isinstance(value, str):
            value = [value]
        return value

    @field_validator("relationship", mode="before")
    def _validate_relationship(cls, value):
        """Ensure that relationship is a list of Relationships."""
        if not isinstance(value, list):
            value = [value]
        return value


class Interface(BaseXmlModel, tag="interface", nsmap=NSMAP):

    """A description of a service interface.

    Since this type is abstract, one must use an Interface subclass to describe an actual interface.

    Additional interface subtypes (beyond WebService and WebBrowser) are defined in the VODataService schema.

    Parameters:
        version: (Optional[str]):
            (attr) - The version of a standard interface specification that this interface complies with.

                Most VO standards indicate the version in the standardID attribute of the capability.
                For these standards, the version attribute should not be used.
        role: (Optional[str]):
            (attr) - A tag name that identifies the role the interface plays in the particular capability.

                If the value is equal to 'std' or begins with 'std:', then the interface refers to a standard
                interface defined by the standard referred to by the capability's standardID attribute.
        type: (str):
            (attr) - The type of interface.

                This is set by the subclass of Interface using the Interface definition.
        access_url: (list[AccessURL]):
            (element) - The URL (or base URL) that a client uses to access the service.

                How this URL is to be interpreted and used depends on the specific Interface subclass
        mirror_url: (Optional[list[MirrorURL]]):
            (element) - A (base) URL of a mirror of this interface.

                As with accessURL, how this URL is to be interpreted and used depends on the specific Interface subclass
        security_method: (Optional[list[SecurityMethod]]):
            (element) - The mechanism the client must employ to authenticate to the service.
        test_querystring: (Optional[str]):
            (element) - Test data for exercising the service.
    """

    version: Optional[str] = attr(name="version", default=None)
    role: Optional[str] = attr(name="role", default=None)
    type: str = attr(name="type", default=None, ns="xsi")

    access_url: list[AccessURL] = element(tag="accessURL")
    mirror_url: Optional[list[MirrorURL]] = element(tag="mirrorURL", default_factory=list)
    security_method: Optional[list[SecurityMethod]] = element(tag="securityMethod", default_factory=list)
    test_querystring: Optional[str] = element(tag="testQueryString", default=None)

    @field_validator("access_url", mode="before")
    def _validate_access_url(cls, value):
        """Ensure that access_url is a list of AccessURLs."""
        if not isinstance(value, list):
            value = [value]
        return value

    @field_validator("mirror_url", mode="before")
    def _validate_mirror_url(cls, value):
        """Ensure that mirror_url is a list of MirrorURLs."""
        if not isinstance(value, list):
            value = [value]
        return value

    @field_validator("security_method", mode="before")
    def _validate_security_method(cls, value):
        """Ensure that security_method is a list of SecurityMethods."""
        if not isinstance(value, list):
            value = [value]
        return value


class WebBrowser(Interface, tag="interface", nsmap=NSMAP):
    """A (form-based) interface intended to be accesed interactively by a user via a web browser.

    Parameters:
        version: (Optional[str]):
            (attr) - The version of a standard interface specification that this interface complies with.

                Most VO standards indicate the version in the standardID attribute of the capability.
                For these standards, the version attribute should not be used.
        role: (Optional[str]):
            (attr) - A tag name that identifies the role the interface plays in the particular capability.

                If the value is equal to 'std' or begins with 'std:', then the interface refers to a standard
                interface defined by the standard referred to by the capability's standardID attribute.
        access_url: (list[AccessURL]):
            (element) - The URL (or base URL) that a client uses to access the service.

                How this URL is to be interpreted and used depends on the specific Interface subclass
        mirror_url: (Optional[list[MirrorURL]]):
            (element) - A (base) URL of a mirror of this interface.

                As with accessURL, how this URL is to be interpreted and used depends on the specific Interface subclass
        security_method: (Optional[list[SecurityMethod]]):
            (element) - The mechanism the client must employ to authenticate to the service.
        test_querystring: (Optional[str]):
            (element) - Test data for exercising the service.
    """

    type: Optional[Literal["vr:WebBrowser"]] = attr(name="type", default="vr:WebBrowser", ns="xsi")


class WebService(Interface, nsmap=NSMAP):
    """A Web Service that is describable by a WSDL document.

    The accessURL element gives the Web Service's endpoint URL.

    Parameters:
        wsdl_url: (Optional[list[networks.AnyUrl]]):
            (element) - The location of the WSDL that describes this Web Service.

                If not provided, the location is assumed to be the accessURL with "?wsdl" appended.
                Multiple occurrences should represent mirror copies of the same WSDL file.
        version: (Optional[str]):
            (attr) - The version of a standard interface specification that this interface complies with.

                Most VO standards indicate the version in the standardID attribute of the capability.
                For these standards, the version attribute should not be used.
        role: (Optional[str]):
            (attr) - A tag name that identifies the role the interface plays in the particular capability.

                If the value is equal to 'std' or begins with 'std:', then the interface refers to a standard
                interface defined by the standard referred to by the capability's standardID attribute.
        access_url: (list[AccessURL]):
            (element) - The URL (or base URL) that a client uses to access the service.

                How this URL is to be interpreted and used depends on the specific Interface subclass
        mirror_url: (Optional[list[MirrorURL]]):
            (element) - A (base) URL of a mirror of this interface.

                As with accessURL, how this URL is to be interpreted and used depends on the specific Interface subclass
        security_method: (Optional[list[SecurityMethod]]):
            (element) - The mechanism the client must employ to authenticate to the service.
        test_querystring: (Optional[str]):
            (element) - Test data for exercising the service.
    """

    type: Optional[Literal["vr:WebService"]] = attr(name="type", default="vr:WebService", ns="xsi")

    wsdl_url: Optional[list[networks.AnyUrl]] = element(tag="wsdlURL", default_factory=list)

    @field_validator("wsdl_url", mode="before")
    def _validate_wsdl_url(cls, value):
        """Ensure that wsdl_url is a list of networks.AnyUrls."""
        if not isinstance(value, list):
            value = [value]
        return value


class Resource(BaseXmlModel, tag="resource", nsmap=NSMAP):
    """Any entity or component of a VO application that is describable and identifiable by an IVOA Identifier.

    Parameters:
        created: (UTCTimestamp):
            (attr) - The UTC date and time this resource metadata description was created.

                This timestamp must not be in the future.  This time is not required to be accurate; it should be at
                least accurate to the day.  Any non-significant time fields should be set to zero.
        updated: (UTCTimestamp):
            (attr) - The UTC date this resource metadata description was last updated.

                This timestamp must not be in the future.  This time is not required to be accurate; it should be at
                least accurate to the day.  Any non-significant time fields should be set to zero.
        status: (Literal["active", "inactive", "deleted"]):
            (attr) - A tag indicating whether this resource is believed to be still actively maintained.

                "active" -  Resource is believed to be currently maintained, and its description is up to date (default)
                "inactive" - Resource is apparently not being maintained at the present
                "deleted" - Resource publisher has explicitly deleted the resource.
        version: (Optional[str]):
            (attr) - The VOResource XML schema version against which this instance was written.

                Implementors should set this to the value of the version attribute of their schema's root (xs:schema)
                element. Clients may assume version 1.0 if this attribute is missing.
        validation_level: (Optional[list[Validation]]):
            (element) - A numeric grade describing the quality of the resource description, when applicable, to be used
            to indicate the confidence an end-user can put in the resource as part of a VO application or research
            study.
        title: (str):
            (element) - The full name given to the resource
        short_name: (Optional[str]):
            (element) - A short name or abbreviation given to the resource.
            One word or a few letters is recommended.  No more than sixteen characters are allowed.
        identifier: (networks.AnyUrl):
            (element) - Unambiguous reference to the resource conforming to the IVOA standard for identifiers
        alt_identifier: (Optional[list[networks.AnyUrl]]):
            (element) - A reference to this resource in a non-IVOA identifier scheme, e.g., DOI or bibcode. Always use
            the an URI scheme here, e.g., bibcode:2008ivoa.spec.0222P.
        curation: (Curation):
            (element) - Information regarding the general curation of the resource
        content: (Content):
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
    def _validate_timestamps(cls, value):
        """Ensure that the created and updated timestamps are not in the future"""
        if value > datetime.datetime.now(tz=datetime.timezone.utc):
            raise ValueError("Timestamps must not be in the future")
        return value

    @field_validator("short_name")
    def _validate_short_name(cls, value):
        """Ensure that the short name is no more than 16 characters"""
        if value and len(value) > 16:
            raise ValueError("Short name must be no more than 16 characters")
        return value

    @field_validator("validation_level", mode="before")
    def _validate_validation_level(cls, value):
        """Ensure that validation_level is a list of Validations."""
        if not isinstance(value, list):
            value = [value]
        return value

    @field_validator("alt_identifier", mode="before")
    def _validate_alt_identifier(cls, value):
        """Ensure that alt_identifier is a list of networks.AnyUrls."""
        if not isinstance(value, list):
            value = [value]
        return value


class Organisation(Resource, tag="organisation", nsmap=NSMAP):
    """A named group of one or more persons brought together to pursue participation in VO applications.

    Parameters:
        created: (UTCTimestamp):
            (attr) - The UTC date and time this resource metadata description was created.
        updated: (UTCTimestamp):
            (attr) - The UTC date this resource metadata description was last updated.
        status: (str):
            (attr) - a tag indicating whether this resource is believed to be still actively maintained.
        version: (Optional[str]):
            (attr) - The VOResource XML schema version against which this instance was written.

                Implementors should set this to the value of the version attribute of their schema's root (xs:schema)
                element. Clients may assume version 1.0 if this attribute is missing.
        facility: (Optional[list[ResourceName]]):
            (element) - The observatory or facility used to collect the data contained or managed by this resource.
        instrument: Optional[list[ResourceName]]):
            (element) - The instrument used to collect the data contained or managed by a resource.

    """

    created: UTCTimestamp = attr(name="created")
    updated: UTCTimestamp = attr(name="updated")
    status: str = attr(name="status")
    version: Optional[str] = attr(name="version", default=None)

    facility: Optional[list[ResourceName]] = element(tag="facility", default_factory=list)
    instrument: Optional[list[ResourceName]] = element(tag="instrument", default_factory=list)

    @field_validator("facility", mode="before")
    def _validate_facility(cls, value):
        """Ensure that facility is a list of ResourceNames."""
        if not isinstance(value, list):
            if isinstance(value, str):
                value = [ResourceName(value=value)]
            else:
                value = [value]
        return value

    @field_validator("instrument", mode="before")
    def _validate_instrument(cls, value):
        """Ensure that instrument is a list of ResourceNames."""
        if not isinstance(value, list):
            if isinstance(value, str):
                value = [ResourceName(value=value)]
            else:
                value = [value]
        return value


class Capability(BaseXmlModel, tag="capability", nsmap=NSMAP):
    """A description of what the service does (in terms of context-specific behavior), and how to use it
    (in terms of an interface)

    Parameters:
        standard_id: (Optional[networks.AnyUrl]):
            (attr) - A URI identifier for a standard service.

                This provides a unique way to refer to a service specification standard, such as a Simple Image Access
                service. The use of an IVOA identifier here implies that a VOResource description of the standard is
                registered and accessible.
        validation_level: (Optional[list[Validation]]):
            (element) - A numeric grade describing the quality of the capability description and interface, when
            applicable, to be used to indicate the confidence an end-user can put in the resource as part of a
            VO application or research study.

                See ValidationLevel for an explanation of the allowed levels.
        description: (Optional[str]):
            (element) - A human-readable description of what this capability provides as part of the over-all service.

                Use of this optional element is especially encouraged when this capability is non-standard and is one
                of several capabilities listed.
        interface: (Optional[list[Interface]]):
            (element) - A description of how to call the service to access this capability.

                Since the Interface type is abstract, one must describe the interface using a subclass of Interface,
                denoting it via xsi:type.
    """

    standard_id: Optional[networks.AnyUrl] = attr(name="standardID", default=None)

    validation_level: Optional[list[Validation]] = element(tag="validationLevel", default_factory=list)
    description: Optional[str] = element(tag="description", default=None)
    interface: Optional[list[Interface]] = element(tag="interface", default_factory=list)

    @field_validator("validation_level", mode="before")
    def _validate_validation_level(cls, value):
        """Ensure that validation_level is a list of Validations."""
        if not isinstance(value, list):
            value = [value]
        return value

    @field_validator("interface", mode="before")
    def _validate_interface(cls, value):
        """Ensure that interface is a list of Interfaces."""
        if not isinstance(value, list):
            value = [value]
        return value


class Service(Resource, tag="service", nsmap=NSMAP):
    """A resource that can be invoked by a client to perform some action on its behalf.

    Parameters:
        created: (UTCTimestamp):
            (attr) - The UTC date and time this resource metadata description was created.
        updated: (UTCTimestamp):
            (attr) - The UTC date this resource metadata description was last updated.
        status: (str):
            (attr) - A tag indicating whether this resource is believed to be still actively maintained.
        version: (Optional[str]):
            (attr) - The VOResource XML schema version against which this instance was written.

                Implementors should set this to the value of the version attribute of their schema's root (xs:schema)
                element. Clients may assume version 1.0 if this attribute is missing.
        rights: (Optional[list[Rights]]):
            (element) - Information about rights held in and over the resource.

                Mainly for compatibility with DataCite, this elementis repeatable.  Resource record authors are advised
                that within the Virtual Observatory clients will typically only display and/or use the rights element
                occurring first and ignore later elements.
        capability: (Optional[list[Capability]]):
            (element) - A description of a general capability of the service and how to use it.

                This describes a general function of the service, usually in terms of a standard service protocol
                (e.g. SIA), but not necessarily so.

                A service can have many capabilities associated with it, each reflecting different aspects of the
                functionality it provides.
    """

    created: UTCTimestamp = attr(name="created")
    updated: UTCTimestamp = attr(name="updated")
    status: str = attr(name="status")
    version: Optional[str] = attr(name="version", default=None)

    rights: Optional[list[Rights]] = element(tag="rights", default_factory=list)
    capability: Optional[list[Capability]] = element(tag="capability", default_factory=list)

    @field_validator("rights", mode="before")
    def _validate_rights(cls, value):
        """Ensure that rights is a list of Rights."""
        if not isinstance(value, list):
            if isinstance(value, str):
                value = Rights(value=value)
            value = [value]
        return value

    @field_validator("capability", mode="before")
    def _validate_capability(cls, value):
        """Ensure that capability is a list of Capabilities."""
        if not isinstance(value, list):
            value = [value]
        return value