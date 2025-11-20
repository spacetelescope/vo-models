"""Tests for the VOEvent models.

Test XML taken from the VOEvent v2.1 specification where provided.
"""

from unittest import TestCase
from xml.etree.ElementTree import canonicalize

from vo_models.vocab.vocab import TimeScale
from vo_models.voevent import Author, ContributorRole, CoordValue, EventIVORN, Name, TimeInstant, TimeInterval


class TestAuthorModel(TestCase):
    """Test the Author model."""

    test_xml = """
    <Author>
        <title>Rapid Telescope for Optical Response</title>
        <shortName>Raptor</shortName>
        <logoURL>http://www.raptor.lanl.gov/images/RAPTOR_patchLarge.jpg</logoURL>
        <contactName>Robert White</contactName>
        <contactEmail>rwhite@lanl.gov</contactEmail>
        <contactPhone>+1 800 555 1212</contactPhone>
    </Author>
    """

    test_element = Author(
        title="Rapid Telescope for Optical Response",
        short_name="Raptor",
        logo_url="http://www.raptor.lanl.gov/images/RAPTOR_patchLarge.jpg",
        contact_name="Robert White",
        contact_email="rwhite@lanl.gov",
        contact_phone="+1 800 555 1212",
    )

    def test_read_from_xml(self):
        """Test reading an Author from XML."""
        author = Author.from_xml(self.test_xml)
        self.assertIsInstance(author, Author)
        self.assertEqual(author.title[0], "Rapid Telescope for Optical Response")
        self.assertEqual(author.short_name[0], "Raptor")
        self.assertEqual(author.logo_url[0], "http://www.raptor.lanl.gov/images/RAPTOR_patchLarge.jpg")
        self.assertEqual(author.contact_name[0], "Robert White")
        self.assertEqual(author.contact_email[0], "rwhite@lanl.gov")
        self.assertEqual(author.contact_phone[0], "+1 800 555 1212")

    def test_write_to_xml(self):
        """Test writing an Author to XML."""
        author_xml = self.test_element.to_xml()
        self.assertEqual(
            canonicalize(author_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestCoordValue(TestCase):
    """Test the CoordValue model."""

    test_xml = """
    <CoordValue pos_unit="deg" ucd="pos.eq.ra;meta.main">248.4056</CoordValue>
    """

    test_element = CoordValue(
        value=248.4056,
        pos_unit="deg",
        ucd="pos.eq.ra;meta.main",
    )

    def test_read_from_xml(self):
        """Test reading a CoordValue from XML."""
        coord_value = CoordValue.from_xml(self.test_xml)
        self.assertIsInstance(coord_value, CoordValue)
        self.assertEqual(coord_value.value, 248.4056)
        self.assertEqual(coord_value.pos_unit, "deg")
        self.assertEqual(coord_value.ucd, "pos.eq.ra;meta.main")

    def test_write_to_xml(self):
        """Test writing a CoordValue to XML."""
        coord_value_xml = self.test_element.to_xml()
        self.assertEqual(
            canonicalize(coord_value_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestEventIVORN(TestCase):
    """Test the EventIVORN model."""

    test_xml = """
    <EventIVORN cite="followup">ivo://raptor.lanl.gov/raptor#1234567890</EventIVORN>
    """

    test_element = EventIVORN(
        value="ivo://raptor.lanl.gov/raptor#1234567890",
        cite="followup",
    )

    def test_read_from_xml(self):
        """Test reading an EventIVORN from XML."""
        event_ivorn = EventIVORN.from_xml(self.test_xml)
        self.assertIsInstance(event_ivorn, EventIVORN)
        self.assertEqual(event_ivorn.value, "ivo://raptor.lanl.gov/raptor#1234567890")
        self.assertEqual(event_ivorn.cite, "followup")

    def test_write_to_xml(self):
        """Test writing an EventIVORN to XML."""
        event_ivorn_xml = EventIVORN.to_xml(self.test_element)
        self.assertEqual(
            canonicalize(event_ivorn_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestNameElement(TestCase):
    """Test the Name model."""

    test_xml = """
    <Name altIdentifier="orcid:0000-0002-1825-0097"
        role="ContactPerson"
        ivorn="ivo://example.org/author/JohnDoe">John Doe</Name>
    """

    test_element = Name(
        value="John Doe",
        alt_identifier="orcid:0000-0002-1825-0097",
        role=ContributorRole.CONTACT_PERSON,
        ivorn="ivo://example.org/author/JohnDoe",
    )

    def test_read_from_xml(self):
        """Test reading a Name from XML."""
        name = Name.from_xml(self.test_xml)
        self.assertIsInstance(name, Name)
        self.assertEqual(name.value, "John Doe")
        self.assertEqual(str(name.alt_identifier), "orcid:0000-0002-1825-0097")
        self.assertEqual(name.role, "ContactPerson")
        self.assertEqual(str(name.ivorn), "ivo://example.org/author/JohnDoe")

    def test_write_to_xml(self):
        """Test writing a Name to XML."""
        name_xml = Name.to_xml(self.test_element)
        self.assertEqual(
            canonicalize(name_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestTimeInstant(TestCase):
    """Test the TimeInstant model."""

    test_xml = """
    <TimeInstant>
        <ISOTime>2004-07-15T08:23:56</ISOTime>
        <TimeOffset>55.1</TimeOffset>
        <TimeScale>UTC</TimeScale>
    </TimeInstant>
    """

    test_elemetn = TimeInstant(
        iso_time="2004-07-15T08:23:56",
        time_offset=55.1,
        time_scale=TimeScale.UTC,
    )

    def test_read_from_xml(self):
        """Test reading a TimeInstant from XML."""
        time_instant = TimeInstant.from_xml(self.test_xml)
        self.assertIsInstance(time_instant, TimeInstant)
        self.assertEqual(time_instant.isotime, "2004-07-15T08:23:56")
        self.assertEqual(time_instant.time_offset, 55.1)
        self.assertEqual(time_instant.time_scale, TimeScale.UTC)

    def test_write_to_xml(self):
        """Test writing a TimeInstant to XML."""
        time_instant_xml = TimeInstant.to_xml(self.test_elemetn)
        self.assertEqual(
            canonicalize(time_instant_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestTimeInterval(TestCase):
    """Test the TimeInterval model."""

    test_xml = """
    <TimeInterval>
        <ISOTimeStart>2004-07-15T08:23:56</ISOTimeStart>
        <ISOTimeStop>2004-07-15T09:23:56</ISOTimeStop>
    </TimeInterval>
    """

    test_element = TimeInterval(
        iso_time_start="2004-07-15T08:23:56",
        iso_time_stop="2004-07-15T09:23:56",
    )

    def test_read_from_xml(self):
        """Test reading a TimeInterval from XML."""
        time_interval = TimeInterval.from_xml(self.test_xml)
        self.assertIsInstance(time_interval, TimeInterval)
        self.assertEqual(time_interval.isotime_start, "2004-07-15T08:23:56")
        self.assertEqual(time_interval.isotime_stop, "2004-07-15T09:23:56")

    def test_write_to_xml(self):
        """Test writing a TimeInterval to XML."""
        time_interval_xml = TimeInterval.to_xml(self.test_element)
        self.assertEqual(
            canonicalize(time_interval_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )
