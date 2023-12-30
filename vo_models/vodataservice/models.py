"""Pydantic-xml models for IVOA schema VODataService-v1.2.xsd"""

from typing import Literal, Optional

from pydantic_xml import BaseXmlModel, attr, element

from vo_models.stc.models import STCDescriptionType, STCResourceProfile
from vo_models.vodataservice.types import (
    ArrayShape,
    FloatInterval,
    HTTPQueryType,
    ParamUse,
)
from vo_models.voresource.models import AccessURL, Interface, Resource, ResourceName, Rights, Service
from vo_models.voresource.types import IdentifierURI

NSMAP = {
    "xml": "http://www.w3.org/XML/1998/namespace",
    "xs": "http://www.w3.org/2001/XMLSchema",
    "vr": "http://www.ivoa.net/xml/VOResource/v1.0",
    "vs": "http://www.ivoa.net/xml/VODataService/v1.1",
    "stc": "http://www.ivoa.net/xml/STC/stc-v1.30.xsd",
    "vm": "http://www.ivoa.net/xml/VOMetadata/v0.1",
    "": "",
}


class SpatialCoverage(BaseXmlModel, ns="vs", nsmap=NSMAP):
    """
    A coverage on a sphere.

    By default, this refers to the celestial sphere in the ICRS frame. Non-celestial frames are indicated by
    non-NULL values of the frame attribute.

    Parameters:
        value (str):
            An ASCII-serialized MOC defining the spatial coverage of the resource.
        frame (str):
            (attr) - When present, the MOC is written in a non-celestial (e.g., planetary) frame.

                    Note that for celestial coverages, ICRS must be used.
                    VODataService 1.2 does not prescribe a vocabulary for what values are allowed here.  As long as no
                    such vocabulary is agreed upon, the frame attribute should not be set.
    """

    value: Optional[str] = None

    frame: Optional[str] = attr(default=None)


class ServiceReference(BaseXmlModel, ns="vs", nsmap=NSMAP):
    """The service URL for a potentially registered service.

    That is, if an IVOA identifier is also provided, then the service is described in a registry.

    Parameters:
        value (str):
            (content) - The URL of the service.
        ivo_id (IdentifierURI):
            (attr) - The URI form of the IVOA identifier for the service describing the capability refered to by
            this element.
    """

    value: Optional[str] = None

    ivo_id: Optional[IdentifierURI] = attr(name="ivo-id")


class Format(BaseXmlModel, ns="vs", nsmap=NSMAP):
    """
    The physical or digital manifestation of the information supported by a resource.

    This should use RFC 2046 media (“MIME”) types for network-retrievable, digital data.

    Parameters:
        is_mimetype (bool):
            (attr) - If true, the value of this element is a MIME type.
    """

    is_mimetype: Optional[bool] = attr(name="isMIMEType", default=False)


class DataType(BaseXmlModel, ns="vs", nsmap=NSMAP):
    """
    A type (in the computer language sense) associated with a parameter with an arbitrary name

    This XML type is used as a parent for defining data types with a restricted set of names.

    Parameters:
        value (str):
            The name of the data type.
        arraysize (ArrayShape):
            (attr) - The shape of the array that constitutes the value.
        delim (str):
            (attr) - A string that is used to delimit elements of an array value in InputParams.
        extended_type (str):
            (attr) - The data value represented by this type can be interpreted as of a custom type
            identified by the value of this attribute.
        extended_schema (str):
            (attr) - An identifier for the schema that the value given by the extended attribute is drawn from.
    """

    value: Optional[str] = None

    arraysize: ArrayShape = attr(name="arraysize")
    delim: str = attr(name="delim")
    extended_type: str = attr(name="extendedType")
    extended_schema: str = attr(name="extendedSchema")


