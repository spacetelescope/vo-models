"""Simple types for the VO Registry 1.1 specification"""

from enum import Enum


class ExtensionSearchSupport(str, Enum):
    """Used in Registry Interfaces 1.0 to denote what VOResource extensions a search interface supports."""

    CORE = "core"
    """Only searches against the core VOResource metadata are supported."""
    PARTIAL = "partial"
    """Searches against some VOResource extension metadata are supported, but not necessarily all that exist
    in the registry."""
    FULL = "full"
    """Searches against all VOResource extension metadata  contained in the registry are supported."""

class OptionalProtocol(str, Enum):
    """Used in Registry Interfaces 1.0 to denote search protocol extensions."""

    XQUERY = "XQuery"
    """The xquery protocol as defined in VO Registry Interface standard."""
