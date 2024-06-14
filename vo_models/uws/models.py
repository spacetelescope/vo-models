"""UWS Job Schema using Pydantic-XML models"""
from typing import Dict, Generic, Optional, TypeVar

from pydantic_xml import BaseXmlModel, attr, element

from vo_models.uws.types import ErrorType, ExecutionPhase, UWSVersion
from vo_models.voresource.types import UTCTimestamp
from vo_models.xlink import XlinkType

NSMAP = {
    "uws": "http://www.ivoa.net/xml/UWS/v1.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

# pylint: disable=invalid-name
ParametersType = TypeVar("ParametersType")


class Parameter(BaseXmlModel, tag="parameter", ns="uws", nsmap=NSMAP):
    """A UWS Job parameter

    Parameters:
        value:
            (content) - the value of the parameter.
        by_reference: (attr) - If this attribute is true then the content of the parameter represents a URL to retrieve the
            actual parameter value.
        id:
            (attr) - The identifier of the parameter.
        is_post:
            (attr) - Undocumented.


    """

    value: Optional[str | int | float | bool | bytes] = None  # only primitive types are allowed

    by_reference: Optional[bool] = attr(name="byReference", default=False)
    id: str = attr()
    is_post: Optional[bool] = attr(name="isPost", default=False)


class Parameters(BaseXmlModel, tag="parameters", ns="uws", nsmap=NSMAP):
    """
    An abstract holder of UWS parameters.

    The list of input parameters to the job - if the job description language does not naturally have
    parameters, then this list should contain one element which is the content of the original POST that created the
    job.
    """

    def __init__(__pydantic_self__, **data) -> None:  # pylint: disable=no-self-argument
        # during init -- especially if reading from xml -- we may not get the parameters in the order
        # pydantic-xml expects. This will remap the dict with keys based on the parameter id.
        parameter_vals = [val for val in data.values() if val is not None]
        remapped_vals = {}
        for param in parameter_vals:
            if isinstance(param, dict):
                remapped_vals[param["id"]] = Parameter(**param)
            else:
                remapped_vals[param.id] = param
        data = remapped_vals
        super().__init__(**data)


class ErrorSummary(BaseXmlModel, tag="errorSummary", ns="uws", nsmap=NSMAP):
    """A short summary of an error

    A fuller representation of the error may be retrieved from /{jobs}/{job-id}/error

    Parameters:
        message:    (element) - A short description of the error.
        type:       (attr) - Characterization of the type of the error
        has_detail: (attr) - If true then there is a more detailed error message available at /{jobs}/{job-id}/error
    """

    message: str = element(default="")

    type: ErrorType = attr(default=ErrorType.TRANSIENT)
    has_detail: bool = attr(name="hasDetail", default=False)


class ResultReference(BaseXmlModel, tag="result", ns="uws", skip_empty=True, nsmap=NSMAP):
    """A reference to a UWS result.

    Parameters:
        id:         (attr) - The identifier of the result.
        type:       (attr) - The xlink type of the result.
        href:       (attr) - The link to the result.
        size:       (attr) - The size of the result in bytes.
        mime_type:  (attr) - The MIME type of the result.
        any_attrs:  (attr) - Any other attributes of the result.
    """

    id: str = attr()

    # attributeGroup uws:reference
    type: Optional[XlinkType] = attr(ns="xlink", default=XlinkType.SIMPLE)
    href: Optional[str] = attr(ns="xlink", default=None)

    size: Optional[int] = attr(default=None)
    mime_type: Optional[str] = attr(name="mime-type", default=None)

    any_attrs: Optional[Dict[str, str]] = None


class Results(BaseXmlModel, tag="results", ns="uws", nsmap=NSMAP):
    """The element returned for /{jobs}/{job-id}/results

    Parameters:
        results: (element) A list of references to UWS results.
    """

    results: Optional[list[ResultReference]] = element(name="result", default_factory=list)


class ShortJobDescription(BaseXmlModel, tag="jobref", ns="uws", nsmap=NSMAP):
    """A short description of a job.

    Parameters:
        phase:
            (element) - The execution phase - returned at /{jobs}/{job-id}/phase
        run_id:
            (element) - A client supplied identifier - the UWS system does nothing other than to return it as part of
            the description of the job
        owner_id:
            (element) - The owner (creator) of the job - this should be expressed as a string that can be parsed in
            accordance with IVOA security standards.
        creation_time:
            (element) - The instant at which the job was created.
        job_id:
            (attr) - The identifier for the job.
        type:
            (attr) - The xlink reference type of the job.
        href:
            (attr) - The link to the job.
    """

    phase: ExecutionPhase = element()
    run_id: Optional[str] = element(tag="runId", default=None)
    owner_id: Optional[str] = element(tag="ownerId", default=None, nillable=True)
    creation_time: Optional[UTCTimestamp] = element(tag="creationTime", default=None)

    job_id: str = attr(name="id")
    type: Optional[XlinkType] = attr(ns="xlink", default=XlinkType.SIMPLE)
    href: Optional[str] = attr(ns="xlink", default=None)


class Jobs(BaseXmlModel, tag="jobs", ns="uws", nsmap=NSMAP):
    """The list of job references returned at /(jobs)

    The list presented may be affected by the current security context and may be filtered

    Parameters:
        jobref: (element) a list of UWS Jobs.

        version:
            (attr) - The version of the UWS standard that the server complies with.

                    Note that this attribute is actually required by the 1.1 specification - however remains
                    optional in the schema for backwards compatibility.
                    It will be formally required in the next major revision.
    """

    jobref: Optional[list[ShortJobDescription]] = element(name="jobref", default_factory=list)

    version: Optional[UWSVersion] = attr(default=UWSVersion.V1_1)


class JobSummary(BaseXmlModel, Generic[ParametersType], tag="job", ns="uws", nsmap=NSMAP):
    """The complete representation of the state of a job

    Parameters:
        job_id:
            (element) - The identifier for the job.
        run_id:
            (element) - This is a client supplied identifier - the UWS system does nothing other than to return it
            as part of the description of the job
        owner_id:
            (element) - The owner (creator) of the job - this should be expressed as a string that can be
            parsed in accordance with IVOA security standards.

                        If there was no authenticated job creator then this should be set to NULL.
        phase:
            (element) - The execution phase.
        quote:
            (element) - A Quote predicts when the job is likely to complete.
        creation_time:
            (element) - The instant at which the job was created.

                        Note that the version 1.1 of the specification requires that this element
                        be present. It is optional only in versions 1.x of the schema for backwards compatibility.
                        2.0+ versions of the schema will make this formally mandatory in an XML sense.
        start_time:
            (element) - The instant at which the job started execution.
        end_time:
            (element) - The instant at which the job finished execution.
        execution_duration:
            (element) - The duration (in seconds) for which the job should be allowed to run.

                        A value of 0 is intended to mean unlimited.
        destruction:
            (element) - The time at which the whole job + records + results will be destroyed.
        parameters:
            (element) - The parameters to the job (where appropriate)
        results:
            (element) - The results for the job
        error_summary:
            (element) - A short summary of an error
        job_info:
            (element) - This is arbitrary information that can be added to the job description by the UWS
            implementation.

        version:
            (attr) - The version of the UWS standard that the server complies with.

                    Note that this attribute is actually required by the 1.1 specification - however remains optional
                    in the schema for backwards compatibility. It will be formally required in the next major revision.
    """

    # pylint: disable = too-few-public-methods

    job_id: str = element(tag="jobId")
    run_id: Optional[str] = element(tag="runId", default=None)
    owner_id: Optional[str] = element(tag="ownerId", default=None, nillable=True)
    phase: ExecutionPhase = element(tag="phase")
    quote: Optional[UTCTimestamp] = element(tag="quote", default=None, nillable=True)
    creation_time: Optional[UTCTimestamp] = element(tag="creationTime", default=None)
    start_time: Optional[UTCTimestamp] = element(tag="startTime", default=None, nillable=True)
    end_time: Optional[UTCTimestamp] = element(tag="endTime", default=None, nillable=True)
    execution_duration: Optional[int] = element(tag="executionDuration", default=0)
    destruction: Optional[UTCTimestamp] = element(tag="destruction", default=None, nillable=True)
    parameters: Optional[ParametersType] = element(tag="parameters", default=None)
    results: Optional[Results] = element(tag="results", default=Results())
    error_summary: Optional[ErrorSummary] = element(tag="errorSummary", default=None)
    job_info: Optional[list[str]] = element(tag="jobInfo", default=[])

    version: Optional[UWSVersion] = attr(default=UWSVersion.V1_1)

    class Config:
        """JobSummary pydantic config options"""

        arbitrary_types_allowed = True


class Job(JobSummary, tag="job"):
    """This is the information that is returned when a GET is made for a single job resource - i.e. /{jobs}/{job-id}"""
