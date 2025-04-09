"""Tests for VORegistry models."""

from datetime import timezone as tz
from unittest import TestCase
from xml.etree.ElementTree import canonicalize

from vo_models.voregistry.models import OAIHTTP, Harvest, Registry, Authority
from vo_models.voresource.models import (
    AccessURL,
    Capability,
    Contact,
    Content,
    Curation,
    Interface,
    ResourceName,
    Rights,
    Service,
    Validation,
)
from vo_models.voresource.types import UTCTimestamp

VOREGISTRY_NAMESPACE_HEADER = """
    xmlns:ri="http://www.ivoa.net/xml/RegistryInterface/v1.0"
    xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0"
    xmlns:vg="http://www.ivoa.net/xml/VORegistry/v1.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:vs="http://www.ivoa.net/xml/VODataService/v1.1"
"""


class TestOAIHTTP(TestCase):
    """Test the OAIHTTP model."""

    test_oaihttp_model = OAIHTTP(
        role="std",
        version="1.0",
        access_url=[AccessURL(value="http://vao.stsci.edu/directory/oai.aspx?", use="base")],
    )

    test_oaihttp_xml = (
        f'<interface {VOREGISTRY_NAMESPACE_HEADER} xsi:type="vg:OAIHTTP" role="std" version="1.0">'
        '<accessURL use="base">http://vao.stsci.edu/directory/oai.aspx?</accessURL>'
        "</interface>"
    )

    def test_read_from_xml(self):
        """Test reading the OAIHTTP model from XML."""

        oaihttp = OAIHTTP.from_xml(self.test_oaihttp_xml)
        self.assertIsInstance(oaihttp, OAIHTTP)
        self.assertIsInstance(oaihttp, Interface)

        # Test for OAIHTTP-specific attributes
        self.assertEqual(oaihttp.role, "std")
        self.assertEqual(oaihttp.version, "1.0")

        # Cursory check for Interface values
        self.assertIsInstance(oaihttp.access_url[0], AccessURL)

    def test_write_to_xml(self):
        """Test writing the OAIHTTP model to XML."""

        test_xml = self.test_oaihttp_model.to_xml(encoding=str, skip_empty=True)
        self.assertEqual(canonicalize(test_xml), canonicalize(self.test_oaihttp_xml))

class TestAuthority(TestCase):
    """Test the Authority model."""

    test_authority_model = Authority(
        created=UTCTimestamp(2024, 4, 5, 14, 55, 33, tzinfo=tz.utc),
        updated=UTCTimestamp(2015, 11, 19, 17, 43, 23, tzinfo=tz.utc),
        validation_level=[Validation(value=2, validated_by="ivo://archive.stsci.edu/nvoregistry")],
        title="CSIRO Authority Resource",
        identifier="ivo://au.csiro",
        curation=Curation(
            publisher=ResourceName(value="CSIRO"),
            contact=Contact(
                name=ResourceName(value="John Doe"),
                email="john.doe@csiro.au"
            )
        ),
        content=Content(
            subject=["Authority"],
            description="CSIRO Authority Resource",
        ),
        managing_org = ResourceName(value="Example Managing Org", ivo_id="ivo://au.csiro/organisation"),
    )

    test_authority_xml = (
        '<ri:Resource created="2014-04-05T14:55:33Z" status="active" updated="2015-11-19T17:43:23Z" xmlns:ri="http://www.ivoa.net/xml/RegistryInterface/v1.0" xmlns:vg="http://www.ivoa.net/xml/VORegistry/v1.0" xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" xsi:type="vg:Authority" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ivoa.net/xml/RegistryInterface/v1.0 http://software.astrogrid.org/schema/registry/RegistryInterface/v1.0/RegistryInterface.xsd http://www.ivoa.net/xml/VOResource/v1.0 http://software.astrogrid.org/schema/vo-resource-types/VOResource/v1.0/VOResource.xsd  http://www.ivoa.net/xml/VORegistry/v1.0 http://software.astrogrid.org/schema/vo-resource-types/VORegistry/v1.0/VORegistry.xsd">'
        '<validationLevel validatedBy="ivo://archive.stsci.edu/nvoregistry">2</validationLevel>'
        '<title>CSIRO Authority Resource</title>'
        '<shortName>CSIRO Authority</shortName>'
        '<identifier>ivo://au.csiro</identifier>'
        '<curation>'
        '<publisher>CSIRO</publisher>'
        '<contact>'
        '<name>John Doe</name>'
        '<email>john.doe@csiro.au</email>'
        '</contact>'
        '</curation>'
        '<content>'
        '<subject>Authority</subject>'
        '<description>CSIRO Authority Resource</description>'
        '<referenceURL>http://data.csiro.au/astrogrid-registry</referenceURL>'
        '</content>'
        '<managingOrg ivo-id="ivo://au.csiro/organisation" />'
        '</ri:Resource>'
    )

