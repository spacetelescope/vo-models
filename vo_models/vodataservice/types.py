"""Simple types for VODataService XML elements."""

from enum import Enum


class HTTPQueryType(Enum, str):
    """The type of HTTP request, either GET or POST.

    The service may indicate support for both GET
    and POST by providing 2 queryType elements, one
    with GET and one with POST.  Since the IVOA standard
    DALI requires standard services to support both
    GET and POST, this piece of metadata is not
    useful in the description of standard DAL services
    and does not need to be given for those.
    """

    GET: str = "GET"
    POST: str = "POST"


class ParamUse(Enum, str):
    """
    The use of a parameter in a query.  The values are:

    required: The parameter is required for the application or
              service to work properly.
    optional: The parameter is optional but supported by the application or
              service.
    ignored: The parameter is not supported and thus is ignored by the
              application or service.
    """

    REQUIRED: str = "required"
    OPTIONAL: str = "optional"
    IGNORED: str = "ignored"


class ArrayShape(str):
    """An expression of a the shape of a multi-dimensional array of the form
    LxNxM... where each value between gives the integer length of the
    array along a dimension. An asterisk (*) as the last dimension of
    the shape indicates that the length of the last axis is variable or
    undetermined."""

    pattern = r"([0-9]+x)*[0-9]*[0-9*]"

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(pattern=cls.pattern)


class FloatInterval(str):
    """An interval of floating point numbers.

    This uses VOTable TABLEDATA serialisation, i.e., simply
    a pair of XSD floating point numbers separated by whitespace;
    note that software utilising non-XSD aware parsers has to
    perform whitespace normalisation itself here (in particular,
    for the internal whitespace).

    """

    pattern = r"[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)? [+-]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)?"

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(pattern=cls.pattern)
