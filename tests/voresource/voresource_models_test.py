"""Tests for VOResource models."""

from unittest import TestCase
from xml.etree.ElementTree import canonicalize

from lxml import etree

from vo_models.voresource import (
    AccessURL,
    Capability,
    Contact,
    Content,
    Creator,
    Curation,
    Date,
    Interface,
    MirrorURL,
    Organisation,
    Relationship,
    Resource,
    ResourceName,
    Rights,
    SecurityMethod,
    Service,
    Source,
    Validation,
    WebService,
)
from vo_models.voresource.types import UTCDateTime

VORESOURCE_NAMESPACE_HEADER = """
    xmlns:xml="http://www.w3.org/XML/1998/namespace",
    xmlns="http://www.w3.org/2001/XMLSchema",
    xmlns:xs="http://www.w3.org/2001/XMLSchema",
    xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0",
    xmlns:vm="http://www.ivoa.net/xml/VOMetadata/v0.1",
"""


class TestValidation(TestCase):
    """Test VOResource Validation model."""

    test_validation_model = Validation(value=0, validated_by="https://example.edu")
    test_validation_xml = '<vr:validation xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" validatedBy="https://example.edu">0</vr:validation>'

    def test_read_from_xml(self):
        """Test reading from XML."""
        validation = Validation.from_xml(self.test_validation_xml)
        self.assertEqual(validation.value, 0)
        self.assertEqual(validation.validated_by, "https://example.edu")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_validation_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_validation_xml), strip_text=True, strip_comments=True),
        )


class TestResourceName(TestCase):
    """Test VOResource ResourceName model."""

    test_resource_name_model = ResourceName(value="Example Resource", ivo_id="ivo://example.edu/resource")
    test_resource_name_xml = '<vr:ResourceName xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" ivo-id="ivo://example.edu/resource">Example Resource</vr:ResourceName>'

    def test_read_from_xml(self):
        """Test reading from XML."""
        resource_name = ResourceName.from_xml(self.test_resource_name_xml)
        self.assertEqual(resource_name.value, "Example Resource")
        self.assertEqual(resource_name.ivo_id, "ivo://example.edu/resource")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_resource_name_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_resource_name_xml), strip_text=True, strip_comments=True),
        )


class TestDate(TestCase):
    """Test VOResource Date model"""

    test_date_model = Date(value="2021-01-01T00:00:00Z", role="update")
    test_date_xml = (
        '<vr:date xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" role="update">2021-01-01T00:00:00Z</vr:date>'
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        date = Date.from_xml(self.test_date_xml)
        self.assertEqual(date.value, "2021-01-01T00:00:00Z")
        self.assertEqual(date.role, "update")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_date_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_date_xml), strip_text=True, strip_comments=True),
        )


class TestSource(TestCase):
    """Test VOResource Source model"""

    test_source_model = Source(value="https://example.edu", format="bibcode")
    test_source_xml = (
        '<vr:source xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" format="bibcode">https://example.edu</vr:source>'
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        source = Source.from_xml(self.test_source_xml)
        self.assertEqual(source.value, "https://example.edu")
        self.assertEqual(source.format, "bibcode")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_source_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_source_xml), strip_text=True, strip_comments=True),
        )


class TestRights(TestCase):
    """Test VOResource Rights model"""

    test_rights_model = Rights(value="CC BY 4.0", rights_uri="https://creativecommons.org/licenses/by/4.0/")
    test_rights_xml = '<vr:rights xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" rights_uri="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</vr:rights>'

    def test_read_from_xml(self):
        """Test reading from XML."""
        rights = Rights.from_xml(self.test_rights_xml)
        self.assertEqual(rights.value, "CC BY 4.0")
        self.assertEqual(rights.rights_uri, "https://creativecommons.org/licenses/by/4.0/")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_rights_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_rights_xml), strip_text=True, strip_comments=True),
        )


class TestAccessURL(TestCase):
    """Test VOResource AccessURL model"""

    test_access_url_model = AccessURL(value="https://example.edu", use="full")
    test_access_url_xml = (
        '<vr:accessURL xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" use="full">https://example.edu</vr:accessURL>'
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        access_url = AccessURL.from_xml(self.test_access_url_xml)
        self.assertEqual(access_url.value, "https://example.edu")
        self.assertEqual(access_url.use, "full")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_access_url_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_access_url_xml), strip_text=True, strip_comments=True),
        )


