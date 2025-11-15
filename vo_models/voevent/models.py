"""XML Element and ComplexType models for VOEvent v2.1"""

from typing import Annotated, Literal, Optional
from warnings import warn

import pydantic
from pydantic import field_validator, networks
from pydantic_xml import BaseXmlModel, attr, element

from vo_models.voevent.types import CiteValues, DataType, RoleValues

NSMAP = {"voe": "http://www.ivoa.net/xml/VOEvent/v2.1"}


class CoordValue(BaseXmlModel, nsmap=NSMAP):
    """Element for each axis in SpaceFrame

    Parameters:
        ucd: (attr) - UCD string for the coordinate value
        pos_unit: (attr) - Unit string for the coordinate value
        value: - The coordinate value
    """

    value: float

    ucd: Optional[str] = attr(name="ucd", default=None)
    pos_unit: Optional[str] = attr(name="pos_unit", default=None)


class EventIVORN(BaseXmlModel, nsmap=NSMAP):
    """Citations/EventIVORN.

    The value is the IVORN of the cited event, the 'cite' attribute is the nature of that relationship, choosing from
    'followup', 'supersedes', or 'retraction'.

    Parameters:
        value: - The IVORN of the cited event
        cite: (attr) - The nature of the citation
    """

    value: str

    cite: Optional[CiteValues] = attr(name="cite", default=None)


class Name(BaseXmlModel, nsmap=NSMAP):
    """A simple Name element used for Contributor names.

    Parameters:
        alt_identifier:
            (attr) - Alternate contact identifier in URI form. The main usage is to refer
                        to ORCIDs (e.g.: https://orcid.org/0000-0001-2345-6789)
        role:
            (attr) - Role of the Contributor
        ivorn:
            (attr) - Person id in the VO registry, if available
        value:
            - The name of the contributor
    """

    value: str

    alt_identifier: Optional[networks.AnyUrl] = attr(name="altIdentifier", default=None)
    role: Optional[str] = attr(name="role", default=None)
    ivorn: Optional[networks.AnyUrl] = attr(name="ivorn", default=None)


class TimeInstant(BaseXmlModel, nsmap=NSMAP):
    """Part of WhereWhen

    Parameters:
        isotime: (elem) - The ISOTime string
        time_offset: (elem) - The TimeOffset value
        time_scale: (elem) - The TimeScale string
    """

    isotime: Optional[str] = element(tag="ISOTime", default=None)
    time_offset: Optional[float] = element(tag="TimeOffset", default=None)
    time_scale: Optional[str] = element(tag="TimeScale", default=None)


class TimeInterval(BaseXmlModel, nsmap=NSMAP):
    """Part of WhereWhen

    Parameters:
        iso_time_start: (elem) - The ISOTimeStart string
        iso_time_stop: (elem) - The ISOTimeStop string
    """

    iso_time_start: Optional[str] = element(tag="ISOTimeStart", default=None)
    iso_time_stop: Optional[str] = element(tag="ISOTimeStop", default=None)


class Time(BaseXmlModel, nsmap=NSMAP):
    """Part of WhereWhen

    Parameters:
        unit: (attr) - The unit string for the time value
        time_instant: (elem) - The TimeInstant element
        time_interval: (elem) - The TimeInterval element
        error: (elem) - The Error value
    """

    unit: Optional[str] = attr(name="unit", default=None)

    time_instant: Optional[TimeInstant] = element(tag="TimeInstant", default=None)
    time_interval: Optional[TimeInterval] = element(tag="TimeInterval", default=None)
    error: Optional[float] = element(tag="Error", default=None)


class Value2(BaseXmlModel, nsmap=NSMAP):
    """Part of WhereWhen"""

    c1: CoordValue = element(tag="C1")
    c2: CoordValue = element(tag="C2")


class Value3(BaseXmlModel, nsmap=NSMAP):
    """Part of WhereWhen"""

    c1: CoordValue = element(tag="C1")
    c2: CoordValue = element(tag="C2")
    c3: CoordValue = element(tag="C3")


class Error2(BaseXmlModel, nsmap=NSMAP):
    """Part of WhereWhen"""

    c1: Optional[CoordValue] = element(tag="C1", default=None)
    c2: Optional[CoordValue] = element(tag="C2", default=None)


class Error3(BaseXmlModel, nsmap=NSMAP):
    """Part of WhereWhen"""

    c1: Optional[CoordValue] = element(tag="C1", default=None)
    c2: Optional[CoordValue] = element(tag="C2", default=None)
    c3: Optional[CoordValue] = element(tag="C3", default=None)