class SimpleDataType(DataType, ns="vs", nsmap=NSMAP):
    """
    A data type restricted to a small set of names which is imprecise as to the format of the individual values.

    This set is intended for describing simple input parameters to a service or function.
    """

    value: Literal[
        "integer",
        "real",
        "complex",
        "boolean",
        "char",
        "string",
    ]


class TableDataType(DataType, ns="vs", nsmap=NSMAP):
    """
    An abstract parent for a class of data types that can be used to specify the data type of a table column.
    """


class VOTableType(BaseXmlModel, ns="vs", nsmap=NSMAP):
    """
    A data type supported explicitly by the VOTable format
    """

    value: Literal[
        "boolean",
        "bit",
        "unsignedByte",
        "short",
        "int",
        "long",
        "char",
        "unicodeChar",
        "float",
        "double",
        "floatComplex",
        "doubleComplex",
    ]


class TAPDataType(TableDataType, ns="vs", nsmap=NSMAP):
    """
    An abstract parent for the specific data types supported by the Table Access Protocol.

    Parameters:
        size (int):
            (attr) - The length of the fixed-length value.
    """

    size: int = attr(gt=0)


class TAPType(TAPDataType, ns="vs", nsmap=NSMAP):
    """
    A data type supported explicitly by the Table Access Protocol (v1.0).

    This is deprecated in VODataService 1.2, and even TAP 1.0 services are encouraged to declare their columns
    using VOTableType.
    """

    value: Literal[
        "BOOLEAN",
        "SMALLINT",
        "INTEGER",
        "BIGINT",
        "REAL",
        "DOUBLE",
        "TIMESTAMP",
        "CHAR",
        "VARCHAR",
        "BINARY",
        "VARBINARY",
        "POINT",
        "REGION",
        "CLOB",
        "BLOB",
    ]


class Coverage(BaseXmlModel, ns="vs", nsmap=NSMAP):
    """
    A description of how a resource's contents or behavior maps to the sky, to time, and to frequency space,
    including coverage and resolution.

    Parameters:
        STCResourceProfile (STCResourceProfile):
            (element) - An STC 1.0 description of the location of the resource's data on the sky, in time, and
            in frequency space, including resolution.

                This is deprecated in favour of the separate spatial, temporal, and spectral elements.

        spatial (SpatialCoverage):
            (element) - An ASCII-serialized MOC defining the spatial coverage of the resource.

                The MOC is to be understood in the ICRS reference frame unless a frame attribute is given.

        temporal (FloatInterval):
            (element) - A pair of lower, upper limits of a time interval for which the resource offers data.

                This is written as for VOTable tabledata (i.e., whitespace-separated C-style floating point literals), as
                in “47847.2 51370.2”.

        spectral (FloatInterval):
            (element) - A pair of lower, upper limits of a spectral interval for which the resource offers data.

        footprint (ServiceReference)
            (element) - A reference to a footprint service for retrieving precise and up-to-date
            description of coverage.

        waveband (str):
            (element) - A name of a messenger that the resource is relevant for (e.g., was used in the measurements).

                Terms must be taken from the vocabulary at http://www.ivoa.net/rdf/messenger.

        regionOfRegard (float):
            (element) - A single numeric value representing the angle, given in decimal degrees, by which a positional
            query against this resource should be “blurred” in order to get an appropriate match.
    """

    # TODO: STCResourceProfile is not implemented
    stcresource_profile: Optional[STCResourceProfile] = element(tag="STCResourceProfile")
    spatial: Optional[SpatialCoverage] = element(default=None)
    temporal: Optional[list[FloatInterval]] = element(default=None)
    spectral: Optional[list[FloatInterval]] = element(default=None)
    footprint: Optional[ServiceReference] = element(default=None)
    waveband: Optional[str] = element(default=None)
    region_of_regard: Optional[float] = element(tag="regionOfRegard", default=None)


