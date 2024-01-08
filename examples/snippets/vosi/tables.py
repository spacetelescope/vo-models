from vo_models.vodataservice import DataType, Table, TableParam, TableSchema
from vo_models.vosi.tables import VOSITable, VOSITableSet

# [table-model-start]
test_element = VOSITable(
    table_type="table",
    table_name="tap_schema.schemas",
    title=None,
    description="description of schemas in this dataset",
    utype=None,
    nrows=None,
    column=[
        TableParam(
            column_name="schema_name",
            description="Fully qualified schema name",
            unit=None,
            ucd=None,
            datatype=DataType(type_attr="vs:VOTableType", arraysize="*", value="char"),
            flag=["std"],
        ),
        TableParam(
            column_name="description",
            description="Brief description of the schema",
            unit=None,
            ucd=None,
            datatype=DataType(type_attr="vs:VOTableType", arraysize="*", value="char"),
            flag=["std"],
        ),
    ],
    foreign_key=None,
)
# [table-model-end]

# [table-xml-start]
table_xml = """
<vosi:table type='table'>
    <name>tap_schema.schemas</name>
    <description>description of schemas in this dataset</description>
    <column>
        <name>schema_name</name>
        <description>Fully qualified schema name</description>
        <dataType xsi:type='vs:VOTableType' arraysize='*'>char</dataType>
        <flag>std</flag>
    </column>
    <column>
        <name>description</name>
        <description>Brief description of the schema</description>
        <dataType xsi:type='vs:VOTableType' arraysize='*'>char</dataType>
        <flag>std</flag>
    </column>
</vosi:table>
"""  # [table-xml-end]

# [tableset-model-start]
test_element = VOSITableSet(
    tableset_schema=[
        TableSchema(
            schema_name="tap_schema",
            title=None,
            description="schema information for TAP services",
            table=[
                Table(
                    table_type="table",
                    table_name="tap_schema.schemas",
                    title=None,
                    description="description of schemas in this dataset",
                    utype=None,
                    nrows=None,
                    column=None,
                    foreign_key=None,
                ),
                Table(
                    table_type="table",
                    table_name="tap_schema.tables",
                    title=None,
                    description="description of tables in this dataset",
                    utype=None,
                    nrows=None,
                    column=None,
                    foreign_key=None,
                ),
            ],
        ),
    ]
)
# [tableset-model-end]

# [tableset-xml-start]
tableset_xml = """
<vosi:tableset>
    <schema>
    <name>tap_schema</name>
    <description>schema information for TAP services</description>
    <table type='table'>
        <name>tap_schema.schemas</name>
        <description>description of schemas in this dataset</description>
    </table>
    <table type='table'>
        <name>tap_schema.tables</name>
        <description>description of tables in this dataset</description>
    </table>
    </schema>
</vosi:tableset>
"""  # [tableset-xml-end]