class Position2D(BaseXmlModel, nsmap=NSMAP):
    """Part of WhereWhen

    Parameters:
        unit: - (attr) The unit string for the coordinate values
        name1: - (elem) The name of the first coordinate axis
        name2: - (elem) The name of the second coordinate axis
        value2: - (elem) The Value2 element holding the two coordinate values
        error2radius: - (elem) The Error2Radius value
        error2: - (elem) The Error2 element holding the two coordinate errors
    """

    unit: Optional[str] = attr(name="unit", default=None)
    name1: Optional[str] = element(tag="Name1", default=None)
    name2: Optional[str] = element(tag="Name2", default=None)
    value2: Value2 = element(tag="Value2")
    error2radius: Optional[CoordValue] = element(tag="Error2Radius", default=None)
    error2: Optional[Error2] = element(tag="Error2", default=None)


class Position3D(BaseXmlModel, nsmap=NSMAP):
    """Part of WhereWhen: Position for the event (3D coordSystem)

    Parameters:
        unit: - (attr) The unit string for the coordinate values
        name1: - (elem) The name of the first coordinate
        name2: - (elem) The name of the second coordinate
        name3: - (elem) The name of the third coordinate
        value3: - (elem) The Value3 element holding the three coordinate values
        error3: - (elem) The Error3 element holding the three coordinate errors
    """

    unit: Optional[str] = attr(name="unit", default=None)

    name1: Optional[str] = element(tag="Name1", default=None)
    name2: Optional[str] = element(tag="Name2", default=None)
    name3: Optional[str] = element(tag="Name3", default=None)

    value3: Value3 = element(tag="Value3")
    error3: Optional[Error3] = element(tag="Error3", default=None)


class Citations(BaseXmlModel, nsmap=NSMAP):
    """
    Follow-up Observations. This section is a sequence of EventIVORN elements, each of which has the IVORN of a cited
    event.

    Parameters:
        event_ivorn: (elem) - The EventIVORN elements
        description: (elem) - An optional description of the citations
    """

    event_ivorn: list[EventIVORN] = element(tag="EventIVORN")
    description: Optional[str] = element(tag="Description", default=None)


class Reference(BaseXmlModel, nsmap=NSMAP):
    """
    Reference: External Content.

    The payload is the URI, and the 'type' describes the nature of the data under that URI.
    The Reference can also be named.

    Parameters:
        uri: (attr) - The URI string
        type: (attr) - The type string
        mimetype: (attr) - The mimetype string
        meaning: (attr) - The meaning string
    """

    uri: str = attr(name="uri")
    type: Optional[str] = attr(name="type", default=None)
    mimetype: Optional[str] = attr(name="mimetype", default=None)
    meaning: Optional[str] = attr(name="meaning", default=None)


class How(BaseXmlModel, nsmap=NSMAP):
    """How: Instrument Configuration. Built with some Description and Reference elements.

    Parameters:
        description: (elem) - The Description element
        reference: (elem) - The Reference element
    """

    description: str = element(tag="Description")
    reference: Reference = element(tag="Reference")


class AstroCoords(BaseXmlModel, nsmap=NSMAP):
    """
    AstroCoords: Part of Where/When

    Parameters:
        coord_system_id: (attr) - The id of the coordinate system
        time: (elem) - Time instant or Time Interval for the event
        position_name: (elem) - Named position for the event or an observatory
        position_2d: (elem) - Position for the event (2D coordSystem)
        position_3d: (elem) - Position for the event (3D coordSystem)
    """

    coord_system_id: Optional[str] = attr(name="coord_system_id", default=None)

    time: Optional[Time] = element(tag="Time", default=None)
    position_name: Optional[str] = element(tag="PositionName", default=None)
    position_2d: Optional[Position2D] = element(tag="Position2D", default=None)
    position_3d: Optional[Position3D] = element(tag="Position3D", default=None)


class TimeFrameType(BaseXmlModel, nsmap=NSMAP):
    """
    The time reference frame consists of a time scale, a time format, and a reference time, if needed.
    A TimeFrame has to have at least an Id.

    Parameters:
        id: (attr) - The id of the TimeFrame
        name: (elem) - The name of the TimeFrame
        reference_position: (elem) - Origin of the coordinate reference frame: either a "known place" such as
            geocenter or barycenter, or a position defined in a known coordinate
            system. Values should be taken from: http://www.ivoa.net/rdf/refposition
        timescale: (elem) - The TimeScale of the TimeFrame

    """

    id: Optional[str] = attr(name="id", default=None)
    name: Optional[str] = element(tag="Name", default=None)
    reference_position: Optional[str] = element(tag="ReferencePosition", default=None)
    timescale: Optional[str] = element(tag="TimeScale", default=None)