class BaseParam(BaseXmlModel, ns="vs", nsmap=NSMAP):
    """
    A description of a parameter that places no restriction on the parameter's data type.

    Parameters:
        name (str):           (element) - The name of the parameter or column.
        description (str):    (element) - A free-text description of a parameter's or column's contents.
        unit (str):           (element) - The unit associated with the values in the parameter or column.
        ucd (str):
            (element) - The name of a unified content descriptor that describes the scientific content  of the parameter
        utype (str):
            (element) - An identifier for a concept in a data model that the data in this schema represent.
    """

    name: Optional[str] = element(default=None)
    description: Optional[str] = element(default=None)
    unit: Optional[str] = element(default=None)
    ucd: Optional[str] = element(default=None)
    utype: Optional[str] = element(default=None)


class TableParam(BaseParam, ns="vs", nsmap=NSMAP):
    """
    A description of a table parameter having a fixed data type.

    Parameters:
        dataType (TableDataType):
            (element) - A type of data contained in the column
        flag (str):
            (element) - A keyword representing traits of the column.

                Recognized values include “indexed”, “primary”, and “nullable”.
        std (bool):
            (attr) - If true, the meaning and use of this parameter is reserved and defined by a standard model.
            If false, it represents a parameter specific to the data described If not provided, then the value is
            unknown.
    """

    std: Optional[bool] = attr(default=None)

    data_type: Optional[TableDataType] = element(tag="dataType", default=None)
    flag: Optional[list[str]] = element(default_factory=list)


class InputParam(BaseParam, ns="vs", nsmap=NSMAP):
    """
    A description of a service or function parameter having a fixed data type.

    Parameters:
        dataType (DataType):
            (element) - A type of data contained in the parameter.
        use (ParamUse):
            (attr) - An indication of whether this parameter is required to be provided for the application or service
            to work properly.
        std (bool):
            (element) - If true, the meaning and use of this parameter is reserved and defined by a standard interface.
            If false, it represents an implementation-specific parameter that effectively extends the behavior of the
            service or application.
    """

    std: Optional[bool] = attr(default=None)
    use: Optional[ParamUse] = attr(default=None)

    data_type: Optional[DataType] = element(tag="dataType")


class StandardSTC(Resource, ns="vs", nsmap=NSMAP):
    """
    A description of standard space-time coordinate systems, positions, and regions.

    This resource type is deprecated, and no resource records
    of this type exist in the Registry.  It will be removed
    in version 1.3 of VODataService.

    Parameters:
        stcDefinitions (stcDescriptionType):
            (element) - An STC description of coordinate systems, positions, and/or regions.

                Each system, position, and region description should have a an XML ID assigned to it.
    """

    # TODO: STCDescriptionType is not implemented
    stc_definitions: list[STCDescriptionType] = element(tag="stcDefinitions")


class FKColumn(BaseXmlModel, ns="vs", nsmap=NSMAP):
    """
    A pair of columns that are used to join two tables.

    Parameters:
        fromColumn (str):
            (element) - The unqualified name of the column from the current table.
        toColumn (str):
            (element) - The unqualified name of the column from the target table.
    """

    from_column: str = element(tag="fromColumn")
    to_column: str = element(tag="toColumn")


class DataResource(Service, ns="vs", nsmap=NSMAP):
    """
    A resource publishing astronomical data.

    This resource type should only be used if the resource has no common underlying tabular schema
    (e.g., an inhomogeneous archive). Use CatalogResource otherwise.

    Parameters:
        facility (ResourceName):
            (element) - The observatory or facility used to collect the data contained or managed by this resource.
        instrument (ResourceName):
            (element) - The instrument used to collect the data contain or managed by a resource.
        coverage (Coverage):
            (element) - Extent of the content of the resource over space, time, and frequency.
    """

    facility: Optional[list[ResourceName]] = element(default=None)
    instrument: Optional[list[ResourceName]] = element(default=None)
    coverage: Optional[Coverage] = element(default=None)


