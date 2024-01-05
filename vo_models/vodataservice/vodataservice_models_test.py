"""Tests for VODataService models"""

from mast.vo_tap.services.tap_service_models.vo_models_test import VOModelTestBase
from mast.vo_tap.services.tap_service_models.vodataservice import (
    DataType,
    FKColumn,
    ForeignKey,
    Table,
    TableParam,
    TableSchema,
    TableSet,
)


class TestFKColumn(VOModelTestBase.VOModelTestCase):
    """Test the FKColumn element model"""

    test_xml = "<fkColumn><fromColumn>from_column</fromColumn><targetColumn>target_column</targetColumn></fkColumn>"
    test_element = FKColumn(from_column="from_column", target_column="target_column")
    base_model = FKColumn


class TestForeignKey(VOModelTestBase.VOModelTestCase):
    """Test the ForeignKey element model"""

    test_xml = (
        "<foreignKey>"
        "<targetTable>target_table</targetTable>"
        "<fkColumn>"
        "<fromColumn>from_column</fromColumn>"
        "<targetColumn>target_column</targetColumn>"
        "</fkColumn>"
        "</foreignKey>"
    )
    test_element = ForeignKey(
        target_table="target_table",
        fk_column=[
            FKColumn(
                from_column="from_column",
                target_column="target_column",
            )
        ],
    )
    base_model = ForeignKey

    def test_single_dict_read(self):
        """Test that we can read a single dict as a ForeignKey

        This can occur for TAP_SCHEMA.keys / TAP_SCHEMA.key_columns db calls, where we don't have a list of
        fk_columns, but instead a single dict of the form:
        """

        single_dict = {
            "target_table": "target_table",
            "from_column": "from_column",
            "target_column": "target_column",
        }

        # pylint: disable=unsubscriptable-object
        foreign_key_element = ForeignKey(**single_dict)
        self.assertIsInstance(foreign_key_element, ForeignKey)
        self.assertIsInstance(foreign_key_element.fk_column, list)
        self.assertEqual(len(foreign_key_element.fk_column), 1)
        self.assertEqual(foreign_key_element.target_table, "target_table")
        self.assertEqual(foreign_key_element.fk_column[0].from_column, "from_column")
        self.assertEqual(foreign_key_element.fk_column[0].target_column, "target_column")


class TestDataType(VOModelTestBase.VOModelTestCase):
    """Test the DataType element model"""

    test_xml = (
        "<dataType xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' "
        "xsi:type='vs:VOTableType' arraysize='*'>string</dataType>"
    )
    test_element = DataType(type="vs:VOTableType", arraysize="*", value="string")
    base_model = DataType


class TestTableParam(VOModelTestBase.VOModelTestCase):
    """Test the TableParam element model"""

    test_xml = (
        "<column>"
        "<name>name</name>"
        "<description>description</description>"
        "<unit>unit</unit>"
        "<ucd>ucd</ucd>"
        "<utype>caom2:Artifact.productType</utype>"
        "<dataType xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' "
        "xsi:type='vs:VOTableType' arraysize='*'>string</dataType>"
        "<flag>flag</flag>"
        "</column>"
    )
    test_element = TableParam(
        column_name="name",
        description="description",
        unit="unit",
        ucd="ucd",
        utype="caom2:Artifact.productType",
        datatype=DataType(type="vs:VOTableType", arraysize="*", value="string"),
        flag=["flag"],
    )
    base_model = TableParam


class TestTableElement(VOModelTestBase.VOModelTestCase):
    """Test the Table element model"""

    test_xml = (
        "<table "
        "type='table'>"
        "<name>tap_schema.schemas</name>"
        "<description>description of schemas in this dataset</description>"
        "<column>"
        "<name>schema_name</name>"
        "<description>Fully qualified schema name</description>"
        "<dataType xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' "
        "xsi:type='vs:VOTableType' arraysize='*'>char</dataType>"
        "<flag>std</flag>"
        "</column>"
        "</table>"
    )
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
    base_model = Table


class TestSchemaElement(VOModelTestBase.VOModelTestCase):
    """Test the TableSchema element model"""

    test_xml = (
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
    )
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
    base_model = TableSchema


class TestTableSetElement(VOModelTestBase.VOModelTestCase):
    """Test the TableSet element model"""

    test_xml = (
        "<tableset>"
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
        "<schema>"
        "<name>dbo</name>"
        "<description>ArchiveCatalog Infrastructure, version 1.0</description>"
        "<table type='table'>"
        "<name>dbo.detailedCatalog</name>"
        "</table>"
        "<table type='table'>"
        "<name>dbo.SumMagAper2Cat</name>"
        "</table>"
        "</schema>"
        "</tableset>"
    )

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
    base_model = TableSet