class TestMirrorURL(TestCase):
    """Test VOResource MirrorURL model"""

    test_mirror_url_model = MirrorURL(value="https://example.edu", title="Mirror")
    test_mirror_url_xml = '<vr:mirrorURL xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" title="Mirror">https://example.edu</vr:mirrorURL>'

    def test_read_from_xml(self):
        """Test reading from XML."""
        mirror_url = MirrorURL.from_xml(self.test_mirror_url_xml)
        self.assertEqual(mirror_url.value, "https://example.edu")
        self.assertEqual(mirror_url.title, "Mirror")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_mirror_url_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_mirror_url_xml), strip_text=True, strip_comments=True),
        )


class TestContact(TestCase):
    """Test VOResource Contact model"""

    test_contact_model = Contact(
        name="John Doe",
        address="1234 Example St.",
        email="jdoe@mail.com",
        telephone="555-555-5555",
        alt_identifier=["http://orcid.org/0000-0001-9718-6515"],
    )
    test_contact_xml = (
        '<vr:contact xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0">'
        "<name>John Doe</name>"
        "<address>1234 Example St.</address>"
        "<email>jdoe@mail.com</email>"
        "<telephone>555-555-5555</telephone>"
        "<altIdentifier>http://orcid.org/0000-0001-9718-6515</altIdentifier>"
        "</vr:contact>"
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        contact = Contact.from_xml(self.test_contact_xml)
        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.address, "1234 Example St.")
        self.assertEqual(contact.email, "jdoe@mail.com")
        self.assertEqual(contact.telephone, "555-555-5555")
        self.assertEqual(contact.alt_identifier, ["http://orcid.org/0000-0001-9718-6515"])

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_contact_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_contact_xml), strip_text=True, strip_comments=True),
        )


class TestCreator(TestCase):
    """Test VOResource Creator model"""

    test_creator_model = Creator(name="Doe, J.", logo="https://example.edu/logo.png")
    test_creator_xml = (
        '<vr:creator xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0">'
        "<name>Doe, J.</name>"
        "<logo>https://example.edu/logo.png</logo>"
        "</vr:creator>"
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        creator = Creator.from_xml(self.test_creator_xml)
        self.assertEqual(creator.name, "Doe, J.")
        self.assertEqual(creator.logo, "https://example.edu/logo.png")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_creator_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_creator_xml), strip_text=True, strip_comments=True),
        )


class TestRelationship(TestCase):
    """Test VOResource Relationship model"""

    test_relationship_model = Relationship(
        relationship_type="isPartOf",
        related_resource=[ResourceName(value="Example Resource", ivo_id="ivo://example.edu/resource")],
    )
    test_relationship_xml = (
        '<vr:relationship xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0">'
        "<relationshipType>isPartOf</relationshipType>"
        '<related_resource ivo-id="ivo://example.edu/resource">Example Resource</related_resource>'
        "</vr:relationship>"
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        relationship = Relationship.from_xml(self.test_relationship_xml)
        self.assertEqual(relationship.relationship_type, "isPartOf")
        self.assertEqual(relationship.related_resource[0].value, "Example Resource")
        self.assertEqual(relationship.related_resource[0].ivo_id, "ivo://example.edu/resource")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_relationship_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_relationship_xml), strip_text=True, strip_comments=True),
        )


class TestSecurityMethod(TestCase):
    """Test VOResource SecurityMethod model"""

    test_security_method_model = SecurityMethod(standard_id="ivo://ivoa.net/std/Security#basic")
    test_security_method_xml = '<vr:securityMethod xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" standardID="ivo://ivoa.net/std/Security#basic"/>'

    def test_read_from_xml(self):
        """Test reading from XML."""
        security_method = SecurityMethod.from_xml(self.test_security_method_xml)
        self.assertEqual(security_method.standard_id, "ivo://ivoa.net/std/Security#basic")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_security_method_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_security_method_xml), strip_text=True, strip_comments=True),
        )


