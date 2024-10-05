"""
Module containing VO TapRegExt classes.

IVOA UWS Spec: https://ivoa.net/documents/TAPRegExt/20120827/REC-TAPRegExt-1.0.html
"""

from vo_models.tapregext.models import (
    DataLimit,
    DataLimits,
    DataModelType,
    Language,
    LanguageFeature,
    LanguageFeatureList,
    OutputFormat,
    TableAccess,
    TimeLimits,
    UploadMethod,
    Version,
)

__all__ = [
    "DataLimit",
    "DataLimits",
    "DataModelType",
    "Language",
    "LanguageFeature",
    "LanguageFeatureList",
    "OutputFormat",
    "TableAccess",
    "TimeLimits",
    "UploadMethod",
    "Version",
]