class TestRegistry(TestCase):
    """Test the Registry model."""

    test_registry_model = Registry(
        full=True,
        managed_authority=["archive.stsci.edu"],
        tableset=None,
        created=UTCTimestamp(2006, 1, 19, 0, 0, 0, tzinfo=tz.utc),
        updated=UTCTimestamp(2024, 10, 30, 18, 55, 23, tzinfo=tz.utc),
        status="active",
        title="STScI Searchable Registry",
        short_name="STScIReg",
        identifier="ivo://archive.stsci.edu/nvoregistry",
        curation=Curation(
            publisher=ResourceName(value="Space Telescope Science Institute"),
            contact=[Contact(name=ResourceName(value="MAST VO team"), email="vo-registry@stsci.edu")],
        ),
        content=Content(
            subject=["virtual observatory"],
            description="Fully Searchable NVO Registry. Implements OAI interface and follows the standards and protocols of the IVOA Registry working group. ",
            reference_url="http://vao.stsci.edu/directory/",
            content_level=["Research"],
        ),
        rights=[Rights(value="CC BY 4.0", rights_uri="https://creativecommons.org/licenses/by/4.0/")],
        capability=[Capability(standard_id="ivo://ivoa.net/std/TAP")],
    )

    test_registry_xml = (
        '<ri:Resource xsi:type="vg:Registry" xmlns:ri="http://www.ivoa.net/xml/RegistryInterface/v1.0" xmlns:vg="http://www.ivoa.net/xml/VORegistry/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ivoa.net/xml/VOResource/v1.0 http://www.ivoa.net/xml/VOResource/v1.0 http://www.ivoa.net/xml/VORegistry/v1.0 http://www.ivoa.net/xml/VORegistry/v1.0 http://www.ivoa.net/xml/VODataService/v1.1 http://www.ivoa.net/xml/VODataService/v1.1" status="active" created="2006-01-19T00:00:00Z" updated="2024-10-30T18:55:23Z">'
        '<validationLevel validatedBy="ivo://archive.stsci.edu/nvoregistry">2</validationLevel>'
        "<title>STScI Searchable Registry</title>"
        "<shortName>STScIReg</shortName>"
        "<identifier>ivo://archive.stsci.edu/nvoregistry</identifier>"
        "<curation>"
        "<publisher> Space Telescope Science Institute</publisher>"
        "<contact>"
        "<name>MAST VO team</name>"
        "<email>vo-registry@stsci.edu</email>"
        "</contact>"
        "</curation>"
        "<content>"
        "<subject>virtual observatory</subject>"
        "<description>Fully Searchable NVO Registry. Implements OAI interface and follows the standards and protocols of the IVOA Registry working group. </description>"
        "<referenceURL>http://vao.stsci.edu/directory/</referenceURL>"
        "<contentLevel>Research</contentLevel>"
        "</content>"
        '<capability xsi:type="vg:Harvest" standardID="ivo://ivoa.net/std/Registry">'
        '<validationLevel validatedBy="ivo://archive.stsci.edu/nvoregistry">2</validationLevel>'
        '<interface xsi:type="vg:OAIHTTP" role="std" version="1.0">'
        '<accessURL use="base">http://vao.stsci.edu/directory/oai.aspx?</accessURL>'
        "</interface>"
        "<maxRecords>1000</maxRecords>"
        "</capability>"
        "<full>true</full>"
        "<managedAuthority>archive.stsci.edu</managedAuthority>"
        "</ri:Resource>"
    )

    def test_read_from_xml(self):
        """Test reading the Registry model from XML."""

        registry = Registry.from_xml(self.test_registry_xml)
        self.assertIsInstance(registry, Registry)
        self.assertIsInstance(registry, Service)

        # Test for registry-specific attributes
        self.assertTrue(registry.full)
        self.assertEqual(registry.managed_authority, ["archive.stsci.edu"])
        self.assertIsNone(registry.tableset)

        # Cursory check for Service values
        self.assertIsInstance(registry.curation, Curation)
        self.assertIsInstance(registry.curation.publisher, ResourceName)
        self.assertIsInstance(registry.content, Content)
        self.assertIsInstance(registry.capability, list)
        self.assertIsInstance(registry.capability[0], Capability)

    def test_write_to_xml(self):
        """Test writing the Registry model to XML."""

        test_xml = self.test_registry_model.to_xml(encoding=str, skip_empty=True)
        self.assertEqual(canonicalize(test_xml), canonicalize(self.test_registry_xml))


class TestHarvest(TestCase):
    """Test the Harvest model."""

    test_harvest_model = Harvest(
        standard_id="ivo://ivoa.net/std/Registry",
        validation_level=[Validation(value=0, validated_by="https://example.edu")],
        description="Example description",
        interface=[
            Interface(version="1.0", role="std", access_url=[AccessURL(value="https://example.edu", use="full")])
        ],
        max_records=100,
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