class DataService(DataResource, ns="vs", nsmap=NSMAP):
    """
    A service for accessing astronomical data.

    This resource type should only be used if the service has no common underlying tabular schema
    (e.g., a storage service) or if it is not explicitly accessible (e.g., an ftp server with images).
    Use CatalogService otherwise.
    """


class ParamHTTP(Interface, ns="vs", nsmap=NSMAP):
    """
    A service invoked via an HTTP Query (either Get or Post) with a set of arguments consisting of keyword
    name-value pairs.

    Parameters:
        queryType (HTTPQueryType):
            (element) - The type of HTTP request, either GET or POST.
        resultType (str):
            (element) - The MIME media type of a document returned in the HTTP response.
        param (InputParam):
          (element) - A description of a input parameter that can be provided as a name=value argument to the service.
        testQuery (str):
            (element) - An ampersand-delimited list of arguments that can be used to test this service interface;
            when provided as the input to this interface, it will produce a legal, non-null response.
    """

    query_type: Optional[list[HTTPQueryType]] = element(tag="queryType", max_occurs=2, default_factory=list)
    result_type: Optional[str] = element(tag="resultType", default=None)
    param: Optional[list[InputParam]] = element(default_factory=list)
    test_query: Optional[str] = element(tag="testQuery", default=None)


class ForeignKey(BaseXmlModel, ns="vs", nsmap=NSMAP):
    """
    A description of the mapping a foreign key -- a set of columns from one table -- to columns in another table.

    When foreign keys are declared in this way, clients can expect that joins constrained with the foreign keys are
    preformed efficiently (e.g., using an index).

    Parameters:
        targetTable (str):
            (element) - The fully qualified name (including catalogue and schema, as applicable) of the table that
            can be joined with the table containing this foreign key.
        fkColumn (FKColumn):
            (element) - A pair of column names, one from this table and one from the target table that should be used to
            join the tables in a query.
        description (str):
            (element) - A free-text description of what this key points to and what the relationship means.
        utype (str):
            (element) - An identifier for a concept in a data model that the association enabled by this key represents.
    """

    target_table: str = element(tag="targetTable")
    fk_column: list[FKColumn] = element(tag="fkColumn")
    description: Optional[str] = element(default=None)
    utype: Optional[str] = element(default=None)


class Table(BaseXmlModel, ns="vs", nsmap=NSMAP):
    """
    A generic Table type.

    Parameters:
        name (str):
            (elements) - The fully qualified name of the table.  This name should include all catalogue or schema
            prefixes needed to sufficiently uniquely distinguish it in a query.
        title (str):
            (element) - A descriptive, human-interpretable name for the table. This is used for display purposes.
            There is no requirement regarding uniqueness.
        description (str):
            (element) - A free-text description of the table's contents.
        utype (str):
            (element) - An identifier for a concept in a data model that the data in this table represent.
        nrows (int):
            (element) - The approximate size of the table in rows.
        column (TableParam):
            (element) - A description of a table column.
        foreign_key (ForeignKey):
            (element) - A description of a foreign keys, one or more columns from the current table that can be used to
            join with another table.
        type (str):
            (attr) - A name for the role this table plays.

                Recognized values include “output”, indicating this table is output from a query;
                “base_table”, indicating a table whose records represent the main subjects of its schema;
                “view”, indicating that the table represents a useful combination or subset of other tables.
                Other values are allowed.
    """

    name: str = element()
    title: Optional[str] = element(default=None)
    description: Optional[str] = element(default=None)
    utype: Optional[str] = element(default=None)
    nrows: Optional[int] = element(default=None, gte=0)
    column: list[TableParam] = element()
    foreign_key: list[ForeignKey] = element(tag="foreignKey")

    type: Optional[str] = attr(name="type", default=None)