class TestCuration(TestCase):
    """Test VOResource Curation model"""

    test_curation_model = Curation(
        publisher=ResourceName(value="STScI"),
        creator=[Creator(name="Doe, J.")],
        contributor=[ResourceName(value="Example Resource")],
        date=[Date(value="2021-01-01T00:00:00Z", role="update")],
        version="1.0",
        contact=[Contact(name="John Doe")],
    )

    test_curation_xml = (
        '<vr:curation xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0">'
        "<publisher>STScI</publisher>"
        "<creator><name>Doe, J.</name></creator>"
        "<contributor>Example Resource</contributor>"
        '<date role="update">2021-01-01T00:00:00Z</date>'
        "<version>1.0</version>"
        "<contact><name>John Doe</name></contact>"
        "</vr:curation>"
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        curation = Curation.from_xml(self.test_curation_xml)
        self.assertEqual(curation.publisher.value, "STScI")
        self.assertEqual(curation.creator[0].name, "Doe, J.")
        self.assertEqual(curation.contributor[0].value, "Example Resource")
        self.assertEqual(curation.date[0].value, "2021-01-01T00:00:00Z")
        self.assertEqual(curation.date[0].role, "update")
        self.assertEqual(curation.version, "1.0")
        self.assertEqual(curation.contact[0].name, "John Doe")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_curation_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_curation_xml), strip_text=True, strip_comments=True),
        )


class TestContent(TestCase):
    """Test VOResource Content model"""

    test_content_model = Content(
        subject="Astronomy",
        description="Example description",
        source=[Source(value="https://example.edu", format="bibcode")],
        reference_url="https://example.edu",
        type="Education",
        content_level="General",
        relationship=[
            Relationship(
                relationship_type="isPartOf",
                related_resource=[ResourceName(value="Example Resource", ivo_id="ivo://example.edu/resource")],
            )
        ],
    )

    test_content_xml = (
        '<vr:content xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0">'
        "<subject>Astronomy</subject>"
        "<description>Example description</description>"
        '<source format="bibcode">https://example.edu</source>'
        "<referenceURL>https://example.edu</referenceURL>"
        "<type>Education</type>"
        "<contentLevel>General</contentLevel>"
        '<relationship xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0">'
        "<relationshipType>isPartOf</relationshipType>"
        '<related_resource ivo-id="ivo://example.edu/resource">Example Resource</related_resource>'
        "</relationship>"
        "</vr:content>"
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        content = Content.from_xml(self.test_content_xml)
        self.assertEqual(content.subject, "Astronomy")
        self.assertEqual(content.description, "Example description")
        self.assertEqual(content.source[0].value, "https://example.edu")
        self.assertEqual(content.source[0].format, "bibcode")
        self.assertEqual(content.reference_url, "https://example.edu")
        self.assertEqual(content.type, "Education")
        self.assertEqual(content.content_level, "General")
        self.assertEqual(content.relationship[0].relationship_type, "isPartOf")
        self.assertEqual(content.relationship[0].related_resource[0].value, "Example Resource")
        self.assertEqual(content.relationship[0].related_resource[0].ivo_id, "ivo://example.edu/resource")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_content_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_content_xml), strip_text=True, strip_comments=True),
        )


class TestInterface(TestCase):
    """Test the VOResource Interface model."""

    test_interface_model = Interface(
        version="1.0",
        role="std",
        access_url=[AccessURL(value="https://example.edu", use="full")],
        mirror_url=[MirrorURL(value="https://example.edu", title="Mirror")],
        security_method=[SecurityMethod(standard_id="ivo://ivoa.net/std/Security#basic")],
        test_querystring="test",
    )
    test_interface_xml = (
        '<vr:interface xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" role="std" version="1.0">'
        '<accessURL use="full">https://example.edu</accessURL>'
        '<mirrorURL title="Mirror">https://example.edu</mirrorURL>'
        '<securityMethod standardID="ivo://ivoa.net/std/Security#basic"/>'
        "<testQuerystring>test</testQuerystring>"
        "</vr:interface>"
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        interface = Interface.from_xml(self.test_interface_xml)
        self.assertEqual(interface.version, "1.0")
        self.assertEqual(interface.role, "std")
        self.assertEqual(interface.access_url[0].value, "https://example.edu")
        self.assertEqual(interface.access_url[0].use, "full")
        self.assertEqual(interface.mirror_url[0].value, "https://example.edu")
        self.assertEqual(interface.mirror_url[0].title, "Mirror")
        self.assertEqual(interface.security_method[0].standard_id, "ivo://ivoa.net/std/Security#basic")
        self.assertEqual(interface.test_querystring, "test")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_interface_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_interface_xml), strip_text=True, strip_comments=True),
        )


