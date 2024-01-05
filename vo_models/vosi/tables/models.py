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
    """A table element as returned by a VOSI /tables request"""


class VOSITableSet(TableSet, tag="tableset", ns="vosi", nsmap=NSMAP):
    """A tableset element as returned by a VOSI /tables request"""