class SpaceFrameType(BaseXmlModel, nsmap=NSMAP):
    """A SpaceFrame has to have at least an Id

    Parameters:
        id: (attr) - The id of the SpaceFrame
        name: (elem) - The name of the SpaceFrame
        space_ref_frame: (elem) - Coordinate reference frame: optional equinox with either a standard
            reference system (ICRS, FK5, FK4) and optional standard pole (equatorial, ecliptic,
            galactic, etc.), or pole (positive Z-axis) and positive X-axis direction. Values should
            be taken from: http://www.ivoa.net/rdf/refframe
        coord_flavor: (elem) - Provides the coordinate definitions: number of axes, SPHERICAL,
            CARTESIAN, UNITSPHERE, POLAR, or HEALPIX, presence of velocities
        reference_position: (elem) - Origin of the coordinate reference frame: either a "known place" such as
            geocenter or barycenter, or a position defined in a known coordinate
            system. Values should be taken from: http://www.ivoa.net/rdf/refposition
    """

    id: Optional[str] = attr(name="id", default=None)

    name: Optional[str] = element(tag="Name", default=None)
    space_ref_frame: Optional[str] = element(tag="SpaceRefFrame", default=None)
    coord_flavor: Optional[str] = element(tag="CoordFlavor", default=None)
    reference_position: Optional[str] = element(tag="ReferencePosition", default=None)


class AstroCoordSystem(BaseXmlModel, nsmap=NSMAP):
    """
    AstroCoordSystem: Part of Where/When

    Parameters:
        time_frame: (elem) - The TimeFrame element
        space_frame: (elem) - The SpaceFrame element
        id: (attr) - The id of the AstroCoordSystem
    """

    time_frame: Optional[TimeFrameType] = element(tag="TimeFrame", default=None)
    space_frame: Optional[SpaceFrameType] = element(tag="SpaceFrame", default=None)

    id: Optional[str] = attr(name="id", default=None)


class ObservationLocation(BaseXmlModel, nsmap=NSMAP):
    """
    ObservationLocation: Part of Where/When

    Parameters:
        astro_coord_system: (elem) - The AstroCoordSystem element
        astro_coords: (elem) - The AstroCoords element
    """

    astro_coord_system: AstroCoordSystem = element(tag="AstroCoordSystem")
    astro_coords: AstroCoords = element(tag="AstroCoords")


class ObservatoryLocation(BaseXmlModel, nsmap=NSMAP):
    """Part of WhereWhen

    Parameters:
        id: (attr) - The id of the ObservatoryLocation
        astrocoordsystem: (elem) - The AstroCoordSystem element
    """

    id: Optional[str] = attr(name="id", default=None)

    astro_coord_system: Optional[AstroCoordSystem] = element(tag="AstroCoordSystem", default=None)
    astro_coords: Optional[AstroCoords] = element(tag="AstroCoords", default=None)


class ObsDataLocation(BaseXmlModel, nsmap=NSMAP):
    """
    ObsDataLocation: Part of Where/When

    Parameters:
        observatory_location: (elem) - The ObservatoryLocation element
        observation_location: (elem) - The ObservationLocation element
    """

    observatory_location: ObservatoryLocation = element(tag="ObservatoryLocation")
    observation_location: ObservationLocation = element(tag="ObservationLocation")


class WhereWhen(BaseXmlModel, nsmap=NSMAP):
    """
    WhereWhen: Space-Time Coordinates.

    Each event has these: observatory, coord_system, time, timeError, longitude, latitude, posError.

    Parameters:
        obs_data_location: (elem) - The ObsDataLocation element
        description: (elem) - An optional description of the location
        reference: (elem) - An optional reference for the location
        id: (attr) - The id of the WhereWhen
    """

    obs_data_location: ObsDataLocation = element(tag="ObsDataLocation")
    description: Optional[list[str]] = element(tag="Description", default_factory=list)
    reference: Optional[list[Reference]] = element(tag="Reference", default_factory=list)

    id: Optional[str] = attr(name="id", default=None)


