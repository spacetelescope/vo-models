"""UWS Job Schema using Pydantic-XML models"""
from typing import Dict, Optional, Union
from xml.etree.ElementTree import Element

from pydantic import field_validator
from pydantic_xml import BaseXmlModel, attr, element

from vo.models.xml.generics import DatetimeElement, NillElement
from vo.models.xml.uws.types import ErrorType, ExecutionPhase, UWSVersion
from vo.models.xml.xlink import XlinkType

NSMAP = {
    "uws": "http://www.ivoa.net/xml/UWS/v1.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class Parameter(BaseXmlModel, tag="parameter", ns="uws", nsmap=NSMAP):
    """A UWS Job parameter

    The list of input parameters to the job - if the job description language does not naturally have
    parameters, then this list should contain one element which is the content of the original POST that created the
    job.

    Attributes:
    byReference (bool): If this attribute is true then the content of the parameter represents a URL to retrieve the
                        actual parameter value.
                        It is up to the implementation to decide if a parameter value cannot be returned directly as
                        the content - the basic rule is that the representation of the parameter must allow the whole
                        job element to be valid XML. If this cannot be achieved then the parameter value must be
                        returned by reference.
    id (str):           The identifier of the parameter.
    isPost (bool):      Undocumented.

    Content:
    value (str): the value of the parameter.
    """

    value: Optional[str] = None

    by_reference: Optional[bool] = attr(name="byReference", default=False)
    id: str = attr()
    isPost: Optional[bool] = attr(name="isPost", default=None)


class Parameters(BaseXmlModel, tag="parameters", ns="uws", nsmap=NSMAP):
    """A list of UWS Job parameters.

    Elements:
    parameter (Parameter): a UWS Job parameter.
    """

    parameter: Optional[list[Parameter]] = element(name="parameter", default_factory=list)


class ErrorSummary(BaseXmlModel, tag="errorSummary", ns="uws", nsmap=NSMAP):
    """A short summary of an error - a fuller representation of the
        error may be retrieved from /{jobs}/{job-id}/error

    Elements:
    message (str):  a short description of the error.

    Attributes:
    type (ErrorType):   Characterization of the type of the error
    has_detail (bool):  If true then there is a more detailed error message available at /{jobs}/{job-id}/error
    """

    message: str = element()

    type: ErrorType = attr()
    has_detail: bool = attr(name="hasDetail")


class ResultReference(BaseXmlModel, tag="resultReference", ns="uws", nsmap=NSMAP):
    """A reference to a UWS result.

    Attributes:
    id (str):           The identifier of the result.
    mime_type (str):    The MIME type of the result.
    size (int):         The size of the result in bytes.
    """

    id: str = attr()

    # attributeGroup uws:reference
    type: Optional[XlinkType] = attr(ns="xlink", default=XlinkType.SIMPLE)
    href: Optional[str] = attr(ns="xlink", default=None)

    size: Optional[int] = attr(default=None)
    mime_type: Optional[str] = attr(name="mime-type", default=None)

    any_attrs: Dict[str, str]


class Results(BaseXmlModel, tag="results", ns="uws", nsmap=NSMAP):
    """The element returned for /{jobs}/{job-id}/results

    Elements:
    result list[ResultReference]: a list of references to UWS results.
    """

    results: Optional[list[ResultReference]] = element(name="result", default_factory=list)


class Jobs(BaseXmlModel, tag="jobs", ns="uws", nsmap=NSMAP):
    """The list of job references returned at /(jobs)

    The list presented may be affected by the current security context and may be filtered

    Elements:
    job list(Job): a list of UWS Jobs.

    Attributes:
    version (UWSVersion):   The version of the UWS standard that the server complies with.
                            Note that this attribute is actually required by the 1.1 specification - however remains
                            optional in the schema for backwards compatibility.
                            It will be formally required in the next major revision.
    """

    jobref: Optional[list["ShortJobDescription"]] = element(name="jobref", default_factory=list)

    version: Optional[UWSVersion] = attr(default=UWSVersion.V1_1)


class JobSummary(BaseXmlModel, tag="job", ns="uws", nsmap=NSMAP, skip_empty=True):
    """The complete representation of the state of a job

    Elements:
    job_id (JobIdentifier, str):    The identifier for the job.
    run_id (str):                   This is a client supplied identifier - the UWS system does nothing other than to
                                    return it as part of the description of the job
    owner_id (str):                 The owner (creator) of the job - this should be expressed as a string that can be
                                    parsed in accordance with IVOA security standards. If there was no authenticated
                                    job creator then this should be set to NULL.
    phase (ExecutionPhase):         The execution phase - returned at /{jobs}/{job-id}/phase
    quote (datetime):               A Quote predicts when the job is likely to complete - returned at
                                    /{jobs}/{job-id}/quote
                                    "don't know" is encoded by setting to the XML null value xsi:nil="true"
    creation_time (datetime):       The instant at which the job was created.
                                    Note that the version 1.1 of the specification requires that this element
                                    be present.
                                    It is optional only in versions 1.x of the schema for backwards compatibility.
                                    2.0+ versions of the schema will make this formally mandatory in an XML sense.
    start_time (datetime):          The instant at which the job started execution.
    end_time (datetime):            The instant at which the job finished execution.
    execution_duration (timedelta): The duration (in seconds) for which the job should be allowed to run - a value of 0
                                    is intended to mean unlimited - returned at /{jobs}/{job-id}/executionduration
    destruction (datetime):         The time at which the whole job + records + results will be destroyed.
                                    Returned at /{jobs}/{job-id}/destruction
    parameters (Parameters):        The parameters to the job (where appropriate) can also be retrieved at
                                    /{jobs}/{job-id}/parameters
    results (Results):              The results for the job - can also be retrieved at /{jobs}/{job-id}/results
    error_summary (ErrorSummary):   A short summary of an error
    job_info (Any):                 This is arbitrary information that can be added to the job description by the UWS
                                    implementation.

    Attributes:
    version: (UWSVersion)   Note that this attribute is actually required by the 1.1 specification - however remains
                            optional in the schema for backwards compatibility.
                            It will be formally required in the next major revision.
    """

    # pylint: disable = no-self-argument

    job_id: str = element(tag="jobId")
    run_id: Optional[str] = element(tag="runId", default=None)
    owner_id: Optional[NillElement] = element(tag="ownerId", default=None)
    phase: ExecutionPhase = element(tag="phase")
    quote: Optional[NillElement] = element(tag="quote", default=None)
    creation_time: Optional[DatetimeElement] = element(tag="creationTime", default=None)
    start_time: Optional[Union[NillElement, DatetimeElement]] = element(tag="startTime", default=None)
    end_time: Optional[Union[NillElement, DatetimeElement]] = element(tag="endTime", default=None)
    execution_duration: Optional[int] = element(tag="executionDuration", default=0)
    destruction: Optional[Union[NillElement, DatetimeElement]] = element(tag="destruction", default=None)
    parameters: Optional[Parameters] = element(tag="parameters", default=None)
    results: Optional[Results] = element(tag="results", default=None)
    error_summary: Optional[ErrorSummary] = element(tag="errorSummary", default=None)
    job_info: Optional[list[Element]] = element(default_factory=[])

    version: Optional[UWSVersion] = attr(default=UWSVersion.V1_1)

    @field_validator("owner_id")
    def validate_owner_id(cls, value):
        """Sets default for owner_id if None"""
        if not value:
            return NillElement()
        return value

    @field_validator("quote")
    def validate_quote(cls, value):
        """Sets default for quote if None"""
        if not value:
            return NillElement()
        return value

    @field_validator("destruction")
    def validate_destruction(cls, value):
        """Sets default for destruction if None"""
        if not value:
            return NillElement()
        return value

    class Config:
        """JobSummary pydantic config options"""

        arbitrary_types_allowed = True


class Job(JobSummary, tag="job"):
    """This is the information that is returned when a GET is made for a single job resource - i.e. /{jobs}/{job-id}"""


class ShortJobDescription(BaseXmlModel, tag="jobref", ns="uws", nsmap=NSMAP):
    """A short description of a job."""

    # pylint: disable = no-self-argument

    phase: ExecutionPhase = element()
    run_id: Optional[str] = element(tag="runId", default=None)
    owner_id: Optional[NillElement] = element(tag="ownerId", default=None)
    creation_time: Optional[DatetimeElement] = element(tag="creationTime", default=None)

    job_id: str = attr(name="id")
    type: Optional[XlinkType] = attr(ns="xlink", default=XlinkType.SIMPLE)
    href: Optional[str] = attr(ns="xlink", default=None)

    @field_validator("owner_id")
    def validate_owner_id(cls, value):
        """Sets default for owner_id if None"""
        if not value:
            return NillElement()
        return value