class TestWebService(TestCase):
    """Test the VOResource WebService model."""

    test_web_service_model = WebService(
        wsdl_url="https://example.edu/wsdl",
        access_url="https://example.edu",
    )
    test_web_service_xml = (
        '<vr:webService xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0">'
        "<wsdlURL>https://example.edu/wsdl</wsdlURL>"
        "<accessURL>https://example.edu</accessURL>"
        "</vr:webService>"
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        web_service = WebService.from_xml(self.test_web_service_xml)
        self.assertEqual(web_service.wsdl_url, "https://example.edu/wsdl")
        self.assertEqual(web_service.access_url, "https://example.edu")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_web_service_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_web_service_xml), strip_text=True, strip_comments=True),
        )

class TestResource(TestCase):
    """Test the VOResource Resource model."""

    test_resource_model = Resource(
        created = UTCDateTime("1996-03-11T19:00:00Z"),
        updated = UTCDateTime("1996-03-11T19:00:00Z"),
        status = "active",
        version = "1.0",
        validation_level = [Validation(value=0, validated_by="https://example.edu")],
        title = "Example Resource",
        short_name = "example",
        identifier = "https://example.edu",
        alt_identifier = ["bibcode:2008ivoa.spec.0222P"],
        curation = Curation(
            publisher=ResourceName(value="STScI"),
            creator=[Creator(name="Doe, J.")],
            contributor=[ResourceName(value="Example Resource")],
            date=[Date(value="2021-01-01T00:00:00Z", role="update")],
            version="1.0",
            contact=[Contact(name="John Doe")],
        ),
        content = Content(
            subject="Astronomy",
            description="Example description",
            source=[Source(value="https://example.edu", format="bibcode")],
            reference_url="https://example.edu",
            type="Education",
            content_level="General",
            relationship=[
                Relationship(
                    relationship_type="isPartOf",
                    related_resource=[ResourceName(value="Example Resource", ivo_id="ivo://example.edu/resource")],
                )
            ],
        ),
    )

    test_resource_xml = (
        '<vr:resource xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" status="active" version="1.0">'
        '<created>1996-03-11T19:00:00Z</created>'
        '<updated>1996-03-11T19:00:00Z</updated>'
        '<validation validatedBy="https://example.edu">0</validation>'
        '<title>Example Resource</title>'
        '<shortName>example</shortName>'
        '<identifier>https://example.edu</identifier>'
        '<altIdentifier>bibcode:2008ivoa.spec.0222P</altIdentifier>'
        '<curation>'
        '<publisher>STScI</publisher>'
        '<creator><name>Doe, J.</name></creator>'
        '<contributor>Example Resource</contributor>'
        '<date role="update">2021-01-01T00:00:00Z</date>'
        '<version>1.0</version>'
        '<contact><name>John Doe</name></contact>'
        '</curation>'
        '<content>'
        '<subject>Astronomy</subject>'
        '<description>Example description</description>'
        '<source format="bibcode">https://example.edu</source>'
        '<referenceURL>https://example.edu</referenceURL>'
        '<type>Education</type>'
        '<contentLevel>General</contentLevel>'
        '<relationship>'
        '<relationshipType>isPartOf</relationshipType>'
        '<related_resource ivo-id="ivo://example.edu/resource">Example Resource</related_resource>'
        '</relationship>'
        '</content>'
        '</vr:resource>'
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        resource = Resource.from_xml(self.test_resource_xml)
        self.assertEqual(resource.created, UTCDateTime("1996-03-11T19:00:00Z"))
        self.assertEqual(resource.updated, UTCDateTime("1996-03-11T19:00:00Z"))
        self.assertEqual(resource.status, "active")
        self.assertEqual(resource.version, "1.0")
        self.assertEqual(resource.validation_level[0].value, 0)
        self.assertEqual(resource.validation_level[0].validated_by, "https://example.edu")
        self.assertEqual(resource.title, "Example Resource")
        self.assertEqual(resource.short_name, "example")
        self.assertEqual(resource.identifier, "https://example.edu")
        self.assertEqual(resource.alt_identifier, ["bibcode:2008ivoa.spec.0222P"])
        self.assertEqual(resource.curation.publisher.value, "STScI")
        self.assertEqual(resource.curation.creator[0].name, "Doe, J.")
        self.assertEqual(resource.curation.contributor[0].value, "Example Resource")
        self.assertEqual(resource.curation.date[0].value, "2021-01-01T00:00:00Z")
        self.assertEqual(resource.curation.date[0].role, "update")
        self.assertEqual(resource.curation.version, "1.0")
        self.assertEqual(resource.curation.contact[0].name, "John Doe")
        self.assertEqual(resource.content.subject, "Astronomy")
        self.assertEqual(resource.content.description, "Example description")
        self.assertEqual(resource.content.source[0].value, "https://example.edu")
        self.assertEqual(resource.content.source[0].format, "bibcode")
        self.assertEqual(resource.content.reference_url, "https://example.edu")
        self.assertEqual(resource.content.type, "Education")
        self.assertEqual(resource.content.content_level, "General")
        self.assertEqual(resource.content.relationship[0].relationship_type, "isPartOf")
        self.assertEqual(resource.content.relationship[0].related_resource[0].value, "Example Resource")
        self.assertEqual(resource.content.relationship[0].related_resource[0].ivo_id, "ivo://example.edu/resource")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_resource_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_resource_xml), strip_text=True, strip_comments=True),
        )