class Param(BaseXmlModel, nsmap=NSMAP):
    """
    What/Param definition.

    A Param has name, value, ucd, unit, dataType and may have Description and Refence.

    Parameters:
        description: (elem) - The Description element
        reference: (elem) - The Reference element
        value: (attr) - The value of the Param
        name: (attr) - The name of the Param
        ucd: (attr) - The UCD of the Param
        unit: (attr) - The unit of the Param
        data_type: (attr) - The dataType of the Param
        utype: (attr) - The utype of the Param
    """

    description: Optional[list[str]] = element(tag="Description", default_factory=list)
    reference: Optional[list[Reference]] = element(tag="Reference", default_factory=list)
    value: Optional[str] = element(tag="Value", default=None)

    value_attr: Optional[str] = attr(name="value", default=None)
    name: Optional[str] = attr(name="name", default=None)
    ucd: Optional[str] = attr(name="ucd", default=None)
    unit: Optional[str] = attr(name="unit", default=None)
    data_type: Optional[Literal["string", "int", "float"]] = attr(name="dataType", default=DataType.STRING)
    utype: Optional[str] = attr(name="utype", default=None)


class Group(BaseXmlModel, nsmap=NSMAP):
    """
    What/Group definition.

    A group is a collection of Params with name and type attributes.

    Parameters:
        param: (elem) - The Param elements
        description: (elem) - The Description elements
        reference: (elem) - The Reference elements
        name: (attr) - The name of the Group
        type: (attr) - The type of the Group
    """

    param: Optional[list[Param]] = element(tag="Param", default_factory=list)
    description: Optional[list[str]] = element(tag="Description", default_factory=list)
    reference: Optional[list[Reference]] = element(tag="Reference", default_factory=list)

    name: Optional[str] = attr(name="name", default=None)
    type: Optional[str] = attr(name="type", default=None)


class Field(BaseXmlModel, nsmap=NSMAP):
    """
    What/Table Field definition.
    """

    description: Optional[list[str]] = element(tag="Description", default_factory=list)
    reference: Optional[list[Reference]] = element(tag="Reference", default_factory=list)

    name: Optional[str] = attr(name="name", default=None)
    ucd: Optional[str] = attr(name="ucd", default=None)
    unit: Optional[str] = attr(name="unit", default=None)
    data_type: Optional[DataType] = attr(name="dataType", default=DataType.STRING)
    utype: Optional[str] = attr(name="utype", default=None)


class TR(BaseXmlModel, nsmap=NSMAP):
    """
    What/Table TR (table row) definition.
    """

    td: list[str] = element(tag="TD", default_factory=list)


class Data(BaseXmlModel, nsmap=NSMAP):
    """
    What/Table Data definition.
    """

    tr: list[TR] = element(tag="TR", default_factory=list)


class Table(BaseXmlModel, nsmap=NSMAP):
    """
    What/Table definition.

    This small Table has Fields for the column definitions, and Data to hold the table data, with TR for row and TD for
    value of a table cell.

    Parameters:
        description: (elem) - The Description elements
        reference: (elem) - The Reference elements
        param: (elem) - The Param elements
        field: (elem) - The Field elements
        data: (elem) - The Data element
        name: (attr) - The name of the Table
        type: (attr) - The type of the Table
    """

    description: Optional[list[str]] = element(tag="Description", default_factory=list)
    reference: Optional[Reference] = element(tag="Reference", default_factory=list)
    param: Optional[list[Param]] = element(tag="Param", default_factory=list)
    field: Optional[list[Field]] = element(tag="Field", default_factory=list)
    data: Data = element(tag="Data", default=None)

    name: Optional[str] = attr(name="name", default=None)
    type: Optional[str] = attr(name="type", default=None)


class What(BaseXmlModel, nsmap=NSMAP):
    """
    What: Event Characterization.

    This is the part of the data model that is chosen by the Authoer of the event rather than the IVOA.
    There can be Params, that may be in Groups, and Tables, and simpleTimeSeries. There can also be Description and
    Reference as with most VOEvent elements.

    Parameters:
        param: (elem) - The Param elements
        group: (elem) - The Group elements
        table: (elem) - The Table elements
        description: (elem) - The Description element
        reference: (elem) - The Reference element
    """

    param: Optional[list[Param]] = element(tag="Param", default_factory=list)
    group: Optional[list[Group]] = element(tag="Group", default_factory=list)
    table: Optional[list[Table]] = element(tag="Table", default_factory=list)
    # This is commented out in the XSD schema and not implemented in this model for now.
    # simple_time_series: Optional[list["SimpleTimeSeries"]] = element(tag="SimpleTimeSeries", default_factory=list)
    description: Optional[str] = element(tag="Description", default=None)
    reference: Optional[Reference] = element(tag="Reference", default=None)


