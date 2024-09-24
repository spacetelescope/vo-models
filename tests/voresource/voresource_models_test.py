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
    WebBrowser,
    WebService,
)

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

