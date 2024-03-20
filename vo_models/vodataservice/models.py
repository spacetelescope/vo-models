"""Pydantic-xml models for VODataService types

TODO: This is an incomplete spec, covering only elements needed for VOSITables
https://github.com/spacetelescope/vo-models/issues/17
"""
from typing import Any, Optional
from xml.sax.saxutils import escape

from pydantic import field_validator
from pydantic_xml import BaseXmlModel, attr, element

from vo_models.adql.misc import ADQL_SQL_KEYWORDS

# pylint: disable=no-self-argument

NSMAP = {
    "": "http://www.ivoa.net/xml/VODataService/v1.1",
    "xs": "http://www.w3.org/2001/XMLSchema",
    "vr": "http://www.ivoa.net/xml/VOResource/v1.0",
    "vs": "http://www.ivoa.net/xml/VODataService/v1.1",
    "stc": "http://www.ivoa.net/xml/STC/stc-v1.30.xsd",
    "vm": "http://www.ivoa.net/xml/VOMetadata/v0.1",
}


class FKColumn(BaseXmlModel, tag="fkColumn"):
    """A pair of columns that are used to join two tables.

    Parameters:
        from_column:
            (elem) - The unqualified name of the column from the current table.
        target_column:
            (elem) - The unqualified name of the column from the target table.

    """

    from_column: str = element(tag="fromColumn")
    target_column: str = element(tag="targetColumn")


class ForeignKey(BaseXmlModel, tag="foreignKey"):
    """A description of the mapping a foreign key -- a set of columns from one table -- to columns in another table.

    Parameters:
        target_table:
            (elem) - The fully qualified name (including catalogue and schema, as applicable) of the table that can
            be joined with the table containing this foreign key.
        fk_column:
            (elem) - A pair of column names, one from this table and one from the target table that should be used to
            join the tables in a query.
        description:
            (elem) - A free-text description of what this key points to and what the relationship means.
        utype:
            (elem) - An identifier for a concept in a data model that the association enabled by this key represents.
    """

    target_table: str = element(tag="targetTable")
    fk_column: list[FKColumn] = element(tag="fkColumn")
    description: Optional[str] = element(tag="description", default=None)
    utype: Optional[str] = element(tag="utype", default=None)

    def __init__(__pydantic_self__, **data: Any) -> None:
        # If what we were given is of the form:
        # {'target_table': 'target_table', 'from_column': 'from_column', 'target_column': 'target_column'}
        # and we don't have an fk_column, make one
        if not data.get("fk_column", None):
            if data.get("from_column") and data.get("target_column"):
                data["fk_column"] = [
                    FKColumn(
                        from_column=data["from_column"],
                        target_column=data["target_column"],
                    )
                ]
        super().__init__(**data)

    @field_validator("fk_column", mode="before")
    def validate_fk_column(cls, value):
        """If we have a single fk_column, make it a list"""
        if not isinstance(value, list):
            value = [value]
        return value


class DataType(BaseXmlModel, tag="dataType", nsmap={"xsi": "http://www.w3.org/2001/XMLSchema-instance"}):
    """A type of data contained in the column.

    Parameters:
        type:
            (attr) - A type of data contained in the parameter.
        arraysize:
            (attr) - The shape of the array that constitutes the value.
        value:
            (text) - The name of the data type (e.g. 'char', 'int', 'double').
    """

    type: Optional[str] = attr(name="type", ns="xsi", default="vs:VOTableType")
    arraysize: Optional[str] = attr(name="arraysize", default=None)
    value: str


class TableParam(BaseXmlModel, ns="", tag="column"):
    """A description of a table column.

    Parameters:
        column_name:
            (elem) - The name of the parameter or column.
        description:
            (elem) - A free-text description of a parameter's or column's contents.
        unit:
            (elem) - The unit associated with the values in the parameter or column.
        ucd:
            (elem) - The name of a unified content descriptor that describes the scientific content of the parameter.
        utype:
            (elem) - An identifier for a concept in a data model that the data in this schema represent.
        xtype:
            (elem) - The xtype of the column.
        datatype:
            (elem) - A type of data contained in the column
        flag:
            (elem) -A keyword representing traits of the column. Recognized values include
            “indexed”, “primary”, and “nullable”.
    """

    column_name: str = element(tag="name")
    description: Optional[str] = element(tag="description", default=None)
    unit: Optional[str] = element(tag="unit", default=None)
    ucd: Optional[str] = element(tag="ucd", default=None)
    utype: Optional[str] = element(tag="utype", default=None)
    xtype: Optional[str] = element(tag="xtype", default=None)
    datatype: Optional[DataType] = element(tag="dataType", default=None)
    flag: Optional[list[str]] = element(tag="flag", default=None)

    def __init__(__pydantic_self__, **data: Any) -> None:
        data["datatype"] = __pydantic_self__.__make_datatype_element(data)
        data["flag"] = __pydantic_self__.__make_flags(data)
        super().__init__(**data)

    # pylint: disable=unused-private-member
    def __make_datatype_element(self, col_data) -> DataType:
        """Helper to make datatype element from column data when first created.

        For TAP_SCHEMA.columns tables that record datatype, arraysize as separate columns
        """
        if col_data.get("datatype", None):
            if isinstance(col_data["datatype"], DataType):
                return col_data["datatype"]

            datatype_value = col_data.get("datatype", None)
            datatype_arraysize = col_data.get("arraysize", None)

            datatype_elem = DataType(
                arraysize=datatype_arraysize,
                value=datatype_value,
            )
            return datatype_elem
        # If no datatype provided, default to char(*)
        return DataType(value="char", arraysize="*")

    def __make_flags(self, col_data) -> list[str]:
        """Set up the flag elements when creating the column.

        In the case that column flags are boolean values, as may occur in TAP_SCHEMA.columns, parse them into
        a list of strings.
        """
        if not col_data.get("flag", None):
            flag = [flag for flag in ["principal", "indexed", "std"] if col_data.get(flag, None) == 1]
            return flag
        return col_data["flag"]

    @field_validator("column_name")
    def validate_colname(cls, value: str):
        """Escape the column name if it is an ADQL reserved word

        See: https://www.ivoa.net/documents/ADQL/20180112/PR-ADQL-2.1-20180112.html#tth_sEc2.1.3

        value: - The column name to escape.
        """
        if value.upper() in ADQL_SQL_KEYWORDS:
            value = f'"{value}"'
        return value

    @field_validator("description")
    def validate_description(cls, value: str):
        """Sanitize bad XML values in the description"""
        if value:
            value = escape(str(value))
        return value


