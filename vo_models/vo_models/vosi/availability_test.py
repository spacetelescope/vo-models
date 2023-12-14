"""Tests for the VOSI Availability model"""

# We're only parsing a locally controlled XSD file
from lxml import etree  # nosec B410

from mast.vo_tap.services.vo_models.vo_models_test import VOModelTestBase
from mast.vo_tap.services.vo_models.vosi import Availability

AVAIL_NS_HEADER = """xmlns:xsd="http://www.w3.org/2001/XMLSchema"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns="http://www.ivoa.net/xml/VOSIAvailability/v1.0"
"""

with open("mast/vo_tap/services/vo_models/vosi/VOSIAvailability-v1.0.xsd", "r") as schema_file:
    availability_schema = etree.XMLSchema(file=schema_file)


class TestAvailability(VOModelTestBase.VOModelTestCase):
    """Test the Availability model"""

    test_xml = (
        f"<availability {AVAIL_NS_HEADER}>"
        "<available>true</available>"
        "<upSince>2021-01-01T00:00:00.000Z</upSince>"
        "<downAt>2021-01-01T00:00:00.000Z</downAt>"
        "<backAt>2021-01-01T00:00:00.000Z</backAt>"
        "<note>Available Mon-Friday</note>"
        "<note>We take weekends off</note>"
        "</availability>"
    )

    test_element = Availability(
        available=True,
        up_since="2021-01-01T00:00:00.000Z",
        down_at="2021-01-01T00:00:00.000Z",
        back_at="2021-01-01T00:00:00.000Z",
        note=["Available Mon-Friday", "We take weekends off"],
    )

    base_model = Availability

    def test_validate(self):
        """Validate the model agains the Availability schema"""
        availability_xml = etree.fromstring(self.test_element.to_xml(skip_empty=True, encoding=str))
        availability_schema.assertValid(availability_xml)
