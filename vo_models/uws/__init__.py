"""
Module containing VO Universal Worker Service (UWS) classes.

Contains pydantic-xml models for UWS request / response serialization.
IVOA UWS Spec: https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html
"""
from vo_models.uws.models import (
    ErrorSummary,
    Job,
    Jobs,
    JobSummary,
    Parameter,
    Parameters,
    ParametersType,
    ResultReference,
    Results,
    ShortJobDescription,
)
