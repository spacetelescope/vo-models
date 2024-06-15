"""Simple types for VODataService XML elements."""

import re
from enum import Enum
from typing import Annotated

from pydantic import Field


class HTTPQueryType(str, Enum):
    """The type of HTTP request, either GET or POST.

    The service may indicate support for both GET and POST by providing 2 queryType elements, one with GET and one with
    POST. Since the IVOA standard DALI requires standard services to support both GET and POST, this piece of metadata
    is not useful in the description of standard DAL services and does not need to be given for those.
    """

    GET = "GET"
    POST = "POST"


class ParamUse(str, Enum):
    """
    The use of a parameter in a query.
    """

    REQUIRED = "required"
    """
    The parameter is required for the application or service to work properly.
    """
    OPTIONAL = "optional"
    """
    The parameter is optional but supported by the application or service.
    """
    IGNORED = "ignored"
    """
    The parameter is not supported and thus is ignored by the application or service.
    """


ArrayShape = Annotated[
    str,
    Field(
        pattern=r"([0-9]+x)*[0-9]*[0-9*]",
        description="An expression of a the shape of a multi-dimensional array of the form LxNxM",
    ),
]

FloatInterval = Annotated[
    str,
    Field(
        pattern=r"[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)? [+-]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)?",
        description="An interval of floating point numbers.",
    ),
]
