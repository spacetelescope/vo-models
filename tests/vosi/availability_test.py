"""Tests for VOSI Availability models."""

from datetime import timezone as tz
from unittest import TestCase
from xml.etree.ElementTree import canonicalize

from lxml import etree

with open("tests/vosi/VOSIAvailability-v1.0.xsd") as f:
    availability_schema = etree.parse(f)

from vo_models.xml.vosi.availability import Availability
from vo_models.xml.voresource.types import UTCTimestamp

VOSI_AVAILABILITY_HEADER = """xmlns="http://www.ivoa.net/xml/VOSIAvailability/v1.0"
xmlns:xsd="http://www.w3.org/2001/XMLSchema"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
"""


class TestVOSIAvailabilityType(TestCase):
    """Tests the VOSI Availability complex type."""

    test_avaiability_xml = (
        f"<availability {VOSI_AVAILABILITY_HEADER}>"
        "<available>true</available>"
        "<upSince>2021-01-01T00:00:00.000Z</upSince>"
        "<downAt>2021-01-01T00:00:00.000Z</downAt>"
        "<backAt>2021-01-01T00:00:00.000Z</backAt>"
        "<note>Test note</note>"
        "</availability>"
    )

    def test_read_from_xml(self):
        """Test reading Availability from XML."""
        availability = Availability.from_xml(self.test_avaiability_xml)
        self.assertTrue(availability.available)
        self.assertEqual(availability.up_since, UTCTimestamp(2021, 1, 1, tzinfo=tz.utc))
        self.assertEqual(availability.down_at, UTCTimestamp(2021, 1, 1, tzinfo=tz.utc))
        self.assertEqual(availability.back_at, UTCTimestamp(2021, 1, 1, tzinfo=tz.utc))
        self.assertEqual(availability.note, ["Test note"])

    def test_write_to_xml(self):
        """Test writing Availability to XML."""
        availability = Availability(
            available=True,
            up_since="2021-01-01T00:00:00.000Z",
            down_at="2021-01-01T00:00:00.000Z",
            back_at="2021-01-01T00:00:00.000Z",
            note=["Test note"],
        )

        availability_xml = availability.to_xml()
        self.assertEqual(
            canonicalize(availability_xml, strip_text=True),
            canonicalize(self.test_avaiability_xml, strip_text=True),
        )
