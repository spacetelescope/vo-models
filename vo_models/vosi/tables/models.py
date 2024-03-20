"""Pydantic-xml models for the VOSI Tables specification"""
from vo_models.vodataservice import Table, TableSet

NSMAP = {
    "vosi": "http://www.ivoa.net/xml/VOSITables/v1.0",
    "vr": "http://www.ivoa.net/xml/VOResource/v1.0",
    "vs": "http://www.ivoa.net/xml/VODataService/v1.1",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class VOSITable(Table, tag="table", ns="vosi", nsmap=NSMAP):
    """A table element as returned by a VOSI /tables request

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


class VOSITableSet(TableSet, tag="tableset", ns="vosi", nsmap=NSMAP):
    """A tableset element as returned by a VOSI /tables request

    Parameters:
        tableset_schema:
            (elem) - A named description of a group of logically related tables.

                The name given by the “name” child element must be unique within this TableSet instance.
                If there is only one schema in this set and/or there is no locally appropriate name to provide,
                the name can be set to “default”.
    """
