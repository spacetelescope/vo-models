from datetime import datetime, timezone

from vo_models.stc.models import STCDescriptionType, STCResourceProfile
from vo_models.vodataservice.models import (
    BaseParam,
    CatalogResource,
    CatalogService,
    Coverage,
    DataCollection,
    DataResource,
    DataService,
    DataType,
    FKColumn,
    ForeignKey,
    Format,
    InputParam,
    ParamHTTP,
    ServiceReference,
    SimpleDataType,
    SpatialCoverage,
    StandardSTC,
    Table,
    TableDataType,
    TableParam,
    TableSchema,
    TableSet,
    TAPDataType,
    TAPType,
    VOTableType,
)


# [spatial-coverage-model-start]
spatial_coverage = SpatialCoverage(
    value="1/1 2 4 2/12-14 21 23 25 8/",
)
spatial_coverage.to_xml()
# [spatial-coverage-model-end]

# [spatial-coverage-xml-start]
spatial_coverage_xml = """
<vs:SpatialCoverage frame="">
    1/1 2 4 2/12-14 21 23 25 8/
</vs:SpatialCoverage>
"""  # [spatial-coverage-xml-end]

# [service-reference-model-start]
service_reference = ServiceReference(
    value="http://archive.stsci.edu/vo/mast_services.html", ivo_id="ivo://archive.stsci.edu/catalogs/2mass"
)
service_reference.to_xml()
# [service-reference-model-end]

# [service-reference-xml-start]
service_reference_xml = """

"""  # [service-reference-xml-end]

# [format-model-start]
format = Format(
    value="application/x-votable+xml",
)
format.to_xml()
# [format-model-end]

# [format-xml-start]
format_xml = """

"""  # [format-xml-end]

# [data-type-model-start]
data_type = DataType(
    value="string",
    arraysize="32*",
    delim=" ",
    extended_type="char",
    extended_schema="None",
)
data_type.to_xml()
# [data-type-model-end]

# [data-type-xml-start]
data_type_xml = """

"""  # [data-type-xml-end]

# [simple-data-type-model-start]
simple_data_type = SimpleDataType(
    value="integer",
    arraysize="32",
    delim="",
    extended_type="int",
    extended_schema="None",
)
simple_data_type.to_xml()
# [simple-data-type-model-end]

# [simple-data-type-xml-start]
simple_data_type_xml = """

"""  # [simple-data-type-xml-end]

# [votabletype-model-start]
votable_type = VOTableType(
    value="int",
    arraysize="32",
    delim="",
    extended_type="int",
    extended_schema="None",
)
votable_type.to_xml()
# [votabletype-model-end]

# [votabletype-xml-start]
votable_type_xml = """

"""  # [votabletype-xml-end]

# [tapdatatype-model-start]
tap_data_type = TAPDataType(
    value="int",
    arraysize="32*",
    size="32",
    delim="",
    extended_type="int",
    extended_schema="None",
)
tap_data_type.to_xml()
# [tapdatatype-model-end]

# [tapdatatype-xml-start]
tap_data_type_xml = """

"""  # [tapdatatype-xml-end]

# [taptype-model-start]
tap_type = TAPType(
    value="INTEGER",
    arraysize="32*",
    size="32",
    delim="",
    extended_type="int",
    extended_schema="None",
)
tap_type.to_xml()
# [taptype-model-end]

# [taptype-xml-start]
tap_type_xml = """

"""  # [taptype-xml-end]

# [coverage-model-start]
coverage = Coverage(
    spatial=spatial_coverage,
    temporal="2959.5 2960.5",
    waveband="Optical",
    region_of_regard=15.0,
)
coverage.to_xml()
# [coverage-model-end]

# [coverage-xml-start]
coverage_xml = """

"""  # [coverage-xml-end]

# [baseparam-model-start]
base_param = BaseParam(
    name="ID",
    description="Unique identifier",
    unit="",
    ucd="meta.id;meta.main",
    utype="",
)
# [baseparam-model-end]

# [baseparam-xml-start]
base_param_xml = """

"""  # [baseparam-xml-end]

# [tableparam-model-start]
table_param = TableParam(
    name="ID",
    description="Unique identifier",
    unit="",
    ucd="meta.id;meta.main",
    utype="",
    std=True,
    data_type=TableDataType(
        value="string",
        arraysize="32*",
        delim=" ",
        extended_type="char",
        extended_schema="None",
    ),
    flag=["std"],
)
table_param.to_xml()
# [tableparam-model-end]

# [tableparam-xml-start]
table_param_xml = """

"""  # [tableparam-xml-end]

# [inputparam-model-start]
input_param = InputParam(
    std=True,
    use="required",
    data_type=data_type,
)
# [inputparam-model-end]

# [inputparam-xml-start]
input_param_xml = """

"""  # [inputparam-xml-end]

# TODO: Add StandardSTC model when STC models are implemented

# [fkcolumn-model-start]
fk_column = FKColumn(
    from_column="schema_name",
    to_column="schema_name",
)
# [fkcolumn-model-end]

# [fkcolumn-xml-start]
fk_column_xml = """

"""  # [fkcolumn-xml-end]

# [paramhttp-model-start]
param_http = ParamHTTP(
    query_type="GET",
    result_type="text/xml",
    param=input_param,
    test_query="SELECT TOP 10 * FROM TAP_SCHEMA.tables",
)
# [paramhttp-model-end]

# [paramhttp-xml-start]
param_http_xml = """

"""  # [paramhttp-xml-end]

# [foreignkey-model-start]
foreign_key = ForeignKey(
    target_table="TAP_SCHEMA.schemas",
    fk_column=fk_column,
    description="",
    utype="string",
)
# [foreignkey-model-end]

# [foreignkey-xml-start]
foreign_key_xml = """

"""  # [foreignkey-xml-end]

# [table-model-start]
table = Table(
    name="TAP_SCHEMA.schemas",
    title="TAP schemas",
    description="Table listing schemas in the TAP service",
    utype="",
    nrows=5,
    column=TableParam(
        name="schema_name",
        description="Name of the schema",
        unit="",
        ucd="meta.id;meta.main",
        utype="",
        std=True,
        data_type=TableDataType(
            value="string",
            arraysize="32*",
            delim=" ",
            extended_type="char",
            extended_schema="None",
        ),
        flag=["std"],
    ),
    foreign_key=foreign_key,
    type="string",
)
# [table-model-end]
