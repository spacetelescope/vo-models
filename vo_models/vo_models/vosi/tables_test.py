"""Tests for VOSI-Tables specific pydantic-xml models"""

from defusedxml import ElementTree as ET
# We're only parsing a locally controlled XSD file
from lxml import etree  # nosec B410

from mast.vo_tap.services.vo_models.vo_models_test import VOModelTestBase
from mast.vo_tap.services.vo_models.vodataservice import DataType, Table, TableParam, TableSchema
from mast.vo_tap.services.vo_models.vosi import VOSITable, VOSITableSet

with open("mast/vo_tap/services/vo_models/vosi/VOSITables-v1.1.xsd", "r") as schema_file:
    vosi_tables_schema = etree.XMLSchema(file=schema_file)


class TestVOSITableElement(VOModelTestBase.VOModelTestCase):
    """Test the Table element model as specified in VOSI Tables"""

    test_xml = """
        <vosi:table xmlns:vosi='http://www.ivoa.net/xml/VOSITables/v1.0'
        xmlns:vr='http://www.ivoa.net/xml/VOResource/v1.0'
        xmlns:vs='http://www.ivoa.net/xml/VODataService/v1.1'
        xmlns:xsd='http://www.w3.org/2001/XMLSchema'
        xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
        type='table'>
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
        """
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
    base_model = VOSITable

    def test_vosi_table_ns(self):
        """Test that the Table is specifically namespaced to VOSI"""
        vosi_element = self.base_model.from_xml(self.test_xml)
        self.assertEqual(vosi_element.__xml_ns__, "vosi")

        vosi_xml = vosi_element.to_xml(skip_empty=True, encoding=str)
        self.assertIn("<vosi:table", vosi_xml)

    def test_validate(self):
        """Test that the Table element validates against the schema"""
        tables_xml = etree.fromstring(self.test_element.to_xml(skip_empty=True, encoding=str))
        vosi_tables_schema.assertValid(tables_xml)


class TestVOSITableSet(VOModelTestBase.VOModelTestCase):
    """Test the TableSet element model as specified in VOSI Tables"""

    test_xml = (
        "<vosi:tableset "
        "xmlns:vosi='http://www.ivoa.net/xml/VOSITables/v1.0' "
        "xmlns:vr='http://www.ivoa.net/xml/VOResource/v1.0' "
        "xmlns:vs='http://www.ivoa.net/xml/VODataService/v1.1' "
        "xmlns:xsd='http://www.w3.org/2001/XMLSchema' "
        "xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>"
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

    base_model = VOSITableSet

    def test_vositableset_ns(self):
        """Test that the TableSet is specifically namespaced to VOSI"""
        vosi_element = self.base_model.from_xml(self.test_xml)
        self.assertEqual(vosi_element.__xml_ns__, "vosi")

        vosi_xml = vosi_element.to_xml(skip_empty=True, encoding=str)
        self.assertIn("<vosi:tableset", vosi_xml)

    def test_validate(self):
        """Test that the TableSet element validates against the schema"""
        tableset_xml = etree.fromstring(self.test_element.to_xml(skip_empty=True, encoding=str))
        vosi_tables_schema.assertValid(tableset_xml)
