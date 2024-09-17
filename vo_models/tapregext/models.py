"""TAPRegExt classes."""

from typing import Literal, Optional

from pydantic_xml import BaseXmlModel, attr, element

from vo_models.voresource import Capability, IdentifierURI, Interface, Validation

NSMAP = {
    "xs": "http://www.w3.org/2001/XMLSchema",
    "vr": "http://www.ivoa.net/xml/VOResource/v1.0",
    "vm": "http://www.ivoa.net/xml/VOMetadata/v0.1",
    "tr": "http://www.ivoa.net/xml/TAPRegExt/v1.0",
}


class TAPCapRestriction(Capability, nsmap=NSMAP):
    """An abstract capability that fixes the standardID to the IVOA ID for the TAP standard."""

    validation_level: Optional[list[Validation]] = element(tag="validationLevel", default_factory=[])
    description: Optional[str] = element(tag="description", default=None)
    interface: Optional[list[Interface]] = element(tag="interface", default_factory=[])

    standard_id: IdentifierURI = attr(tag="standardID", default="ivo://ivoa.net/std/TAP")


class DataModelType(BaseXmlModel, nsmap=NSMAP):
    """IVOA defined data model, identified by an IVORN.

    Parameters:
        value:
            (content) - The human-readable name of the data model.
        ivo_id:
            (attribute) - The IVORN of the data model.
    """

    value: str
    ivo_id: str = attr(tag="ivo-id")


class Version(BaseXmlModel, nsmap=NSMAP):
    """One version of the language supported by the service.

    Parameters:
        value:
            (content) - The version of the language.
        ivo_id:
            (attribute) - An optional IVORN of the language.
    """

    value: str
    ivo_id: Optional[str] = attr(tag="ivo-id", default=None)


class LanguageFeature(BaseXmlModel, nsmap=NSMAP):
    """A non-standard or non-mandatory feature implemented by the language.

    Parameters:
        form:
            (element) - Formal notation for the language feature.
        description:
            (element) - Human-readable freeform documentation for the language feature.
    """

    form: str = element(tag="form")
    description: Optional[str] = element(tag="description", default=None)


class OutputFormat(BaseXmlModel, nsmap=NSMAP):
    """An output format supported by the service.

    Parameters:
        mime:
            (element) - The MIME type of this format.
        alias:
            (element) - Other values of FORMAT that make the service return documents with this MIME type.
    """

    mime: str = element(tag="mime")
    alias: Optional[list[str]] = element(tag="alias", default_factory=[])


class UploadMethod(BaseXmlModel, nsmap=NSMAP):
    """An upload method as defined by IVOA.

    Parameters:
        ivo_id:
            (attribute) - The IVORN of the upload method.
    """

    ivo_id: str = attr(tag="ivo-id")


class TimeLimits(BaseXmlModel, nsmap=NSMAP):
    """Time-valued limits, all values given in seconds.

    Parameters:
        default:
            (element) - The value of this limit for newly-created jobs, given in seconds.
        hard:
            (element) - The value this limit cannot be raised above, given in seconds.
    """

    default: Optional[int] = element(tag="default", default=None)
    hard: Optional[int] = element(tag="hard", default=None)


class DataLimits(BaseXmlModel, nsmap=NSMAP):
    """Limits on data sizes, given in rows or bytes.

    Parameters:
        default:
            (element) - The value of this limit for newly-created jobs.
        hard:
            (element) - The value this limit cannot be raised above.
    """

    default: Optional[int] = element(tag="default", default=None)
    hard: Optional[int] = element(tag="hard", default=None)


class DataLimit(BaseXmlModel, nsmap=NSMAP):
    """A limit on some data size, either in rows or in bytes.

    Parameters:
        value:
            (content) - The value of this limit.
        unit:
            (attribute) - The unit of the limit specified.
    """

    value: int
    unit: Literal["byte", "row"] = attr(tag="unit")


class LanguageFeatureList(BaseXmlModel, nsmap=NSMAP):
    """An enumeration of non-standard or non-mandatory features of a specific type implemented by the language.

    Parameters:
        feature:
            (element) - A language feature of the type given by this element's type attribute.
        type:
            (attribute) - The type of the language feature.
    """

    feature: Optional[list[LanguageFeature]] = element(tag="feature", default_factory=[])
    type: str = attr(tag="type")


class Language(BaseXmlModel, nsmap=NSMAP):
    """A query language supported by the service.

    Parameters:
        name:
            (element) - The name of the language without a version suffix.
        version:
            (element) - A version of the language supported by the server.
        description:
            (element) - A short, human-readable description of the query language.
        language_features:
            (element) - Optional features of the query language, grouped by feature type.
    """

    name: str = element(tag="name")
    version: list[Version] = element(tag="version")
    description: Optional[str] = element(tag="description", default=None)
    language_features: Optional[list[LanguageFeatureList]] = element(tag="languageFeatures", default_factory=[])


class TableAccess(TAPCapRestriction):
    """The capabilities of a TAP server.

    Parameters:
        data_model:
            (element) - Identifier of IVOA-approved data model supported by the service.
        language:
            (element) - Language supported by the service.
        output_format:
            (element)  - Output format supported by the service.
        upload_method:
            (element) - Upload method supported by the service.
        retention_period:
            (element) - Limits on the time between job creation and destruction time.
        execution_duration:
            (element) - Limits on executionDuration.
        output_limit:
            (element) - Limits on the size of data returned.
        upload_limit:
            (element) - Limits on the size of uploaded data.
    """

    data_model: Optional[list[DataModelType]] = element(tag="dataModel", default_factory=[])
    language: list[Language] = element(tag="language")
    output_format: list[OutputFormat] = element(tag="outputFormat")
    upload_method: Optional[list[UploadMethod]] = element(tag="uploadMethod", default_factory=[])
    retention_period: Optional[TimeLimits] = element(tag="retentionPeriod", default=None)
    execution_duration: Optional[TimeLimits] = element(tag="executionDuration", default=None)
    output_limit: Optional[DataLimits] = element(tag="outputLimit", default=None)
    upload_limit: Optional[DataLimits] = element(tag="uploadLimit", default=None)
