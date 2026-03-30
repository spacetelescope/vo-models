"""Tests for the VOEvent models.

Test XML taken from the VOEvent v2.1 specification where provided.
"""

from unittest import TestCase
from xml.etree.ElementTree import canonicalize

from vo_models.vocab.vocab import TimeScale
from vo_models.voevent import (
    AstroCoords,
    AstroCoordSystem,
    Author,
    Citations,
    ContributorRole,
    CoordValue,
    Data,
    Error2,
    Error3,
    EventIVORN,
    Field,
    Group,
    How,
    Inference,
    Name,
    ObsDataLocation,
    ObservationLocation,
    ObservatoryLocation,
    Param,
    Position2D,
    Position3D,
    Reference,
    RoleValues,
    SpaceFrameType,
    Table,
    Time,
    TimeFrameType,
    TimeInstant,
    TimeInterval,
    Value2,
    Value3,
    VOEvent,
    What,
    WhereWhen,
    Who,
    Why,
)


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
        isotime_stop="2004-07-15T09:23:56",
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


class TestTimeElement(TestCase):
    """Test the Time element models."""

    time_instant_xml = """
<Time unit="s">
  <TimeInstant>
    <ISOTime>2025-11-22T10:30:45.123</ISOTime>
    <TimeScale>UTC</TimeScale>
  </TimeInstant>
  <Error>0.5</Error>
</Time>
"""

    time_interval_xml = """
<Time unit="s">
  <TimeInterval>
    <ISOTimeStart>2025-11-22T10:30:00</ISOTimeStart>
    <ISOTimeStop>2025-11-22T10:31:00</ISOTimeStop>
  </TimeInterval>
</Time>
"""

    time_instant_model = Time(
        unit="s",
        time_instant=TimeInstant(
            isotime="2025-11-22T10:30:45.123",
            time_scale=TimeScale.UTC,
        ),
        error=0.5,
    )

    time_interval_model = Time(
        unit="s",
        time_interval=TimeInterval(
            isotime_start="2025-11-22T10:30:00",
            isotime_stop="2025-11-22T10:31:00",
        ),
    )

    def test_read_time_instant_from_xml(self):
        """Test reading a Time element with TimeInstant from XML."""
        time_element = Time.from_xml(self.time_instant_xml)
        self.assertIsInstance(time_element, Time)
        self.assertEqual(time_element.unit, "s")
        self.assertIsNotNone(time_element.time_instant)
        self.assertIsNone(time_element.time_interval)
        self.assertEqual(time_element.time_instant.isotime, "2025-11-22T10:30:45.123")
        self.assertEqual(time_element.time_instant.time_scale, TimeScale.UTC)
        self.assertEqual(time_element.error, 0.5)

    def test_write_time_instant_to_xml(self):
        """Test writing a Time element with TimeInstant to XML."""
        time_instant_xml = Time.to_xml(self.time_instant_model, skip_empty=True)
        self.assertEqual(
            canonicalize(time_instant_xml, strip_text=True),
            canonicalize(self.time_instant_xml, strip_text=True),
        )

    def test_read_time_interval_from_xml(self):
        """Test reading a Time element with TimeInterval from XML."""
        time_element = Time.from_xml(self.time_interval_xml)
        self.assertIsInstance(time_element, Time)
        self.assertEqual(time_element.unit, "s")
        self.assertIsNotNone(time_element.time_interval)
        self.assertIsNone(time_element.time_instant)
        self.assertEqual(time_element.time_interval.isotime_start, "2025-11-22T10:30:00")
        self.assertEqual(time_element.time_interval.isotime_stop, "2025-11-22T10:31:00")

    def test_write_time_interval_to_xml(self):
        """Test writing a Time element with TimeInterval to XML."""
        time_interval_xml = Time.to_xml(self.time_interval_model, skip_empty=True)
        self.assertEqual(
            canonicalize(time_interval_xml, strip_text=True),
            canonicalize(self.time_interval_xml, strip_text=True),
        )