class TableSchema(BaseXmlModel, ns="vs", nsmap=NSMAP):
    """
    A detailed description of a logically related group of tables.

    Parameters:
        name (str):
            (element) - A name for the group of tables.

                This is used to uniquely identify the group of tables among several groups.
                If no title is given, this name can be used for display purposes. If there is no appropriate logical name
                associated with this group, the name should be explicitly set to “default”.
        title (str):
            (element) - A descriptive, human-interpretable name for the table.

                This is used for display purposes.  There is no requirement regarding uniqueness.
        description (str):
            (element) - A free text description of the group of tables that should explain in general how all of the tables
            in the group are related.
        utype (str):
            (element) - An identifier for a concept in a data model that the data in this schema as a whole represent.

                The form of the utype string depends on the data model; common forms are sequences of dotted identifiers
                (e.g., in SSA) or URIs (e.g., in RegTAP).
        table (list[Table]):
            (element) - A description of a table that is part of this schema.
    """

    name: str = element(default="default")
    title: Optional[str] = element()
    description: Optional[str] = element()
    utype: Optional[str] = element()
    table: list[Table] = element()


class TableSet(BaseXmlModel, ns="vs", nsmap=NSMAP):
    """
    The set of tables hosted by a resource.

    Parameters:
        schema (TableSchema):
            (element) - A named description of a group of logically related tables.

                The name given by the “name” child element must be unique within this TableSet instance.  If there is
                only one schema in this set and/or there is no locally appropriate name to provide, the name can be set
                to “default”.
    """

    schema: list[TableSchema] = element()


class DataCollection(Resource, ns="vs", nsmap=NSMAP):
    """
    A logical grouping of data which, in general, is composed of one or
    more accessible datasets. A collection can contain any combination
    of images, spectra, catalogues, or other data.

    (A dataset is a collection of digitally-encoded data that is normally accessible as a single unit, e.g., a file.)

    This type is deprecated.  Resource record authors should use vs:CatalogResource instead.  This type will be removed
    from the schema when no resource record using it remains in the registry.

    Parameters:
        facility (ResourceName):
            (element) - The observatory or facility used to collect the data contained or managed by this resource.
        instrument (ResourceName):
            (element) - The instrument used to collect the data contain or managed by a resource.
        rights (Rights):
            (element) - Information about rights held in and over the resource.
                This should be repeated for all Rights values that apply.
        format (Format):
            (element) - The physical or digital manifestation of the information supported by a resource.

                    This should use RFC 2046 media (“MIME”) types for network-retrievable, digital data.
                    Non-RFC 2046 values could be used for media that cannot be retrieved over the network.
        coverage (Coverage):
            (element) - Extent of the content of the resource over space, time, and frequency.
        tableset (TableSet):
            (element) - A description of the tables that are part of this collection.

                    Each schema name must be unique within a tableset.
        access_url (AccessURL):
            (element) - The URL that can be used to download the data contained in this data collection.
    """

    facility: Optional[list[ResourceName]] = element(default=None)
    instrument: Optional[list[ResourceName]] = element(default=None)
    rights: Optional[list[Rights]] = element(default=None)
    format: Optional[list[Format]] = element(default=None)
    coverage: Optional[Coverage] = element(default=None)
    tableset: Optional[TableSet] = element(default=None)
    access_url: Optional[AccessURL] = element(tag="accessURL", default=None)


class CatalogResource(DataResource):
    """
    A resource giving astronomical data in tabular form.

    While this includes classical astronomical catalogues,
    this resource is also appropriate for collections of observations
    or simulation results provided their metadata are available
    in a sufficiently structured form (e.g., Obscore, SSAP, etc).

    Parameters:
        tableset (TableSet):
            (element) - A description of the tables that are accessible through this service.

                Each schema name must be unique within a tableset.
    """

    tableset: Optional[TableSet] = element(default=None)


class CatalogService(CatalogResource):
    """
    A service that interacts with astronomical data through one or more specified tables.

    This is the appropriate resource type for normal VO services,
    e.g., TAP, SSAP, SIAP, ConeSearch.
    """
