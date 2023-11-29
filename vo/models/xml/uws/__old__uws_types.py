"""Simple types for UWS models"""
from enum import Enum


class ExecutionPhase(str, Enum):
    """Enum for valid async job phases. Not necessarily all supported.
    From https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html#ExecutionPhase"""

    PENDING = "PENDING"
    QUEUED = "QUEUED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    ABORTED = "ABORTED"
    UNKNOWN = "UNKNOWN"
    HELD = "HELD"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"
    RUN = "RUN"  # nonstandard support for astropy/TAPPlus


class ErrorTypeName(str, Enum):
    """Enum for error types in job summary.
    From https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html#Error"""

    TRANSIENT = "transient"
    FATAL = "fatal"


class UWSVersions(str, Enum):
    """Supported UWS version numbers"""

    V1_0 = "1.0"
    V1_1 = "1.1"