class TestOrganization(TestCase):
    """Test the VOResource Organization model."""

    test_organization_model = Organisation(
        created = UTCDateTime("1996-03-11T19:00:00Z"),
        updated = UTCDateTime("1996-03-11T19:00:00Z"),
        status = "active",
        version = "1.0",
        facility = [ResourceName(value="Example Facility", ivo_id="ivo://example.edu/facility")],
        instrument = [ResourceName(value="Example Instrument", ivo_id="ivo://example.edu/instrument")],
    )

    test_organization_xml = (
        '<vr:organization xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" status="active" version="1.0">'
        '<created>1996-03-11T19:00:00Z</created>'
        '<updated>1996-03-11T19:00:00Z</updated>'
        '<facility ivo-id="ivo://example.edu/facility">Example Facility</facility>'
        '<instrument ivo-id="ivo://example.edu/instrument">Example Instrument</instrument>'
        '</vr:organization>'
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        organization = Organisation.from_xml(self.test_organization_xml)
        self.assertEqual(organization.created, UTCDateTime("1996-03-11T19:00:00Z"))
        self.assertEqual(organization.updated, UTCDateTime("1996-03-11T19:00:00Z"))
        self.assertEqual(organization.status, "active")
        self.assertEqual(organization.version, "1.0")
        self.assertEqual(organization.facility[0].value, "Example Facility")
        self.assertEqual(organization.facility[0].ivo_id, "ivo://example.edu/facility")
        self.assertEqual(organization.instrument[0].value, "Example Instrument")
        self.assertEqual(organization.instrument[0].ivo_id, "ivo://example.edu/instrument")

    def test_write_to_xml(self):
        """Test writing to XML."""

        xml = self.test_organization_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_organization_xml), strip_text=True, strip_comments=True),
        )

class TestCapability(TestCase):
    """Test the VOResource Capability model."""

    test_capability_model = Capability(
        standard_id = "ivo://ivoa.net/std/TAP",
        validation_level = [Validation(value=0, validated_by="https://example.edu")],
        description = "Example description",
        interface = [Interface(version="1.0", role="std")],
    )

    test_capability_xml = (
        '<vr:capability xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" standardID="ivo://ivoa.net/std/TAP">'
        '<validation validatedBy="https://example.edu">0</validation>'
        '<description>Example description</description>'
        '<interface role="std" version="1.0"/>'
        '</vr:capability>'
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        capability = Capability.from_xml(self.test_capability_xml)
        self.assertEqual(capability.standard_id, "ivo://ivoa.net/std/TAP")
        self.assertEqual(capability.validation_level[0].value, 0)
        self.assertEqual(capability.validation_level[0].validated_by, "https://example.edu")
        self.assertEqual(capability.description, "Example description")
        self.assertEqual(capability.interface[0].version, "1.0")
        self.assertEqual(capability.interface[0].role, "std")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_capability_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_capability_xml), strip_text=True, strip_comments=True),
        )

