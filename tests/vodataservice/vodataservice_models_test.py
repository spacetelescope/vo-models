"""Tests for VODataService models

# TODO: This is an incomplete spec, covering only elements needed for VOSITables
"""

from unittest import TestCase
from xml.etree.ElementTree import canonicalize

from vo_models.vodataservice import (
    DataType,
    FKColumn,
    ForeignKey,
    Table,
    TableParam,
    TableSchema,
    TableSet,
)


class TestFKColumn(TestCase):
    """Test the FKColumn element model"""

    test_xml = """
    <fkColumn>
        <fromColumn>from_column</fromColumn>
        <targetColumn>target_column</targetColumn>
    </fkColumn>
    """

    test_element = FKColumn(
        from_column="from_column",
        target_column="target_column",
    )

    def test_read_from_xml(self):
        """Test reading FKColumn from XML."""
        fk_column = FKColumn.from_xml(self.test_xml)
        self.assertEqual(fk_column.from_column, "from_column")
        self.assertEqual(fk_column.target_column, "target_column")

    def test_write_to_xml(self):
        """Test writing FKColumn to XML."""
        fk_column_xml = self.test_element.to_xml(skip_empty=True)
        self.assertEqual(
            canonicalize(fk_column_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestForeignKey(TestCase):
    """Test the ForeignKey element model"""

    test_xml = """
        <foreignKey>
            <targetTable>target_table</targetTable>
            <fkColumn>
                <fromColumn>from_column</fromColumn>
                <targetColumn>target_column</targetColumn>
            </fkColumn>
        </foreignKey>
    """

    test_element = ForeignKey(
        target_table="target_table",
        fk_column=[
            FKColumn(
                from_column="from_column",
                target_column="target_column",
            )
        ],
    )

    def test_read_from_xml(self):
        """Test reading ForeignKey from XML."""
        foreign_key = ForeignKey.from_xml(self.test_xml)
        self.assertEqual(foreign_key.target_table, "target_table")
        self.assertEqual(len(foreign_key.fk_column), 1)
        self.assertEqual(foreign_key.fk_column[0].from_column, "from_column")
        self.assertEqual(foreign_key.fk_column[0].target_column, "target_column")

    def test_write_to_xml(self):
        """Test writing ForeignKey to XML."""
        foreign_key_xml = self.test_element.to_xml(skip_empty=True)
        self.assertEqual(
            canonicalize(foreign_key_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestDataType(TestCase):
    """Test the DataType element model"""

    test_xml = """
        <dataType xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
        xsi:type='vs:VOTableType' arraysize='*'>string</dataType>
    """

    test_element = DataType(
        type="vs:VOTableType",
        arraysize="*",
        value="string",
    )

    def test_read_from_xml(self):
        """Test reading DataType from XML."""
        data_type = DataType.from_xml(self.test_xml)
        self.assertEqual(data_type.type, "vs:VOTableType")
        self.assertEqual(data_type.arraysize, "*")
        self.assertEqual(data_type.value, "string")

    def test_write_to_xml(self):
        """Test writing DataType to XML."""
        data_type_xml = self.test_element.to_xml(skip_empty=True)
        self.assertEqual(
            canonicalize(data_type_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestTableParam(TestCase):
    """Test the TableParam element model"""

    test_xml = """
        <column>
            <name>name</name>
            <description>description</description>
            <unit>unit</unit>
            <ucd>ucd</ucd>
            <utype>caom2:Artifact.productType</utype>
            <dataType xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
            xsi:type='vs:VOTableType' arraysize='*'>string</dataType>
            <flag>flag</flag>
        </column>"""

    test_element = TableParam(
        column_name="name",
        description="description",
        unit="unit",
        ucd="ucd",
        utype="caom2:Artifact.productType",
        datatype=DataType(type="vs:VOTableType", arraysize="*", value="string"),
        flag=["flag"],
    )

    def test_read_from_xml(self):
        """Test reading TableParam from XML."""
        table_param = TableParam.from_xml(self.test_xml)
        self.assertEqual(table_param.column_name, "name")
        self.assertEqual(table_param.description, "description")
        self.assertEqual(table_param.unit, "unit")
        self.assertEqual(table_param.ucd, "ucd")
        self.assertEqual(table_param.utype, "caom2:Artifact.productType")
        self.assertEqual(table_param.datatype.type, "vs:VOTableType")
        self.assertEqual(table_param.datatype.arraysize, "*")
        self.assertEqual(table_param.datatype.value, "string")
        self.assertEqual(table_param.flag, ["flag"])

    def test_write_to_xml(self):
        """Test writing TableParam to XML."""
        table_param_xml = self.test_element.to_xml(skip_empty=True)
        self.assertEqual(
            canonicalize(table_param_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestTableElement(TestCase):
    """Test the Table element model"""

    test_xml = """
        <table
        type='table'>
            <name>tap_schema.schemas</name>
            <description>description of schemas in this dataset</description>
            <column>
                <name>schema_name</name>
                <description>Fully qualified schema name</description>
                <dataType xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
                xsi:type='vs:VOTableType' arraysize='*'>char</dataType>
                <flag>std</flag>
            </column>
        </table>
    """

    test_element = Table(
        table_name="tap_schema.schemas",
        table_type="table",
        description="description of schemas in this dataset",
        column=[
            TableParam(
                column_name="schema_name",
                description="Fully qualified schema name",
                datatype=DataType(type="vs:VOTableType", arraysize="*", value="char"),
                flag=["std"],
            )
        ],
    )

    def test_read_from_xml(self):
        """Test reading Table from XML."""
        table = Table.from_xml(self.test_xml)
        self.assertEqual(table.table_name, "tap_schema.schemas")
        self.assertEqual(table.table_type, "table")
        self.assertEqual(table.description, "description of schemas in this dataset")
        self.assertEqual(len(table.column), 1)
        self.assertEqual(table.column[0].column_name, "schema_name")
        self.assertEqual(table.column[0].description, "Fully qualified schema name")
        self.assertEqual(table.column[0].datatype.type, "vs:VOTableType")
        self.assertEqual(table.column[0].datatype.arraysize, "*")
        self.assertEqual(table.column[0].datatype.value, "char")
        self.assertEqual(table.column[0].flag, ["std"])

    def test_write_to_xml(self):
        """Test writing Table to XML."""
        table_xml = self.test_element.to_xml(skip_empty=True)
        self.assertEqual(
            canonicalize(table_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestSchemaElement(TestCase):
    """Test the TableSchema element model"""

    test_xml = """
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
        """

    test_element = TableSchema(
        schema_name="tap_schema",
        description="schema information for TAP services",
        table=[
            Table(
                table_name="tap_schema.schemas",
                table_type="table",
                description="description of schemas in this dataset",
            ),
            Table(
                table_name="tap_schema.tables",
                table_type="table",
                description="description of tables in this dataset",
            ),
        ],
    )

    def test_read_from_xml(self):
        """Test reading TableSchema from XML."""
        table_schema = TableSchema.from_xml(self.test_xml)
        self.assertEqual(table_schema.schema_name, "tap_schema")
        self.assertEqual(table_schema.description, "schema information for TAP services")
        self.assertEqual(len(table_schema.table), 2)
        self.assertEqual(table_schema.table[0].table_name, "tap_schema.schemas")
        self.assertEqual(table_schema.table[0].table_type, "table")
        self.assertEqual(table_schema.table[0].description, "description of schemas in this dataset")
        self.assertEqual(table_schema.table[1].table_name, "tap_schema.tables")
        self.assertEqual(table_schema.table[1].table_type, "table")
        self.assertEqual(table_schema.table[1].description, "description of tables in this dataset")

    def test_write_to_xml(self):
        """Test writing TableSchema to XML."""
        table_schema_xml = self.test_element.to_xml(skip_empty=True)
        self.assertEqual(
            canonicalize(table_schema_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )


class TestTableSetElement(TestCase):
    """Test the TableSet element model"""

    test_xml = """
        <tableset>
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
            <schema>
                <name>dbo</name>
                <description>ArchiveCatalog Infrastructure, version 1.0</description>
                <table type='table'>
                    <name>dbo.detailedCatalog</name>
                </table>
                <table type='table'>
                    <name>dbo.SumMagAper2Cat</name>
                </table>
            </schema>
        </tableset>"""

    test_element = TableSet(
        tableset_schema=[
            TableSchema(
                schema_name="tap_schema",
                description="schema information for TAP services",
                table=[
                    Table(
                        table_name="tap_schema.schemas",
                        table_type="table",
                        description="description of schemas in this dataset",
                    ),
                    Table(
                        table_name="tap_schema.tables",
                        table_type="table",
                        description="description of tables in this dataset",
                    ),
                ],
            ),
            TableSchema(
                schema_name="dbo",
                description="ArchiveCatalog Infrastructure, version 1.0",
                table=[
                    Table(
                        table_name="dbo.detailedCatalog",
                        table_type="table",
                    ),
                    Table(
                        table_name="dbo.SumMagAper2Cat",
                        table_type="table",
                    ),
                ],
            ),
        ],
    )

    def test_read_from_xml(self):
        """Test reading TableSet from XML."""
        tableset = TableSet.from_xml(self.test_xml)
        self.assertEqual(len(tableset.tableset_schema), 2)
        self.assertEqual(tableset.tableset_schema[0].schema_name, "tap_schema")
        self.assertEqual(tableset.tableset_schema[0].description, "schema information for TAP services")
        self.assertEqual(len(tableset.tableset_schema[0].table), 2)
        self.assertEqual(tableset.tableset_schema[0].table[0].table_name, "tap_schema.schemas")
        self.assertEqual(tableset.tableset_schema[0].table[0].table_type, "table")
        self.assertEqual(tableset.tableset_schema[0].table[0].description, "description of schemas in this dataset")
        self.assertEqual(tableset.tableset_schema[0].table[1].table_name, "tap_schema.tables")
        self.assertEqual(tableset.tableset_schema[0].table[1].table_type, "table")
        self.assertEqual(tableset.tableset_schema[0].table[1].description, "description of tables in this dataset")
        self.assertEqual(tableset.tableset_schema[1].schema_name, "dbo")
        self.assertEqual(tableset.tableset_schema[1].description, "ArchiveCatalog Infrastructure, version 1.0")
        self.assertEqual(len(tableset.tableset_schema[1].table), 2)
        self.assertEqual(tableset.tableset_schema[1].table[0].table_name, "dbo.detailedCatalog")
        self.assertEqual(tableset.tableset_schema[1].table[0].table_type, "table")
        self.assertEqual(tableset.tableset_schema[1].table[1].table_name, "dbo.SumMagAper2Cat")
        self.assertEqual(tableset.tableset_schema[1].table[1].table_type, "table")

    def test_write_to_xml(self):
        """Test writing TableSet to XML."""
        tableset_xml = self.test_element.to_xml(skip_empty=True)
        self.assertEqual(
            canonicalize(tableset_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )
