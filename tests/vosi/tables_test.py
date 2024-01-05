"""Tests for VOSI-Tables specific pydantic-xml models"""

# We're only parsing a locally controlled XSD file
from unittest import TestCase
from xml.etree.ElementTree import canonicalize

from lxml import etree  # nosec B410

from vo_models.vodataservice.models import DataType, Table, TableParam, TableSchema
from vo_models.vosi.tables import VOSITable, VOSITableSet

with open("tests/vosi/VOSITables-v1.1.xsd", "r") as schema_file:
    vosi_tables_schema = etree.XMLSchema(file=schema_file)

VOSIT_TABLES_HEADER = """xmlns:vosi='http://www.ivoa.net/xml/VOSITables/v1.0'
xmlns:vr='http://www.ivoa.net/xml/VOResource/v1.0'
xmlns:vs='http://www.ivoa.net/xml/VODataService/v1.1'
xmlns:xsd='http://www.w3.org/2001/XMLSchema'
xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
"""


class TestVOSITableElement(TestCase):
    """Test the VOSI Table element"""

    test_xml = (
        f"<vosi:table {VOSIT_TABLES_HEADER}"
        "type='table'>"
        "<name>tap_schema.schemas</name>"
        "<description>description of schemas in this dataset</description>"
        "<column>"
        "<name>schema_name</name>"
        "<description>Fully qualified schema name</description>"
        "<dataType xsi:type='vs:VOTableType' arraysize='*'>char</dataType>"
        "<flag>std</flag>"
        "</column>"
        "<column>"
        "<name>description</name>"
        "<description>Brief description of the schema</description>"
        "<dataType xsi:type='vs:VOTableType' arraysize='*'>char</dataType>"
        "<flag>std</flag>"
        "</column>"
        "</vosi:table>"
    )

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

    def test_read_from_xml(self):
        """Test reading a Table from XML"""
        vosi_table = VOSITable.from_xml(self.test_xml)
        self.assertEqual(vosi_table.table_name, "tap_schema.schemas")
        self.assertEqual(vosi_table.table_type, "table")
        self.assertEqual(vosi_table.description, "description of schemas in this dataset")
        self.assertEqual(len(vosi_table.column), 2)
        self.assertEqual(vosi_table.column[0].column_name, "schema_name")
        self.assertEqual(vosi_table.column[0].description, "Fully qualified schema name")
        self.assertEqual(vosi_table.column[0].datatype.type, "vs:VOTableType")
        self.assertEqual(vosi_table.column[0].datatype.arraysize, "*")
        self.assertEqual(vosi_table.column[0].datatype.value, "char")
        self.assertEqual(vosi_table.column[0].flag, ["std"])

    def test_write_to_xml(self):
        """Test writing a Table to XML"""

        tables_xml = self.test_element.to_xml()
        self.assertEqual(
            canonicalize(tables_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )

    def test_validate(self):
        """Test validating a Table against the VOSI Tables schema"""
        table_xml = etree.fromstring(self.test_element.to_xml(skip_empty=True, encoding=str))  # nosec B320
        vosi_tables_schema.assertValid(table_xml)


class TestVOSITableSet(TestCase):
    """Test the TableSet element model as specified in VOSI Tables"""

    test_xml = (
        f"<vosi:tableset {VOSIT_TABLES_HEADER}>"
        "<schema>"
        "<name>tap_schema</name>"
        "<description>schema information for TAP services</description>"
        "<table type='table'>"
        "<name>tap_schema.schemas</name>"
        "<description>description of schemas in this dataset</description>"
        "</table>"
        "<table type='table'>"
        "<name>tap_schema.tables</name>"
        "<description>description of tables in this dataset</description>"
        "</table>"
        "</schema>"
        "</vosi:tableset>"
    )

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

    def test_vositableset_ns(self):
        """Test that the TableSet is specifically namespaced to VOSI"""
        vosi_element = VOSITableSet.from_xml(self.test_xml)
        self.assertEqual(vosi_element.__xml_ns__, "vosi")

        vosi_xml = vosi_element.to_xml(skip_empty=True, encoding=str)
        self.assertIn("<vosi:tableset", vosi_xml)

    def test_read_from_xml(self):
        """Test reading a TableSet from XML"""
        tableset = VOSITableSet.from_xml(self.test_xml)
        self.assertEqual(len(tableset.tableset_schema), 1)
        self.assertEqual(tableset.tableset_schema[0].schema_name, "tap_schema")
        self.assertEqual(tableset.tableset_schema[0].description, "schema information for TAP services")
        self.assertEqual(len(tableset.tableset_schema[0].table), 2)
        self.assertEqual(tableset.tableset_schema[0].table[0].table_name, "tap_schema.schemas")
        self.assertEqual(
            tableset.tableset_schema[0].table[0].description,
            "description of schemas in this dataset",
        )
        self.assertEqual(tableset.tableset_schema[0].table[1].table_name, "tap_schema.tables")
        self.assertEqual(
            tableset.tableset_schema[0].table[1].description,
            "description of tables in this dataset",
        )

    def test_write_to_xml(self):
        """Test writing a TableSet to XML"""

        tableset_xml = self.test_element.to_xml()
        self.assertEqual(
            canonicalize(tableset_xml, strip_text=True),
            canonicalize(self.test_xml, strip_text=True),
        )

    def test_validate(self):
        """Test the tableset element validates against the schema"""
        tableset_xml = etree.fromstring(self.test_element.to_xml(skip_empty=True, encoding=str))
        vosi_tables_schema.assertValid(tableset_xml)