class Author(BaseXmlModel, nsmap=NSMAP):
    """
    Author information follows the IVOA curation information schema:

    The organization responsible for the packet can have a title, short name or acronym, and a
    logo. A contact person has a name, email, and phone number. Other contributors can also
    be noted.
    """

    title: Optional[list[str]] = element(tag="title", default_factory=list)
    short_name: Optional[list[str]] = element(tag="shortName", default_factory=list)
    logo_url: Optional[list[str]] = element(tag="logoURL", default_factory=list)
    contact_name: Optional[list[str]] = element(tag="contactName", default_factory=list)
    contact_email: Optional[list[str]] = element(tag="contactEmail", default_factory=list)
    contact_phone: Optional[list[str]] = element(tag="contactPhone", default_factory=list)
    contributor: Optional[list[Name]] = element(tag="Contributor", default_factory=list)

    def __init__(self, **data):
        if "contributor" in data:
            if isinstance(data["contributor"], list):
                for idx, contrib in enumerate(data["contributor"]):
                    if isinstance(contrib, str):
                        data["contributor"][idx] = Name(value=contrib)
                        warn(
                            "The 'contributor' parameter as a simple string is deprecated and will be removed in a future version of VOEvent. Use the 'Contibutor' model instead.",
                            DeprecationWarning,
                            stacklevel=2,
                        )
        super().__init__(**data)

    @field_validator("title", "short_name", "logo_url", "contact_name", "contact_email", "contact_phone", mode="before")
    @classmethod
    def ensure_list(cls, v):
        """Allow single values to be passed in and convert them to lists."""
        if v is None:
            return []
        if isinstance(v, list):
            return v
        return [v]


class Who(BaseXmlModel, nsmap=NSMAP):
    """
    Who: Curation Metadata for the VOEvent
    """

    author_ivorn: Optional[str] = element(tag="AuthorIVORN", default=None)
    date: Optional[str] = element(tag="Date", default=None)
    description: Optional[str] = element(tag="Description", default=None)

    reference: Optional[Reference] = element(tag="Reference", default=None)
    author: Optional[Author] = element(tag="Author", default=None)


class Inference(BaseXmlModel, nsmap=NSMAP):
    """Why/Inference: A container for a more nuanced expression, including relationships and probability."""

    value: Annotated[float, pydantic.Field(ge=0.0, le=1.0)]

    probability: Optional[float] = attr(name="probability", default=None)
    relation: Optional[str] = attr(name="relation", default=None)

    name: str = element(tag="Name")
    concept: str = element(tag="Concept")
    description: str = element(tag="Description")
    reference: Reference = element(tag="Reference")


class Why(BaseXmlModel, nsmap=NSMAP):
    """Why: Initial Scientific Assessment.

    Can make simple Concept/Name/Desc/Ref for the inference or use multiple Inference containers for more semantic
    sophistication.
    """

    importance: Optional[float] = attr(name="importance", default=None)
    expires: Optional[str] = attr(name="expires", default=None)

    name: str = element(tag="Name")
    concept: str = element(tag="Concept")
    inference: Inference = element(tag="Inference")
    description: str = element(tag="Description")
    reference: Reference = element(tag="Reference")


class VOEvent(BaseXmlModel, tag="VOEvent", ns="voe", nsmap=NSMAP):
    """
    VOEvent is the root element for describing observations of immediate
        astronomical events. For more information, see
        http://www.ivoa.net/twiki/bin/view/IVOA/IvoaVOEvent. The event consists of at most one of
        each of: Who, What, WhereWhen, How, Why, Citations, Description, and
        Reference.
    """

    who: Optional[Who] = element(tag="Who", default=None)
    what: Optional[What] = element(tag="What", default=None)
    where_when: Optional[WhereWhen] = element(tag="WhereWhen", default=None)
    how: Optional[How] = element(tag="How", default=None)
    why: Optional[Why] = element(tag="Why", default=None)
    citations: Optional[Citations] = element(tag="Citations", default=None)
    description: Optional[str] = element(tag="Description", default=None)
    reference: Optional[Reference] = element(tag="Reference", default=None)

    version: Literal["2.1"] = attr(name="version", default="2.1")
    ivorn: str = attr(name="ivorn")
    role: Optional[RoleValues] = attr(name="role", default=RoleValues.OBSERVATION)
