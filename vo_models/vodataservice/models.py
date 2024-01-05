"""Pydantic-xml models for VODataService types"""
from typing import Any, Optional
# skip the bandit check here since we use escape() here only on XML we generated
from xml.sax.saxutils import escape  # nosec B406

from asb.core.encoding import ADQL_SQL_KEYWORDS, handle_votable_arraysize
from pydantic import field_validator
from pydantic_xml import BaseXmlModel, RootXmlModel, attr, element

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
    """An individual foreign key column."""

    from_column: str = element(tag="fromColumn")
    target_column: str = element(tag="targetColumn")


class ForeignKey(BaseXmlModel, tag="foreignKey"):
    """An element containing one or more foreign key columns."""

    target_table: str = element(tag="targetTable")
    fk_column: list[FKColumn] = element(tag="fkColumn")
    description: Optional[str] = element(tag="description", default=None)
    utype: Optional[str] = element(tag="utype", default=None)

    def __init__(__pydantic_self__, **data: Any) -> None:
        # If what we were given is of the form:
        # {'target_table': 'target_table', 'from_column': 'from_column', 'target_column': 'target_column'}
        # and we don't have an fk_column, make one
        # this is a convenience for database calls to TAP_SCHEMA.keys / TAP_SCHEMA.key_columns
        if not data.get("fk_column", None):
            if data.get("from_column") and data.get("target_column"):
                data["fk_column"] = [
                    FKColumn(
                        from_column=data["from_column"],
                        target_column=data["target_column"],
                    )
                ]
        super().__init__(**data)


class DataType(BaseXmlModel, tag="dataType", nsmap={"xsi": "http://www.w3.org/2001/XMLSchema-instance"}):
    """A simple element containing a column datatype"""

    type: Optional[str] = attr(name="type", ns="xsi", default="vs:VOTableType")
    arraysize: Optional[str] = attr(name="arraysize", default=None)
    value: str


class TableParam(BaseXmlModel, ns="", tag="column"):
    """A column element as returned from TAP_SCHEMA.columns.

    'TableParam' is the IVOA standard name for this element, but it's basically a column.
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
        """Helper to make datatype element from column data when first created"""
        if col_data.get("datatype", None):
            if isinstance(col_data["datatype"], DataType):
                return col_data["datatype"]
            col = handle_votable_arraysize(col_data)

            datatype_type = col.get("datatype", None)
            datatype_arraysize = col.get("arraysize", None)

            datatype_elem = DataType(
                arraysize=datatype_arraysize,
                value=datatype_type,
            )
            return datatype_elem
        # If no datatype provided, default to char(*)
        return DataType(value="char", arraysize="*")

    def __make_flags(self, col_data) -> list[str]:
        """Set up the flag elements when creating the column.

        These flags are represented in the database as a boolean integer, but in the XML are represented
        as XML elements with the name of the flag, i.e. <principal/>, <indexed/>, <std/>.

        """
        if not col_data.get("flag", None):
            flag = [flag for flag in ["principal", "indexed", "std"] if col_data.get(flag, None) == 1]
            return flag
        return col_data["flag"]

    @field_validator("column_name")
    def validate_colname(cls, value):
        """Escape the column name if it is an ADQL reserved word

        See: https://www.ivoa.net/documents/ADQL/20180112/PR-ADQL-2.1-20180112.html#tth_sEc2.1.3
        """
        if value.upper() in ADQL_SQL_KEYWORDS:
            value = f'"{value}"'
        return value

    @field_validator("description")
    def validate_description(cls, value):
        """Sanitize bad XML values in the description"""
        if value:
            value = escape(str(value))
        return value


class _TableName(RootXmlModel[str], tag="name"):
    """Element containing a table name

    Note: used internally to avoid namespacing issues with pydantic-xml
    """


class _TableTitle(RootXmlModel[str], tag="title"):
    """Element containing a table title

    Note: used internally to avoid namespacing issues with pydantic-xml
    """


class _TableDesc(RootXmlModel[str], tag="description"):
    """Element containing a table description

    Note: used internally to avoid namespacing issues with pydantic-xml
    """


class _TableUtype(RootXmlModel[str], tag="utype"):
    """Element containing a table utype

    Note: used internally to avoid namespacing issues with pydantic-xml
    """


class _TableNRows(RootXmlModel[int], tag="nrows"):
    """Element containing an integer describing the number of rows in a table

    Note: used internally to avoid namespacing issues with pydantic-xml
    """


class Table(BaseXmlModel, tag="table", ns="", skip_empty=True):
    """A model representing a single table element.

    The private classes _TableName, _TableTitle, _TableDesc, _TableUtype, and _TableNRows
    are used to create elements that do not inherit the default namespace from their parent.
    This is necessary when creating a VOSITable, which has a default namespace of 'vosi',
    but needs child elements without that prefix, since the elements below are part of the
    VODataservice / DALI standard.
    """

    table_type: Optional[str] = attr(name="type")

    table_name: _TableName = element(tag="name", ns="")
    title: Optional[_TableTitle] = element(tag="title", ns="", default=None)
    description: Optional[_TableDesc] = element(tag="description", ns="", default=None)
    utype: Optional[_TableUtype] = element(tag="utype", ns="", default=None)
    nrows: Optional[_TableNRows] = element(tag="nrows", gte=0, ns="", default=None)
    column: Optional[list[TableParam]] = element(tag="column", ns="", default=None)
    foreign_key: Optional[list[ForeignKey]] = element(tag="foreignKey", ns="", default=None)

    def __init__(__pydantic_self__, **data: Any) -> None:
        """Escape any keys that are passed in."""
        for key, val in data.items():
            if isinstance(val, str):
                data[key] = escape(val)
        super().__init__(**data)


class TableSchema(BaseXmlModel, tag="schema", ns="", skip_empty=True):
    """A model representing a table schema."""

    schema_name: str = element(tag="name", default="default")
    title: Optional[str] = element(tag="title", default=None)
    description: Optional[str] = element(tag="description", default=None)
    table: Optional[list[Table]] = element(tag="table", default=None)

    def __init__(__pydantic_self__, **data: Any) -> None:
        """Escape any keys that are passed in."""
        for key, val in data.items():
            if isinstance(val, str):
                data[key] = escape(val)
        super().__init__(**data)


class TableSet(BaseXmlModel, tag="tableset", skip_empty=True):
    """A model representing a tableset, a list of tables."""

    tableset_schema: list[TableSchema] = element(tag="schema")
