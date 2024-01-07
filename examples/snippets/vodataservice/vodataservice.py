from vo_models.vodataservice.models import (
    DataType,
    FKColumn,
    ForeignKey,
    Table,
    TableParam,
    TableSchema,
    TableSet,
)

# [FKColumn-model-start]
fk_column = FKColumn(
    from_column="from_column",
    target_column="target_column",
)
# [FKColumn-model-end]

# [FKColumn-xml-start]
fk_column_xml = """
<fkColumn>
    <fromColumn>from_column</fromColumn>
    <targetColumn>target_column</targetColumn>
</fkColumn>
"""  # [FKColumn-xml-end]

# [ForeignKey-model-start]
foreign_key = ForeignKey(
    target_table="target_table",
    fk_column=fk_column,
    description="description",
    utype="utype",
)
# [ForeignKey-model-end]

# [ForeignKey-xml-start]
foreign_key_xml = """
<foreignKey>
    <targetTable>target_table</targetTable>
    <fkColumn>
        <fromColumn>from_column</fromColumn>
        <targetColumn>target_column</targetColumn>
    </fkColumn>
    <description>description</description>
    <utype>utype</utype>
</foreignKey>
"""  # [ForeignKey-xml-end]

# [DataType-model-start]
data_type = DataType(
    type="string",
    arraysize="32*",
    value="value",
)
# [DataType-model-end]

# [DataType-xml-start]
data_type_xml = """
<dataType
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:type="string" arraysize="32*">value</dataType>
"""
# [DataType-xml-end]

# [TableParam-model-start]
table_param = TableParam(
    column_name="example_column",
    description="Example column description",
    datatype=data_type,
    flag=["std", "indexed"],
)
# [TableParam-model-end]

# [TableParam-xml-start]
table_param_xml = """
<column>
    <name>example_column</name>
    <description>Example column description</description>
    <unit></unit>
    <ucd></ucd>
    <utype></utype>
    <xtype></xtype>
    <dataType
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:type="string"
        arraysize="32*">
        value
    </dataType>
    <flag>std</flag>
    <flag>indexed</flag>
</column>
"""  # [TableParam-xml-end]

# [Table-model-start]
table = Table(
    table_type="table",
    table_name="example_table",
    description="Example table description",
    column=table_param,
    foreign_key=foreign_key,
)
# [Table-model-end]

# [Table-xml-start]
table_xml = """
<table type="table">
    <name>example_table</name>
    <description>Example table description</description>
    <column>
        <name>example_column</name>
        <description>Example column description</description>
        <dataType
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:type="string" arraysize="32*">
                value
        </dataType>
        <flag>std</flag>
        <flag>indexed</flag>
    </column>
    <foreignKey>
        <targetTable>target_table</targetTable>
        <fkColumn>
            <fromColumn>from_column</fromColumn>
            <targetColumn>target_column</targetColumn>
        </fkColumn>
        <description>description</description>
        <utype>utype</utype>
    </foreignKey>
</table>
"""  # [Table-xml-end]

# [TableSchema-model-start]
table_schema = TableSchema(
    name="example_schema",
    title="Example schema title",
    description="Example schema description",
    table=table,
)
# [TableSchema-model-end]

# [TableSchema-xml-start]
table_schema_xml = """
<schema>
    <name>default</name>
    <title>Example schema title</title>
    <description>Example schema description</description>
    <table type="table">
        <name>example_table</name>
        <description>Example table description</description>
        <column>
            <name>example_column</name>
            <description>Example column description</description>
            <dataType
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:type="string"
                arraysize="32*"
            >value</dataType>
            <flag>std</flag>
            <flag>indexed</flag>
        </column>
        <foreignKey>
            <targetTable>target_table</targetTable>
            <fkColumn>
                <fromColumn>from_column</fromColumn>
                <targetColumn>target_column</targetColumn>
            </fkColumn>
            <description>description</description>
            <utype>utype</utype>
        </foreignKey>
    </table>
</schema>
"""  # [TableSchema-xml-end]

# [TableSet-model-start]
table_set = TableSet(
    tableset_schema=table_schema,
)
# [TableSet-model-end]

# [TableSet-xml-start]
table_set_xml = """
<tableset>
    <schema>
        <name>default</name>
        <title>Example schema title</title>
        <description>Example schema description</description>
        <table type="table">
            <name>example_table</name>
            <description>Example table description</description>
            <column>
                <name>example_column</name>
                <description>Example column description</description>
                <dataType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="string"
                    arraysize="32*">value</dataType>
                <flag>std</flag>
                <flag>indexed</flag>
            </column>
            <foreignKey>
                <targetTable>target_table</targetTable>
                <fkColumn>
                    <fromColumn>from_column</fromColumn>
                    <targetColumn>target_column</targetColumn>
                </fkColumn>
                <description>description</description>
                <utype>utype</utype>
            </foreignKey>
        </table>
    </schema>
</tableset>
"""  # [TableSet-xml-end]