class TestService(TestCase):
    """Test the VOResource Service model."""

    test_service_model = Service(
        created = UTCDateTime("1996-03-11T19:00:00Z"),
        updated = UTCDateTime("1996-03-11T19:00:00Z"),
        status = "active",
        version = "1.0",
        capability = [Capability(standard_id="ivo://ivoa.net/std/TAP")],
        interface = [Interface(version="1.0", role="std")],
        title = "Example Service",
        short_name = "example",
        identifier = "https://example.edu",
        alt_identifier = ["bibcode:2008ivoa.spec.0222P"],
        curation = Curation(
            publisher=ResourceName(value="STScI"),
            creator=[Creator(name="Doe, J.")],
            contributor=[ResourceName(value="Example Resource")],
            date=[Date(value="2021-01-01T00:00:00Z", role="update")],
            version="1.0",
            contact=[Contact(name="John Doe")],
        ),
        content = Content(
            subject="Astronomy",
            description="Example description",
            source=[Source(value="https://example.edu", format="bibcode")],
            reference_url="https://example.edu",
            type="Education",
            content_level="General",
            relationship=[
                Relationship(
                    relationship_type="isPartOf",
                    related_resource=[ResourceName(value="Example Resource", ivo_id="ivo://example.edu/resource")],
                )
            ],
        ),
    )

    test_service_xml = (
        '<vr:service xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" status="active" version="1.0">'
        '<created>1996-03-11T19:00:00Z</created>'
        '<updated>1996-03-11T19:00:00Z</updated>'
        '<capability standardID="ivo://ivoa.net/std/TAP"/>'
        '<interface role="std" version="1.0"/>'
        '<title>Example Service</title>'
        '<shortName>example</shortName>'
        '<identifier>https://example.edu</identifier>'
        '<altIdentifier>bibcode:2008ivoa.spec.0222P</altIdentifier>'
        '<curation>'
        '<publisher>STScI</publisher>'
        '<creator><name>Doe, J.</name></creator>'
        '<contributor>Example Resource</contributor>'
        '<date role="update">2021-01-01T00:00:00Z</date>'
        '<version>1.0</version>'
        '<contact><name>John Doe</name></contact>'
        '</curation>'
        '<content>'
        '<subject>Astronomy</subject>'
        '<description>Example description</description>'
        '<source format="bibcode">https://example.edu</source>'
        '<referenceURL>https://example.edu</referenceURL>'
        '<type>Education</type>'
        '<contentLevel>General</contentLevel>'
        '<relationship>'
        '<relationshipType>isPartOf</relationshipType>'
        '<related_resource ivo-id="ivo://example.edu/resource">Example Resource</related_resource>'
        '</relationship>'
        '</content>'
        '</vr:service>'
    )

    def test_read_from_xml(self):
        """Test reading from XML."""
        service = Service.from_xml(self.test_service_xml)
        self.assertEqual(service.created, UTCDateTime("1996-03-11T19:00:00Z"))
        self.assertEqual(service.updated, UTCDateTime("1996-03-11T19:00:00Z"))
        self.assertEqual(service.status, "active")
        self.assertEqual(service.version, "1.0")
        self.assertEqual(service.capability[0].standard_id, "ivo://ivoa.net/std/TAP")
        self.assertEqual(service.interface[0].version, "1.0")
        self.assertEqual(service.interface[0].role, "std")
        self.assertEqual(service.title, "Example Service")
        self.assertEqual(service.short_name, "example")
        self.assertEqual(service.identifier, "https://example.edu")
        self.assertEqual(service.alt_identifier, ["bibcode:2008ivoa.spec.0222P"])
        self.assertEqual(service.curation.publisher.value, "STScI")
        self.assertEqual(service.curation.creator[0].name, "Doe, J.")
        self.assertEqual(service.curation.contributor[0].value, "Example Resource")
        self.assertEqual(service.curation.date[0].value, "2021-01-01T00:00:00Z")
        self.assertEqual(service.curation.date[0].role, "update")
        self.assertEqual(service.curation.version, "1.0")
        self.assertEqual(service.curation.contact[0].name, "John Doe")
        self.assertEqual(service.content.subject, "Astronomy")
        self.assertEqual(service.content.description, "Example description")
        self.assertEqual(service.content.source[0].value, "https://example.edu")
        self.assertEqual(service.content.source[0].format, "bibcode")
        self.assertEqual(service.content.reference_url, "https://example.edu")
        self.assertEqual(service.content.type, "Education")
        self.assertEqual(service.content.content_level, "General")
        self.assertEqual(service.content.relationship[0].relationship_type, "isPartOf")
        self.assertEqual(service.content.relationship[0].related_resource[0].value, "Example Resource")
        self.assertEqual(service.content.relationship[0].related_resource[0].ivo_id, "ivo://example.edu/resource")

    def test_write_to_xml(self):
        """Test writing to XML."""
        xml = self.test_service_model.to_xml()
        self.assertEqual(
            canonicalize(xml, strip_text=True, strip_comments=True),
            canonicalize(etree.fromstring(self.test_service_xml), strip_text=True, strip_comments=True),
        )