class TestValue2Model(TestCase):
    """Test the Value2 model."""

    test_xml = """
        <Value2>
            <C1>148.88821</C1>
            <C2>69.06529</C2>
        </Value2>
    """

    test_element = Value2(
        c1=CoordValue(
            value=148.88821,
        ),
        c2=CoordValue(
            value=69.06529,
        ),
    )

    def test_read_from_xml(self):
        """Test reading a Value2 from XML."""
        value2 = Value2.from_xml(self.test_xml)
        self.assertIsInstance(value2, Value2)
        self.assertEqual(value2.c1.value, 148.88821)
        self.assertEqual(value2.c2.value, 69.06529)

    def test_write_to_xml(self):
        """Test writing a Value2 to XML."""
        value2_xml = Value2.to_xml(self.test_element, skip_empty=True)
        self.assertEqual(
            canonicalize(value2_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestValue3Model(TestCase):
    """Test the Value3 model."""

    test_xml = """
        <Value3>
            <C1>148.88821</C1>
            <C2>69.06529</C2>
            <C3>150.12345</C3>
        </Value3>
    """

    test_element = Value3(
        c1=CoordValue(
            value=148.88821,
        ),
        c2=CoordValue(
            value=69.06529,
        ),
        c3=CoordValue(
            value=150.12345,
        ),
    )

    def test_read_from_xml(self):
        """Test reading a Value3 from XML."""
        value3 = Value3.from_xml(self.test_xml)
        self.assertIsInstance(value3, Value3)
        self.assertEqual(value3.c1.value, 148.88821)
        self.assertEqual(value3.c2.value, 69.06529)
        self.assertEqual(value3.c3.value, 150.12345)

    def test_write_to_xml(self):
        """Test writing a Value3 to XML."""
        value3_xml = Value3.to_xml(self.test_element, skip_empty=True)
        self.assertEqual(
            canonicalize(value3_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestError2Model(TestCase):
    """Test the Error2 model."""

    test_xml = """
        <Error2>
            <C1>0.1</C1>
            <C2>0.2</C2>
        </Error2>
    """

    test_element = Error2(
        c1=CoordValue(
            value=0.1,
        ),
        c2=CoordValue(
            value=0.2,
        ),
    )

    def test_read_from_xml(self):
        """Test reading an Error2 from XML."""
        error2 = Error2.from_xml(self.test_xml)
        self.assertIsInstance(error2, Error2)
        self.assertEqual(error2.c1.value, 0.1)
        self.assertEqual(error2.c2.value, 0.2)

    def test_write_to_xml(self):
        """Test writing an Error2 to XML."""
        error2_xml = Error2.to_xml(self.test_element, skip_empty=True)
        self.assertEqual(
            canonicalize(error2_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestError3Model(TestCase):
    """Test the Error3 model."""

    test_xml = """
        <Error3>
            <C1>0.1</C1>
            <C2>0.2</C2>
            <C3>0.3</C3>
        </Error3>
    """

    test_element = Error3(
        c1=CoordValue(
            value=0.1,
        ),
        c2=CoordValue(
            value=0.2,
        ),
        c3=CoordValue(
            value=0.3,
        ),
    )

    def test_read_from_xml(self):
        """Test reading an Error3 from XML."""
        error3 = Error3.from_xml(self.test_xml)
        self.assertIsInstance(error3, Error3)
        self.assertEqual(error3.c1.value, 0.1)
        self.assertEqual(error3.c2.value, 0.2)
        self.assertEqual(error3.c3.value, 0.3)

    def test_write_to_xml(self):
        """Test writing an Error3 to XML."""
        error3_xml = Error3.to_xml(self.test_element, skip_empty=True)
        self.assertEqual(
            canonicalize(error3_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestPosition2DModel(TestCase):
    """Test the Position2D model."""

    test_xml = """
        <Position2D unit="deg">
            <Name1>RA</Name1>
            <Name2>Dec</Name2>
            <Value2>
                <C1>148.88821</C1>
                <C2>69.06529</C2>
            </Value2>
            <Error2Radius>0.03</Error2Radius>
            <Error2>
                <C1>0.1</C1>
                <C2>0.2</C2>
            </Error2>
        </Position2D>
    """

    test_model = Position2D(
        unit="deg",
        name1="RA",
        name2="Dec",
        value2=Value2(
            c1=CoordValue(value=148.88821),
            c2=CoordValue(value=69.06529),
        ),
        error2_radius=CoordValue(value=0.03),
        error2=Error2(
            c1=CoordValue(value=0.1),
            c2=CoordValue(value=0.2),
        ),
    )

    def test_read_from_xml(self):
        """Test reading a Position2D from XML."""
        position2d = Position2D.from_xml(self.test_xml)
        self.assertIsInstance(position2d, Position2D)
        self.assertEqual(position2d.unit, "deg")
        self.assertEqual(position2d.name1, "RA")
        self.assertEqual(position2d.name2, "Dec")
        self.assertEqual(position2d.value2.c1.value, 148.88821)
        self.assertEqual(position2d.value2.c2.value, 69.06529)
        self.assertEqual(position2d.error2_radius, 0.03)
        self.assertEqual(position2d.error2.c1.value, 0.1)
        self.assertEqual(position2d.error2.c2.value, 0.2)

    def test_write_to_xml(self):
        """Test writing a Position2D to XML."""
        position2d_xml = Position2D.to_xml(self.test_model, skip_empty=True)
        self.assertEqual(
            canonicalize(position2d_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestPosition3DModel(TestCase):
    """Test the Position3D model."""

    test_xml = """
        <Position3D unit="deg">
            <Name1>RA</Name1>
            <Name2>Dec</Name2>
            <Name3>Distance</Name3>
            <Value3>
                <C1>148.88821</C1>
                <C2>69.06529</C2>
                <C3>150.12345</C3>
            </Value3>
            <Error3>
                <C1>0.1</C1>
                <C2>0.2</C2>
                <C3>0.3</C3>
            </Error3>
        </Position3D>
    """

    test_model = Position3D(
        unit="deg",
        name1="RA",
        name2="Dec",
        name3="Distance",
        value3=Value3(
            c1=CoordValue(value=148.88821),
            c2=CoordValue(value=69.06529),
            c3=CoordValue(value=150.12345),
        ),
        error3=Error3(
            c1=CoordValue(value=0.1),
            c2=CoordValue(value=0.2),
            c3=CoordValue(value=0.3),
        ),
    )

    def test_read_from_xml(self):
        """Test reading a Position3D from XML."""
        position3d = Position3D.from_xml(self.test_xml)
        self.assertIsInstance(position3d, Position3D)
        self.assertEqual(position3d.unit, "deg")
        self.assertEqual(position3d.name1, "RA")
        self.assertEqual(position3d.name2, "Dec")
        self.assertEqual(position3d.name3, "Distance")
        self.assertEqual(position3d.value3.c1.value, 148.88821)
        self.assertEqual(position3d.value3.c2.value, 69.06529)
        self.assertEqual(position3d.value3.c3.value, 150.12345)
        self.assertEqual(position3d.error3.c1.value, 0.1)
        self.assertEqual(position3d.error3.c2.value, 0.2)
        self.assertEqual(position3d.error3.c3.value, 0.3)

    def test_write_to_xml(self):
        """Test writing a Position3D to XML."""
        position3d_xml = Position3D.to_xml(self.test_model, skip_empty=True)
        self.assertEqual(
            canonicalize(position3d_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestCitationsModel(TestCase):
    """Test the Citations model."""

    test_xml = """
    <Citations>
        <EventIVORN cite="followup">ivo://raptor.lanl.gov/raptor#1234567890</EventIVORN>
        <EventIVORN cite="supersedes">ivo://example.org/voevent#0987654321</EventIVORN>
        <Description>Previous related events</Description>
    </Citations>
    """

    test_element = Citations(
        event_ivorn=[
            EventIVORN(
                value="ivo://raptor.lanl.gov/raptor#1234567890",
                cite="followup",
            ),
            EventIVORN(
                value="ivo://example.org/voevent#0987654321",
                cite="supersedes",
            ),
        ],
        description="Previous related events",
    )

    def test_read_from_xml(self):
        """Test reading a Citations from XML."""
        citations = Citations.from_xml(self.test_xml)
        self.assertIsInstance(citations, Citations)
        self.assertEqual(len(citations.event_ivorn), 2)
        self.assertEqual(citations.event_ivorn[0].value, "ivo://raptor.lanl.gov/raptor#1234567890")
        self.assertEqual(citations.event_ivorn[0].cite, "followup")
        self.assertEqual(citations.event_ivorn[1].value, "ivo://example.org/voevent#0987654321")
        self.assertEqual(citations.event_ivorn[1].cite, "supersedes")
        self.assertEqual(citations.description, "Previous related events")

    def test_write_to_xml(self):
        """Test writing a Citations to XML."""
        citations_xml = Citations.to_xml(self.test_element, skip_empty=True)
        self.assertEqual(
            canonicalize(citations_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestReferenceModel(TestCase):
    """Test the Reference model."""

    test_xml = """
    <Reference uri="http://raptor.lanl.gov/data/lightcurves/235649409"
      mimetype="application/x-votable+xml"
      meaning="http://ivoa.net/rdf/uat#light-curves"/>
    """

    test_element = Reference(
        uri="http://raptor.lanl.gov/data/lightcurves/235649409",
        mimetype="application/x-votable+xml",
        meaning="http://ivoa.net/rdf/uat#light-curves",
    )

    def test_read_from_xml(self):
        """Test reading a Reference from XML."""
        reference = Reference.from_xml(self.test_xml)
        self.assertIsInstance(reference, Reference)
        self.assertEqual(reference.uri, "http://raptor.lanl.gov/data/lightcurves/235649409")
        self.assertEqual(reference.mimetype, "application/x-votable+xml")
        self.assertEqual(reference.meaning, "http://ivoa.net/rdf/uat#light-curves")

    def test_write_to_xml(self):
        """Test writing a Reference to XML."""
        reference_xml = Reference.to_xml(self.test_element, skip_empty=True)
        self.assertEqual(
            canonicalize(reference_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestHowModel(TestCase):
    """Test the How model."""

    test_xml = """
    <How>
        <Description>Details on how the observation was made.</Description>
        <Reference uri="http://example.org/observation/method"
            mimetype="text/html"
            meaning="http://ivoa.net/rdf/uat#observation-method"/>
    </How>
    """

    test_element = How(
        description="Details on how the observation was made.",
        reference=Reference(
            uri="http://example.org/observation/method",
            mimetype="text/html",
            meaning="http://ivoa.net/rdf/uat#observation-method",
        ),
    )

    def test_read_from_xml(self):
        """Test reading a How from XML."""
        how = How.from_xml(self.test_xml)
        self.assertIsInstance(how, How)
        self.assertEqual(how.description, "Details on how the observation was made.")
        self.assertIsNotNone(how.reference)
        self.assertEqual(how.reference.uri, "http://example.org/observation/method")
        self.assertEqual(how.reference.mimetype, "text/html")
        self.assertEqual(how.reference.meaning, "http://ivoa.net/rdf/uat#observation-method")

    def test_write_to_xml(self):
        """Test writing a How to XML."""
        how_xml = How.to_xml(self.test_element, skip_empty=True)
        self.assertEqual(
            canonicalize(how_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestAstroCoords(TestCase):
    """Test the AstroCoords model."""

    test_xml = """
        <AstroCoords coord_system_id="UTC-ICRS-TOPO">
        <Time>
            <TimeInstant>
            <ISOTime>2009-09-25T12:00:00</ISOTime>
            </TimeInstant>
            <Error>0.0</Error>
        </Time>
        <Position2D unit="deg">
            <Value2>
            <C1>37.0603169</C1>
            <!-- RA  -->
            <C2>31.3116578</C2>
            <!-- Dec -->
            </Value2>
            <Error2Radius>0.03</Error2Radius>
        </Position2D>
        </AstroCoords>
    """

    test_element = AstroCoords(
        coord_system_id="UTC-ICRS-TOPO",
        time=Time(
            time_instant=TimeInstant(
                isotime="2009-09-25T12:00:00",
            ),
            error=0.0,
        ),
        position2d=Position2D(
            unit="deg",
            value2=Value2(
                c1=CoordValue(value=37.0603169),
                c2=CoordValue(value=31.3116578),
            ),
            error2_radius=CoordValue(value=0.03),
        ),
    )

    def test_read_from_xml(self):
        """Test reading an AstroCoords from XML."""
        astro_coords = AstroCoords.from_xml(self.test_xml)
        self.assertIsInstance(astro_coords, AstroCoords)
        self.assertEqual(astro_coords.coord_system_id, "UTC-ICRS-TOPO")
        self.assertIsNotNone(astro_coords.time)
        self.assertEqual(astro_coords.time.time_instant.isotime, "2009-09-25T12:00:00")
        self.assertEqual(astro_coords.time.error, 0.0)
        self.assertIsNotNone(astro_coords.position_2d)
        self.assertEqual(astro_coords.position_2d.unit, "deg")
        self.assertEqual(astro_coords.position_2d.value2.c1.value, 37.0603169)
        self.assertEqual(astro_coords.position_2d.value2.c2.value, 31.3116578)
        self.assertEqual(astro_coords.position_2d.error2_radius.value, 0.03)

    def test_write_to_xml(self):
        """Test writing an AstroCoords to XML."""
        astro_coords_xml = AstroCoords.to_xml(self.test_element, skip_empty=True)
        self.assertEqual(
            canonicalize(astro_coords_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestAstroCoordSystem(TestCase):
    """Test AstroCoordSystem model."""

    test_xml = """
    <AstroCoordSystem id="JupiterSystem">
        <TimeFrame id="JupiterTimeFrame">
            <Name>Jupiter Standard Time</Name>
            <ReferencePosition>Jupiter</ReferencePosition>
            <TimeScale>UTC</TimeScale>
        </TimeFrame>
        <SpaceFrame id="JupiterICRS">
            <Name>Jupiter ICRS</Name>
            <ReferenceFrame>ICRS</ReferenceFrame>
            <ReferencePosition>Jupiter</ReferencePosition>
            <Flavor>SPHERICAL</Flavor>
        </SpaceFrame>
    </AstroCoordSystem>
    """

    test_element = AstroCoordSystem(
        id="JupiterSystem",
        time_frame=TimeFrameType(
            id="JupiterTimeFrame",
            name="Jupiter Standard Time",
            reference_position="Jupiter",
            time_scale=TimeScale.UTC,
        ),
        space_frame=SpaceFrameType(
            id="JupiterICRS",
            name="Jupiter ICRS",
            reference_frame="ICRS",
            reference_position="Jupiter",
            flavor="SPHERICAL",
        ),
    )

    def test_read_from_xml(self):
        """Test reading an AstroCoordSystem from XML."""
        coord_system = AstroCoordSystem.from_xml(self.test_xml)
        self.assertIsInstance(coord_system, AstroCoordSystem)
        self.assertEqual(coord_system.id, "JupiterSystem")
        self.assertIsNotNone(coord_system.time_frame)
        self.assertEqual(coord_system.time_frame.id, "JupiterTimeFrame")
        self.assertIsNotNone(coord_system.space_frame)
        self.assertEqual(coord_system.space_frame.id, "JupiterICRS")

    def test_write_to_xml(self):
        """Test writing an AstroCoordSystem to XML."""
        coord_system_xml = AstroCoordSystem.to_xml(self.test_element, skip_empty=True)
        self.assertEqual(
            canonicalize(coord_system_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestObservationLocationModel(TestCase):
    """Test the ObservationLocation model."""

    test_xml = """
        <ObservationLocation>
        <AstroCoordSystem id="UTC-ICRS-TOPO" />
        <AstroCoords coord_system_id="UTC-ICRS-TOPO">
            <Time>
            <TimeInstant>
                <ISOTime>2009-09-25T12:00:00</ISOTime>
            </TimeInstant>
            <Error>0.0</Error>
            </Time>
            <Position2D unit="deg">
            <Value2>
                <C1>37.0603169</C1>
                <!-- RA  -->
                <C2>31.3116578</C2>
                <!-- Dec -->
            </Value2>
            <Error2Radius>0.03</Error2Radius>
            </Position2D>
        </AstroCoords>
        </ObservationLocation>
    """

    test_element = ObservationLocation(
        astro_coord_system=AstroCoordSystem(
            id="UTC-ICRS-TOPO",
        ),
        astro_coords=AstroCoords(
            coord_system_id="UTC-ICRS-TOPO",
            time=Time(
                time_instant=TimeInstant(
                    isotime="2009-09-25T12:00:00",
                ),
                error=0.0,
            ),
            position2d=Position2D(
                unit="deg",
                value2=Value2(
                    c1=CoordValue(value=37.0603169),
                    c2=CoordValue(value=31.3116578),
                ),
                error2_radius=CoordValue(value=0.03),
            ),
        ),
    )

    def test_read_from_xml(self):
        """Test reading an ObservationLocation from XML."""
        obs_location = ObservationLocation.from_xml(self.test_xml)
        self.assertIsInstance(obs_location, ObservationLocation)
        self.assertIsNotNone(obs_location.astro_coord_system)
        self.assertEqual(obs_location.astro_coord_system.id, "UTC-ICRS-TOPO")
        self.assertIsNotNone(obs_location.astro_coords)
        self.assertEqual(obs_location.astro_coords.coord_system_id, "UTC-ICRS-TOPO")
        self.assertIsNotNone(obs_location.astro_coords.time)
        self.assertEqual(obs_location.astro_coords.time.time_instant.isotime, "2009-09-25T12:00:00")
        self.assertEqual(obs_location.astro_coords.time.error, 0.0)
        self.assertIsNotNone(obs_location.astro_coords.position_2d)
        self.assertEqual(obs_location.astro_coords.position_2d.unit, "deg")
        self.assertEqual(obs_location.astro_coords.position_2d.value2.c1.value, 37.0603169)
        self.assertEqual(obs_location.astro_coords.position_2d.value2.c2.value, 31.3116578)
        self.assertEqual(obs_location.astro_coords.position_2d.error2_radius.value, 0.03)

    def test_write_to_xml(self):
        """Test writing an ObservationLocation to XML."""
        obs_location_xml = ObservationLocation.to_xml(self.test_element, skip_empty=True)
        self.assertEqual(
            canonicalize(obs_location_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestWhereWhen(TestCase):
    """Test the WhereWhen model."""

    test_xml = """
        <WhereWhen id="Raptor-2455100">
        <ObsDataLocation>
            <ObservatoryLocation id="RAPTOR" />
            <ObservationLocation>
            <AstroCoordSystem id="UTC-ICRS-TOPO" />
            <AstroCoords coord_system_id="UTC-ICRS-TOPO">
                <Time>
                <TimeInstant>
                    <ISOTime>2009-09-25T12:00:00</ISOTime>
                </TimeInstant>
                <Error>0.0</Error>
                </Time>
                <Position2D unit="deg">
                <Value2>
                    <C1>37.0603169</C1>
                    <!-- RA  -->
                    <C2>31.3116578</C2>
                    <!-- Dec -->
                </Value2>
                <Error2Radius>0.03</Error2Radius>
                </Position2D>
            </AstroCoords>
            </ObservationLocation>
        </ObsDataLocation>
        </WhereWhen>
    """

    test_element = WhereWhen(
        id="Raptor-2455100",
        obs_data_location=ObsDataLocation(
            observatory_location=ObservatoryLocation(
                id="RAPTOR",
            ),
            observation_location=ObservationLocation(
                astro_coord_system=AstroCoordSystem(
                    id="UTC-ICRS-TOPO",
                ),
                astro_coords=AstroCoords(
                    coord_system_id="UTC-ICRS-TOPO",
                    time=Time(
                        time_instant=TimeInstant(
                            isotime="2009-09-25T12:00:00",
                        ),
                        error=0.0,
                    ),
                    position2d=Position2D(
                        unit="deg",
                        value2=Value2(
                            c1=CoordValue(value=37.0603169),
                            c2=CoordValue(value=31.3116578),
                        ),
                        error2_radius=CoordValue(value=0.03),
                    ),
                ),
            ),
        ),
    )

    def test_read_from_xml(self):
        """Test reading a WhereWhen from XML."""
        where_when = WhereWhen.from_xml(self.test_xml)
        self.assertIsInstance(where_when, WhereWhen)
        self.assertEqual(where_when.id, "Raptor-2455100")
        self.assertIsNotNone(where_when.obs_data_location)
        self.assertIsNotNone(where_when.obs_data_location.observatory_location)
        self.assertEqual(where_when.obs_data_location.observatory_location.id, "RAPTOR")
        self.assertIsNotNone(where_when.obs_data_location.observation_location)
        obs_location = where_when.obs_data_location.observation_location
        self.assertIsNotNone(obs_location.astro_coord_system)
        self.assertEqual(obs_location.astro_coord_system.id, "UTC-ICRS-TOPO")
        self.assertIsNotNone(obs_location.astro_coords)
        self.assertEqual(obs_location.astro_coords.coord_system_id, "UTC-ICRS-TOPO")
        self.assertIsNotNone(obs_location.astro_coords.time)
        self.assertEqual(obs_location.astro_coords.time.time_instant.isotime, "2009-09-25T12:00:00")
        self.assertEqual(obs_location.astro_coords.time.error, 0.0)
        self.assertIsNotNone(obs_location.astro_coords.position_2d)
        self.assertEqual(obs_location.astro_coords.position_2d.unit, "deg")
        self.assertEqual(obs_location.astro_coords.position_2d.value2.c1.value, 37.0603169)
        self.assertEqual(obs_location.astro_coords.position_2d.value2.c2.value, 31.3116578)
        self.assertEqual(obs_location.astro_coords.position_2d.error2_radius.value, 0.03)

    def test_write_to_xml(self):
        """Test writing a WhereWhen to XML."""
        where_when_xml = WhereWhen.to_xml(self.test_element, skip_empty=True)
        self.assertEqual(
            canonicalize(where_when_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestWhatModel(TestCase):
    """Test the What model."""

    test_xml = """
<What>
  <Description>An imaginary event report about SN 2009lw.</Description>
  <Reference
    uri="http://raptor.lanl.gov/data/lightcurves/235649409"
    mimetype="application/x-votable+xml"
    meaning="http://ivoa.net/rdf/uat#light-curves" />
  <Param name="seeing" value="2" unit="arcsec"
    ucd="instr.obsty.seeing" dataType="float" />
  <Group name="magnitude">
    <Description>Time is days since the ref time in the
      WhereWhen section</Description>
    <Param name="time" value="278.02" unit="d"
      ucd="time.epoch" dataType="float" />
    <Param name="mag" value="19.5" unit="mag"
      ucd="phot.mag" dataType="float" />
    <Param name="magerr" value="0.14" unit="mag"
      ucd="stat.err;phot.mag" dataType="float" />
  </Group>
  <Table>
    <Param name="telescope" value="various" />
    <Description>Individual Moduli and Distances for NGC
      0931
      from NED</Description>
    <Field name="(m-M)" unit="mag" ucd="phot.mag.distMod" />
    <Field name="err(m-M)" unit="mag"
      ucd="stat.err;phot.mag.distMod" />
    <Field name="D" unit="Mpc" ucd="pos.distance" />
    <Field name="REFCODE" ucd="meta.bib.bibcode" />
    <Data>
      <TR><TD>33.16</TD><TD>0.38</TD><TD>51.3</TD><TD>1997ApJS..109..333W</TD></TR>
      <TR><TD>33.32</TD><TD>0.38</TD><TD>46.1</TD><TD>1997ApJS..109..333W</TD></TR>
      <TR><TD>33.51</TD><TD>0.48</TD><TD>50.4</TD><TD>2009ApJS..182..474S</TD></TR>
      <TR><TD>33.55</TD><TD>0.38</TD><TD>51.3</TD><TD>1997ApJS..109..333W</TD></TR>
      <TR><TD>33.71</TD><TD>0.43</TD><TD>55.2</TD><TD>2009ApJS..182..474S</TD></TR>
      <TR><TD>34.01</TD><TD>0.80</TD><TD>63.3</TD><TD>1997ApJS..109..333W</TD></TR>
    </Data>
  </Table>
</What>
"""

    test_model = What(
        description="An imaginary event report about SN 2009lw.",
        reference=Reference(
            uri="http://raptor.lanl.gov/data/lightcurves/235649409",
            mimetype="application/x-votable+xml",
            meaning="http://ivoa.net/rdf/uat#light-curves",
        ),
        param=[
            Param(name="seeing", value="2", unit="arcsec", ucd="instr.obsty.seeing", data_type="float"),
        ],
        group=[
            Group(
                name="magnitude",
                description=["Time is days since the ref time in the WhereWhen section"],
                param=[
                    Param(name="time", value="278.02", unit="d", ucd="time.epoch", data_type="float"),
                    Param(name="mag", value="19.5", unit="mag", ucd="phot.mag", data_type="float"),
                    Param(name="magerr", value="0.14", unit="mag", ucd="stat.err;phot.mag", data_type="float"),
                ],
            ),
        ],
        table=[
            Table(
                param=[
                    Param(name="telescope", value="various"),
                ],
                description=["Individual Moduli and Distances for NGC 0931 from NED"],
                field=[
                    Field(name="(m-M)", unit="mag", ucd="phot.mag.distMod"),
                    Field(name="err(m-M)", unit="mag", ucd="stat.err;phot.mag.distMod"),
                    Field(name="D", unit="Mpc", ucd="pos.distance"),
                    Field(name="REFCODE", ucd="meta.bib.bibcode"),
                ],
                data=Data(
                    rows=[
                        ["33.16", "0.38", "51.3", "1997ApJS..109..333W"],
                        ["33.32", "0.38", "46.1", "1997ApJS..109..333W"],
                        ["33.51", "0.48", "50.4", "2009ApJS..182..474S"],
                        ["33.55", "0.38", "51.3", "1997ApJS..109..333W"],
                        ["33.71", "0.43", "55.2", "2009ApJS..182..474S"],
                        ["34.01", "0.80", "63.3", "1997ApJS..109..333W"],
                    ],
                ),
            )
        ],
    )

    def test_read_from_xml(self):
        """Test reading a What from XML."""
        what = What.from_xml(self.test_xml)
        self.assertIsInstance(what, What)
        self.assertEqual(what.description, "An imaginary event report about SN 2009lw.")
        self.assertIsNotNone(what.reference)
        self.assertEqual(what.reference.uri, "http://raptor.lanl.gov/data/lightcurves/235649409")
        self.assertEqual(len(what.param), 1)
        self.assertEqual(what.param[0].name, "seeing")
        self.assertEqual(len(what.group), 1)
        self.assertEqual(what.group[0].name, "magnitude")
        self.assertIsNotNone(what.table)
        self.assertEqual(len(what.table.field), 4)
        self.assertEqual(len(what.table.data.rows), 6)

    def test_write_to_xml(self):
        """Test writing a What to XML."""
        what_xml = What.to_xml(self.test_model, skip_empty=True)
        self.assertEqual(
            canonicalize(what_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestWhoModel(TestCase):
    """Test the Who model."""

    test_xml = """
    <Who>
        <AuthorIVORN>ivo://raptor.lanl/organization</AuthorIVORN>
        <Date>2005-04-15T14:34:16</Date>
    </Who>
    """

    test_element = Who(
        author_ivorn="ivo://raptor.lanl/organization",
        date="2005-04-15T14:34:16",
    )

    def test_read_from_xml(self):
        """Test reading a Who from XML."""
        who = Who.from_xml(self.test_xml)
        self.assertIsInstance(who, Who)
        self.assertEqual(who.author_ivorn, "ivo://raptor.lanl/organization")
        self.assertEqual(who.date, "2005-04-15T14:34:16")

    def test_write_to_xml(self):
        """Test writing a Who to XML."""
        who_xml = Who.to_xml(self.test_element, skip_empty=True)
        self.assertEqual(
            canonicalize(who_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestWhyModel(TestCase):
    """Test the Why model."""

    test_xml = """
    <Why>
        <Concept>http://ivoat.ivoa.net/process.variation.burst;em.opt</Concept>
        <Description>Looks like a SN</Description>
        <Inference relation="associated" probability="0.99">
            <Name>NGC0931</Name>
        </Inference>
    </Why>
    """

    test_element = Why(
        concept="http://ivoat.ivoa.net/process.variation.burst;em.opt",
        description="Looks like a SN",
        inference=Inference(
            relation="associated",
            probability=0.99,
            name="NGC0931",
        ),
    )

    def test_read_from_xml(self):
        """Test reading a Why from XML."""
        why = Why.from_xml(self.test_xml)
        self.assertIsInstance(why, Why)
        self.assertEqual(why.concept, "http://ivoat.ivoa.net/process.variation.burst;em.opt")
        self.assertEqual(why.description, "Looks like a SN")
        self.assertIsNotNone(why.inference)
        self.assertEqual(why.inference.relation, "associated")
        self.assertEqual(why.inference.probability, 0.99)
        self.assertEqual(why.inference.name, "NGC0931")

    def test_write_to_xml(self):
        """Test writing a Why to XML."""
        why_xml = Why.to_xml(self.test_element, skip_empty=True)
        self.assertEqual(
            canonicalize(why_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestVOEventModel(TestCase):
    """Test the VOEvent model."""

    test_xml = """
<voe:VOEvent ivorn="ivo://raptor.lanl/VOEvent#235649409"
  role="observation"
  version="2.1"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:voe="http://www.ivoa.net/xml/VOEvent/v2.1">
  <Who>
    <AuthorIVORN>ivo://raptor.lanl/organization</AuthorIVORN>
    <Date>2005-04-15T14:34:16</Date>
  </Who>
  <What>
    <Description>An imaginary event report about SN 2009lw.</Description>
    <Reference
      uri="http://raptor.lanl.gov/data/lightcurves/235649409"
      mimetype="application/x-votable+xml"
      meaning="http://ivoa.net/rdf/uat#light-curves" />
    <Param name="seeing" value="2" unit="arcsec"
      ucd="instr.obsty.seeing" dataType="float" />
    <Group name="magnitude">
      <Description>Time is days since the ref time in the
        WhereWhen section</Description>
      <Param name="time" value="278.02" unit="d"
        ucd="time.epoch" dataType="float" />
      <Param name="mag" value="19.5" unit="mag"
        ucd="phot.mag" dataType="float" />
      <Param name="magerr" value="0.14" unit="mag"
        ucd="stat.err;phot.mag" dataType="float" />
    </Group>
  </What>
  <WhereWhen id="Raptor-2455100">
    <ObsDataLocation>
      <ObservatoryLocation id="RAPTOR" />
      <ObservationLocation>
        <AstroCoordSystem id="UTC-ICRS-TOPO" />
        <AstroCoords coord_system_id="UTC-ICRS-TOPO">
          <Time>
            <TimeInstant>
              <ISOTime>2009-09-25T12:00:00</ISOTime>
            </TimeInstant>
            <Error>0.0</Error>
          </Time>
          <Position2D unit="deg">
            <Value2>
              <C1>37.0603169</C1>
              <!-- RA  -->
              <C2>31.3116578</C2>
              <!-- Dec -->
            </Value2>
            <Error2Radius>0.03</Error2Radius>
          </Position2D>
        </AstroCoords>
      </ObservationLocation>
    </ObsDataLocation>
  </WhereWhen>
  <How>
    <Description>
      <![CDATA[This VOEvent packet resulted from observations made with
        <a href=http://www.raptor.lanl.gov>Raptor</a> AB at Los Alamos. ]]>
    </Description>
  </How>
  <Citations>
    <EventIVORN cite="followup">ivo://raptor.lanl/VOEvent#235649408</EventIVORN>
  </Citations>
  <Why>
    <Concept>http://ivoat.ivoa.net/process.variation.burst;em.opt</Concept>
    <Description>Looks like a SN</Description>
    <Inference relation="associated" probability="0.99">
      <Name>NGC0931</Name>
    </Inference>
  </Why>
</voe:VOEvent>
"""

    test_model = VOEvent(
        ivorn="ivo://raptor.lanl/VOEvent#235649409",
        role=RoleValues.OBSERVATION,
        version="2.1",
        who=Who(
            author_ivorn="ivo://raptor.lanl/organization",
            date="2005-04-15T14:34:16",
        ),
        what=What(
            description="An imaginary event report about SN 2009lw.",
            reference=Reference(
                uri="http://raptor.lanl.gov/data/lightcurves/235649409",
                mimetype="application/x-votable+xml",
                meaning="http://ivoa.net/rdf/uat#light-curves",
            ),
            param=[
                Param(name="seeing", value="2", unit="arcsec", ucd="instr.obsty.seeing", data_type="float"),
            ],
            group=[
                Group(
                    name="magnitude",
                    description=["Time is days since the ref time in the WhereWhen section"],
                    param=[
                        Param(name="time", value="278.02", unit="d", ucd="time.epoch", data_type="float"),
                        Param(name="mag", value="19.5", unit="mag", ucd="phot.mag", data_type="float"),
                        Param(name="magerr", value="0.14", unit="mag", ucd="stat.err;phot.mag", data_type="float"),
                    ],
                ),
            ],
        ),
        where_when=WhereWhen(
            id="Raptor-2455100",
            obs_data_location=ObsDataLocation(
                observatory_location=ObservatoryLocation(
                    id="RAPTOR",
                ),
                observation_location=ObservationLocation(
                    astro_coord_system=AstroCoordSystem(
                        id="UTC-ICRS-TOPO",
                    ),
                    astro_coords=AstroCoords(
                        coord_system_id="UTC-ICRS-TOPO",
                        time=Time(
                            time_instant=TimeInstant(
                                isotime="2009-09-25T12:00:00",
                            ),
                            error=0.0,  
                        ),
                        position2d=Position2D(
                            unit="deg",
                            value2=Value2(
                                c1=CoordValue(value=37.0603169),
                                c2=CoordValue(value=31.3116578),
                            ),
                            error2_radius=CoordValue(value=0.03),
                        ),
                    ),
                ),
            ),
            how=How(
                description=(
                    "This VOEvent packet resulted from observations made with "
                    "<a href=http://www.raptor.lanl.gov>Raptor</a> AB at Los Alamos. "
                ),
            ),
            citations=Citations(
                event_ivorn=[
                    EventIVORN(
                        value="ivo://raptor.lanl/VOEvent#235649408",
                        cite="followup",
                    ),
                ],
            ),
            why=Why(
                concept="http://ivoat.ivoa.net/process.variation.burst;em.opt",
                description="Looks like a SN",
                inference=Inference(
                    relation="associated",
                    probability=0.99,
                    name="NGC0931",
                ),
            ),
        ),
    )

    def test_read_from_xml(self):
        """Test reading a VOEvent from XML."""
        voevent = VOEvent.from_xml(self.test_xml)
        self.assertIsInstance(voevent, VOEvent)
        self.assertEqual(voevent.ivorn, "ivo://raptor.lanl/VOEvent#235649409")
        self.assertEqual(voevent.role, RoleValues.OBSERVATION)
        self.assertIsNotNone(voevent.who)
        self.assertIsNotNone(voevent.what)
        self.assertIsNotNone(voevent.where_when)
        self.assertIsNotNone(voevent.how)
        self.assertIsNotNone(voevent.citations)
        self.assertIsNotNone(voevent.why)

    def test_write_to_xml(self):
        """Test writing a VOEvent to XML."""
        voevent_xml = VOEvent.to_xml(self.test_model, skip_empty=True)
        self.assertEqual(
            canonicalize(voevent_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )
