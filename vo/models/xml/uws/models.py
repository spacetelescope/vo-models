"""UWS Job Schema using Pydantic-XML models"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Generic, Optional, TypeVar, Union
from xml.etree.ElementTree import Element

from pydantic import validator
from pydantic_xml import BaseXmlModel, attr, element

from vo.models.xml.generics import NillableElement, VODateTime
from vo.models.xml.uws.types import ErrorType, ExecutionPhase, UWSVersion
from vo.models.xml.xlink import TypeValue

NSMAP = {
    "uws": "http://www.ivoa.net/xml/UWS/v1.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class Parameter(BaseXmlModel, tag="parameter", ns="uws", nsmap=NSMAP):
    """A UWS Job parameter

    The list of input parameters to the job - if the job description language does not naturally have
    parameters, then this list should contain one element which is the content of the original POST that created the job.

    Attributes:
    byReference (bool): if this attribute is true then the content of the parameter represents a URL to retrieve the
                        actual parameter value.
                        It is up to the implementation to decide if a parameter value cannot be returned directly as
                        the content - the basic rule is that the representation of the parameter must allow the whole
                        job element to be valid XML. If this cannot be achieved then the parameter value must be
                        returned by reference.
    id (str): the identifier of the parameter.
    isPost (bool): undocumented.

    Content:
    value (str): the value of the parameter.
    """

    value: Optional[str]

    by_reference: Optional[bool] = attr(name="byReference", default=False)
    id: str = attr()
    isPost: Optional[bool] = attr(name="isPost")


class Parameters(BaseXmlModel, tag="parameters", ns="uws", nsmap=NSMAP):
    """A list of UWS Job parameters.

    Elements:
    parameter (Parameter): a UWS Job parameter.
    """

    parameter: Optional[list[Parameter]] = element(name="parameter", min_occurs=0, max_occurs=None)


class ErrorSummary(BaseXmlModel, tag="errorSummary", ns="uws", nsmap=NSMAP):
    """A short summary of an error - a fuller representation of the
        error may be retrieved from /{jobs}/{job-id}/error

    Elements:
    message (str): a short description of the error.

    Attributes:
    type (ErrorType): Characterization of the type of the error
    has_detail (bool): if true then there is a more detailed error message available at /{jobs}/{job-id}/error
    """

    message: str = element()

    type: ErrorType = attr()
    has_detail: bool = attr(name="hasDetail")


class ResultReference(BaseXmlModel, tag="resultReference", ns="uws", nsmap=NSMAP):
    """A reference to a UWS result.

    Attributes:
    id (str): the identifier of the result.
    mime_type (str): the MIME type of the result.
    size (int): the size of the result in bytes.
    """

    id: str = attr()

    # attributeGroup uws:reference
    type: Optional[TypeValue] = attr(ns="xlink", default=TypeValue.SIMPLE)
    href: Optional[str] = attr(ns="xlink")

    size: Optional[int] = attr()
    mime_type: Optional[str] = attr(name="mime-type")

    any_attrs: Dict[str, str]


class Results(BaseXmlModel, tag="results", ns="uws", nsmap=NSMAP):
    """The element returned for /{jobs}/{job-id}/results

    Elements:
    result list[ResultReference]: a list of references to UWS results.
    """

    result: Optional[list[ResultReference]] = element(name="result")


class Jobs(BaseXmlModel, tag="jobs", ns="uws", nsmap=NSMAP):
    """The list of job references returned at /(jobs)

    The list presented may be affected by the current security context and may be filtered

    Elements:
    job list(Job): a list of UWS Jobs.

    Attributes:
    version (UWSVersion): the version of the UWS standard that the server complies with.
                        Note that this attribute is actually required by the 1.1 specification - however remains
                        optional in the schema for backwards compatibility. It will be formally required in the next
                        major revision.
    """

    jobref: Optional[list["ShortJobDescription"]] = element(name="jobref")

    version: Optional[UWSVersion] = attr()


class JobSummary(BaseXmlModel, ns="uws", nsmap=NSMAP):
    """The complete representation of the state of a job

    Elements:
    job_id (JobIdentifier, str): the identifier for the job.
    run_id (str): This is a client supplied identifier - the UWS system does nothing other than to return it as part of
                the description of the job
    owner_id (str): The owner (creator) of the job - this should be expressed as a string that can be parsed in
                accordance with IVOA security standards. If there was no authenticated job creator then this should be
                set to NULL.
    phase (ExecutionPhase): the execution phase - returned at /{jobs}/{job-id}/phase
    quote (datetime): A Quote predicts when the job is likely to complete - returned at /{jobs}/{job-id}/quote
                "don't know" is encoded by setting to the XML null value xsi:nil="true"
    creation_time (datetime): The instant at which the job was created.
                        Note that the version 1.1 of the specification requires that this element be present.
                        It is optional only in versions 1.x of the schema for backwards compatibility.
                        2.0+ versions of the schema will make this formally mandatory in an XML sense.
    start_time (datetime): The instant at which the job started execution.
    end_time (datetime): The instant at which the job finished execution.
    execution_duration (timedelta): The duration (in seconds) for which the job should be allowed to run - a value of 0
                    is intended to mean unlimited - returned at /{jobs}/{job-id}/executionduration
    destruction (datetime): The time at which the whole job + records + results will be destroyed.
                        Returned at /{jobs}/{job-id}/destruction
    parameters (Parameters): The parameters to the job (where appropriate) can also be retrieved at
                        /{jobs}/{job-id}/parameters
    results (Results): The results for the job - can also be retrieved at /{jobs}/{job-id}/results
    error_summary (ErrorSummary): A short summary of an error
    job_info (Any): This is arbitrary information that can be added to the job description by the UWS implementation.

    Attributes:
    version: (UWSVersion) note that this attribute is actually required by the 1.1 specification - however remains
            optional in the schema for backwards compatibility. It will be formally required in the next major revision.
    """

    job_id: str = element(tag="jobId")
    run_id: Optional[str] = element(tag="runId")
    owner_id: Optional[NillableElement] = element(tag="ownerId")
    phase: ExecutionPhase = element(tag="phase")
    quote: Optional[NillableElement] = element(tag="quote")
    creation_time: Optional[datetime] = element(tag="creationTime")
    start_time: Optional[datetime] = element(tag="startTime")
    end_time: Optional[datetime] = element(tag="endTime")
    execution_duration: Optional[int] = element(tag="executionDuration", default=0)
    destruction: Optional[NillableElement] = element(tag="destruction")
    parameters: Optional[Parameters] = element(tag="parameters")
    results: Optional[Results] = element(tag="results")
    error_summary: Optional[ErrorSummary] = element(tag="errorSummary")
    job_info: list[Element] = element()

    version: Optional[UWSVersion] = attr()

    class Config:
        """JobSummary pydantic config options"""

        arbitrary_types_allowed = True


class Job(JobSummary, tag="job"):
    """This is the information that is returned when a GET is made for a single job resource - i.e. /{jobs}/{job-id}"""


class ShortJobDescription(BaseXmlModel, tag="jobref", ns="uws", nsmap=NSMAP):
    """A short description of a job."""

    phase: ExecutionPhase = element()
    run_id: Optional[str] = element(tag="runId")
    owner_id: Optional[NillableElement] = element(tag="ownerId")
    creation_time: Optional[datetime] = element(tag="creationTime")

    id: str = attr()
