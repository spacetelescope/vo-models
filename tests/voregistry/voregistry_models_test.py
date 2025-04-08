"""Tests for VORegistry models."""

from unittest import TestCase
from datetime import datetime, timezone as tz
from xml.etree.ElementTree import canonicalize

from vo_models.voregistry.models import Registry, Harvest, Search, OAIHTTP, OAISOAP, Authority
from vo_models.voresource.types import UTCDateTime, UTCTimestamp, ValidationLevel
from vo_models.voresource.models import (
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

VOREGISTRY_NAMESPACE_HEADER = """
    xmlns:ri="http://www.ivoa.net/xml/RegistryInterface/v1.0"
    xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0"
    xmlns:vg="http://www.ivoa.net/xml/VORegistry/v1.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:vs="http://www.ivoa.net/xml/VODataService/v1.1"
"""

class TestRegistry(TestCase):
    """Test the Registry model."""
    test_registry_model = Registry(
        full=True,
        managed_authority=["ivo://example.edu"],
        tableset=None,
        created=UTCTimestamp(1996, 3, 11, 19, 0, 0, tzinfo=tz.utc),
        updated=UTCTimestamp(1996, 3, 11, 19, 0, 0, tzinfo=tz.utc),
        status="active",
        title="Example Service",
        identifier="https://example.edu",
        curation=Curation(
            publisher=ResourceName(value="STScI"),
            creator=[Creator(name=ResourceName(value="Doe, J."))],
            contributor=[ResourceName(value="Example Resource")],
            date=[Date(value="2021-01-01T00:00:00Z", role="update")],
            version="1.0",
            contact=[Contact(name=ResourceName(value="John Doe"))],
        ),
        content=Content(
            subject=["Astronomy"],
            description="Example description",
            source=Source(value="https://example.edu", format="bibcode"),
            reference_url="https://example.edu",
            type=["Education"],
            content_level=["General"],
            relationship=[
                Relationship(
                    relationship_type="isPartOf",
                    related_resource=[ResourceName(value="Example Resource", ivo_id="ivo://example.edu/resource")],
                )
            ],
        ),
        rights=[Rights(value="CC BY 4.0", rights_uri="https://creativecommons.org/licenses/by/4.0/")],
        capability=[Capability(standard_id="ivo://ivoa.net/std/TAP")],
    )

    test_registry_xml = (
        f'<ri:Resource xsi:type="vg:Registry" {VOREGISTRY_NAMESPACE_HEADER} '
        'created="1996-03-11T19:00:00.000Z" updated="1996-03-11T19:00:00.000Z" status="active">'
        "<title>Example Service</title>"
        "<identifier>https://example.edu/</identifier>"
        "<curation>"
        "<publisher>STScI</publisher>"
        "<creator><name>Doe, J.</name></creator>"
        "<contributor>Example Resource</contributor>"
        '<date role="update">2021-01-01T00:00:00.000Z</date>'
        "<version>1.0</version>"
        "<contact><name>John Doe</name></contact>"
        "</curation>"
        "<content>"
        "<subject>Astronomy</subject>"
        "<description>Example description</description>"
        '<source format="bibcode">https://example.edu/</source>'
        "<referenceURL>https://example.edu/</referenceURL>"
        "<type>Education</type>"
        "<contentLevel>General</contentLevel>"
        "<relationship>"
        "<relationshipType>isPartOf</relationshipType>"
        '<relatedResource ivo-id="ivo://example.edu/resource">Example Resource</relatedResource>'
        "</relationship>"
        "</content>"
        "<rights rightsURI='https://creativecommons.org/licenses/by/4.0/'>CC BY 4.0</rights>"
        "<capability standardID='ivo://ivoa.net/std/TAP'/>"
        "<full>true</full>"
        "<managedAuthority>ivo://example.edu</managedAuthority>"
        "</ri:Resource>"
    )

    def test_read_from_xml(self):
        """Test reading the Registry model from XML."""

        registry = Registry.from_xml(self.test_registry_xml)
        self.assertIsInstance(registry, Registry)
        self.assertIsInstance(registry, Service)

        # Test for registry-specific attributes
        self.assertTrue(registry.full)
        self.assertEqual(registry.managed_authority, ["ivo://example.edu"])
        self.assertIsNone(registry.tableset)

        # Cursory check for Service values
        self.assertIsInstance(registry.curation, Curation)
        self.assertIsInstance(registry.curation.publisher, ResourceName)
        self.assertIsInstance(registry.content, Content)
        self.assertIsInstance(registry.content.relationship[0], Relationship)
        self.assertIsInstance(registry.capability, list)
        self.assertIsInstance(registry.capability[0], Capability)

    def test_write_to_xml(self):
        """Test writing the Registry model to XML."""

        test_xml = self.test_registry_model.to_xml(encoding=str, skip_empty=True)
        self.assertEqual(
            canonicalize(test_xml),
            canonicalize(self.test_registry_xml)
        )

class TestHarvest(TestCase):
    """Test the Harvest model."""

    test_harvest_model = Harvest(
        standard_id="ivo://ivoa.net/std/Registry",
        validation_level=[Validation(value=0, validated_by="https://example.edu")],
        description="Example description",
        interface=[
            Interface(version="1.0", role="std", access_url=[AccessURL(value="https://example.edu", use="full")])
        ],
        max_records=100
    )

    test_harvest_xml = (
        '<Harvest standardID="ivo://ivoa.net/std/Registry">'
        '<validationLevel validatedBy="https://example.edu/">0</validationLevel>'
        "<description>Example description</description>"
        '<interface role="std" version="1.0">'
        '<accessURL use="full">https://example.edu/</accessURL>'
        "</interface>"
        "<maxRecords>100</maxRecords>"
        "</Harvest>"
    )

    def test_read_from_xml(self):
        """Test reading the Harvest model from XML."""

        harvest = Harvest.from_xml(self.test_harvest_xml)
        self.assertIsInstance(harvest, Harvest)
        self.assertIsInstance(harvest, Capability)

        # Test for harvest-specific attributes
        self.assertEqual(harvest.max_records, 100)

        # Cursory check for Capability values
        self.assertIsInstance(harvest.standard_id, str)
        self.assertIsInstance(harvest.validation_level, list)
        self.assertIsInstance(harvest.interface[0], Interface)



# class TestSearch(TestCase):
#     """Test the Search model."""
#     test_element = Search()

# class TestOAIHTTP(TestCase):
#     """Test the OAIHTTP model."""
#     test_element = OAIHTTP()

# class TestOAISOAP(TestCase):
#     """Test the OAISOAP model."""
#     test_element = OAISOAP()

# class TestAuthority(TestCase):
#     """Test the Authority model."""
#     test_element = Authority()