class Table(BaseXmlModel, tag="table", ns="", skip_empty=True):
    """A model representing a single table element.

    Parameters:
        table_type:
            (attr) - A name for the role this table plays.

                Recognized values include “output”, indicating this table is output from a query;
                “base_table”, indicating a table whose records represent the main subjects of its schema;
                and “view”, indicating that the table represents a useful combination or subset of other tables.
                Other values are allowed.
        table_name:
            (elem) - The fully qualified name of the table.

                This name should include all catalogue or schema prefixes needed to sufficiently uniquely
                distinguish it in a query.
        title:
            (elem) - A descriptive, human-interpretable name for the table.
        description:
            (elem) - A free-text description of the table's contents
        utype:
            (elem) - An identifier for a concept in a data model that the data in this table represent.
        nrows:
            (elem) - The approximate size of the table in rows.
        column:
            (elem) - A description of a table column.
        foreign_key:
            (elem) - A description of a foreign keys, one or more columns from the current table that can be used to
            join with another table.
    """

    table_type: Optional[str] = attr(name="type", default=None)

    table_name: str = element(tag="name", ns="")
    title: Optional[str] = element(tag="title", ns="", default=None)
    description: Optional[str] = element(tag="description", ns="", default=None)
    utype: Optional[str] = element(tag="utype", ns="", default=None)
    nrows: Optional[int] = element(tag="nrows", gte=0, ns="", default=None)
    column: Optional[list[TableParam]] = element(tag="column", ns="", default=None)
    foreign_key: Optional[list[ForeignKey]] = element(tag="foreignKey", ns="", default=None)

    def __init__(__pydantic_self__, **data: Any) -> None:
        """Escape any keys that are passed in."""
        for key, val in data.items():
            if isinstance(val, str):
                data[key] = escape(val)
        super().__init__(**data)

    @field_validator("column", "foreign_key", mode="before")
    def validate_lists(cls, value):
        """If we have a single column or foreign_key, make it a list"""
        if value:
            if not isinstance(value, list):
                value = [value]
        return value


class TableSchema(BaseXmlModel, tag="schema", ns="", skip_empty=True):
    """A detailed description of a logically related group of tables.

    Parameters:
        schema_name:
            (elem) - A name for the group of tables.

                If no title is given, this name can be used for display purposes. If there is no appropriate logical
                name associated with this group, the name should be explicitly set to “default”.
        title:
            (elem) - A descriptive, human-interpretable name for the group of tables.
        description:
            (elem) - A free text description of the group of tables that should explain in general how all of the tables
            in the group are related.
        utype:
            (elem) - An identifier for a concept in a data model that the data in this schema as a whole represent.
        table:
            (elem) - A description of a table.

    """

    schema_name: str = element(tag="name", default="default")
    title: Optional[str] = element(tag="title", default=None)
    description: Optional[str] = element(tag="description", default=None)
    utype: Optional[str] = element(tag="utype", default=None)
    table: Optional[list[Table]] = element(tag="table", default=None)

    def __init__(__pydantic_self__, **data: Any) -> None:
        """Escape any keys that are passed in."""
        for key, val in data.items():
            if isinstance(val, str):
                data[key] = escape(val)
        super().__init__(**data)

    @field_validator("table", mode="before")
    def validate_table(cls, value):
        """If we have a single table, make it a list"""
        if not isinstance(value, list):
            value = [value]
        return value


class TableSet(BaseXmlModel, tag="tableset", skip_empty=True):
    """A description of the tables that are accessible through this service.

    Each schema name must be unique within a tableset.

    Parameters:
        tableset_schema:
            (elem) - A named description of a group of logically related tables.

                The name given by the “name” child element must be unique within this TableSet instance.
                If there is only one schema in this set and/or there is no locally appropriate name to provide,
                the name can be set to “default”.

    """

    tableset_schema: list[TableSchema] = element(tag="schema")

    @field_validator("tableset_schema", mode="before")
    def validate_tableset_schema(cls, value):
        """If we have a single tableset_schema, make it a list"""
        if not isinstance(value, list):
            value = [value]
        return value
