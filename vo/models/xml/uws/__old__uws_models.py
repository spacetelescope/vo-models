"""UWS Job Schema using Pydantic-XML models"""
from datetime import timedelta, timezone
from typing import Any, Generic, Optional, TypeVar, Union

from pydantic import validator
from pydantic_xml import BaseXmlModel, attr, element

from vo.models.xml.generics import VODateTime
from vo.models.xml.uws.__old__uws_types import ErrorTypeName, ExecutionPhase, UWSVersions
from vo.models.xml.xlink import TypeValue

# pylint: disable=line-too-long
# pylint: disable=no-self-argument

NSMAP = {
    "uws": "http://www.ivoa.net/xml/UWS/v1.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

RESULT_EXPIRATION_SEC = 24 * 60 * 60  # 1 day in seconds


def validate_nillable(value, expected_type) -> dict:
    """Creates a dictionary representing a NillableElement for a pydantic-xml model.

    The dictionary creates the element by way of NillableElement(**dict) in pydantic-xml internally.
    It also handles deserialized cases, when reading from the cache, for example.

    Example:
    the <startTime> element

    - job_summary.start_time = 01-01-1970
    -- pydantic-xml receives NillableElement(**{value:'01-01-1970', nil:None})
    -- the element is represented as <startTime>01-01-1970</startTime>

    - job_summary.start_time = None (or value was not provided)
    -- pydantic-xml receives NillableElement(**{value:None, nil:'true'})
    -- the element is represented as <startTime xsi:nil='true' />

    When serialized (not XML - in the cache as a dict) the element is represented by:
        if defined:
            start_time = {'value':'01-01-1970', 'nil'=None}
        or if not defined:
            start_time = None

    When JobSummary elements are deserialized from the cache, these elements are handled similarly
    as the above cases.
    """
    if value:
        if isinstance(value, NillableElement):
            return value
        if isinstance(value, dict):
            # if we received a dict to validate, we're reading this value from the cache, and was
            # already coerced into the format of a NillableElement dict.
            if value.get("value"):
                # if value was previously set, check it (mostly in cases of bad cache/model data)
                if not isinstance(value.get("value"), expected_type):
                    raise ValueError(f"Incorrect type for value: {value}. Expected type {str(expected_type)}")
            return value

        if not isinstance(value, expected_type):
            # if we actually got a value, it's probably from user or code input - validate it
            raise ValueError(f"Incorrect type for value: {value}. Expected type {str(expected_type)}")
        return {"value": value}

    return {"nil": "true"}


class NillableElement(BaseXmlModel, ns="uws", nsmap=NSMAP):
    """A generic used for elements that may have a value, but must display a 'xsi:nil' attribute when they do not.

    Used to maintain compatibility with the pydantic-xml 'to_xml()' function parameter 'skip_empty=True'

    The skip_empty=True parameter allows XML elements with no content (optionals) to be skipped when serializing
    elements. Without it, pydantic-xml will attempt to serialize every element and attribute. Optionals with None,
    will fail and throw an error. Therefore, if we have an element that can be None, but must also be displayed
    and have a 'nil' attribute, we need to handle it differently.

    The 'validate_nillable' function above will create a blank nillable element for a job attribute that was not
    defined (owner_id=None) but must be displayed. Those elements are ownerId, quote, startTime, endTime and destruction.
    We define destruction at job creation, so it is not necessary to check.
    """

    value: Optional[str]
    nil: Optional[str] = attr(name="nil", ns="xsi")


class DatetimeElement(BaseXmlModel, ns="uws", nsmap=NSMAP):
    """A wrapper element for a VODatetime object.

    Necessary to allow a Union between a NillableElement and simple VODatetime datatype.
    """

    __root__: VODateTime


class ErrorSummary(BaseXmlModel, tag="errorSummary", ns="uws", nsmap=NSMAP):
    """ErrorSummary element - a short summary of a UWS Job error

    Included as part of a JobSummary - a full representation of the error is available
    from the /{job_id}/error endpoint.

    Elements:
        message: a brief summary of the error.
    Attributes:
        type: characterization of the error type - transient or fatal
        has_detail: if true there is a more detailed error message at the errors endpoint

    """

    message: str = element(tag="message", default="")

    type: ErrorTypeName = attr(name="type", default=ErrorTypeName.TRANSIENT)
    has_detail: bool = attr(name="hasDetail", default=False)


class Parameter(BaseXmlModel, tag="parameter", ns="uws", nsmap=NSMAP):
    """Parameter element - list of input parameters to an async job

    value: the text content of the parameter tag

    Attributes
        id: the parameter's identifier e.g. 'maxrec', 'catalog'
        byReference: if true, the content of the parameter is a URL where the actual parameter value is stored
        is_post: isn't documented in the UWS spec...
    """

    value: Optional[str]
    by_reference: Optional[bool] = attr(name="byReference")
    id: str = attr(name="id")
    is_post: Optional[bool] = attr(name="isPost")


class ResultReference(BaseXmlModel, tag="result", ns="uws", nsmap=NSMAP):
    """ResultReference element - simple container for xlink result references"""

    id: str = attr(name="id", default="result")
    type: Optional[TypeValue] = attr(
        name="type",
        ns="xlink",
        default=TypeValue.SIMPLE,
    )
    href: Optional[str] = attr(ns="xlink")
    size: Optional[int] = attr()
    mime_type: Optional[str] = attr(name="mime-type")


class ShortJobDescription(BaseXmlModel, tag="jobref", ns="uws", nsmap=NSMAP):
    """ShortJobDescription element - a brief description of a UWS Job

    This is returned as part of a JobList query, to keep the list of results brief.

    Elements:
        phase: the execution phase - returned at /{job_id}/phase
        runId: a client-supplied identifier - UWS simply returns it when referencing the job
        ownerId: the creator of the job - a parsable string, otherwise a nill element
        creationTime: the instance a job was created
    Attributes:
        job_id: UUID4 identifier for the job
        xsi:type/href: a link to the full job summary endpoint
    """

    phase: ExecutionPhase = element(tag="phase")
    run_id: Optional[str] = element(tag="runId")
    owner_id: Optional[NillableElement] = element(tag="ownerId")
    creation_time: VODateTime = element(tag="creationTime")

    job_id: str = attr(name="id")
    type: Optional[TypeValue] = attr(ns="xlink", name="type", default=TypeValue.SIMPLE)
    href: Optional[str] = attr(ns="xlink")

    @validator("owner_id", pre=True, always=True)
    def validate_ownerid(cls, value):
        """Validate the owner_id - create a nillable element if it doesn't exist"""
        return validate_nillable(value, str)


class Parameters(BaseXmlModel, tag="parameters", ns="uws", nsmap=NSMAP):
    """A generic UWS parameters type

    Used to create a list of parameters for a UWS JobSummary object.
    Parameters subtypes should be created for specific UWS applications with the appropriate
    service-specific parameters. See asb.core.vo.uws.tap_models.TAPParameters for an example.
    """

    def __init__(__pydantic_self__, **data: Any) -> None:
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

    class Config:
        """UWS Parameters config"""

        extra = "allow"


# pylint: disable=invalid-name
ParametersType = TypeVar("ParametersType", bound=Parameters)


class Results(BaseXmlModel, tag="results", ns="uws", nsmap=NSMAP):
    """Results element - a simple container holding a list of Result elements"""

    results: list[ResultReference] = element(tag="result", default_factory=lambda: [])


class JobSummary(BaseGenericXmlModel, Generic[ParametersType], tag="job", ns="uws", nsmap=NSMAP):
    """JobSummary element - The complete representation of the state of a UWS Job

    JobSummary takes a Generic type for the Parameters element, allowing for service-specific
    parameters (TAP for example) to be included in the JobSummary. This allows us to use the common model structure
    of the UWS JobSummary with any parameters, but swap in alternate parameters when stricter
    service-specific validation is needed.

    For pydantic docs on generic models see: https://docs.pydantic.dev/latest/usage/models/#generic-models
    And for generic xml models with pydantic-xml: https://pydantic-xml.readthedocs.io/en/latest/pages/data-binding/generics.html

    Attributes:
        version (schema_version) - the UWS service version. Required by UWS V1.1
            Version 1.0 is included in an Enum for read-support only.
    Elements:
        job_id: the server-provided UUID4 identifier for the job
        run_id: a client-provided string - UWS simply returns it as part of the job
        owner_id: the creator of the job - a parsable string, otherwise a nill element
        phase: the execution phase of the job - returned at /{job_id}/phase
        quote: when the job is likely to complete (datetime) or a nill value
            -- not supported in our implementation
        creation_time: the datetime when the job was created
        start_time: the datetime a job started execution
        end_time: the datetime a job finished execution
        execution_duration: how long (in seconds) a job is permitted to run - 0 for unlimited
        destruction: the datetime at which the job + records + results will be destroyed
        parameters: a Parameters object containing a list of job creation parameters
        results: the results for the job - also retrieved at /{job_id}/results
        error_summary: a brief description of an error, if one occurred during the job
        job_info: arbitrary information that can be provided by the UWS service
    """

    schema_version: UWSVersions = attr(name="version", default=UWSVersions.V1_1.value)

    job_id: str = element(tag="jobId")
    run_id: Optional[str] = element(tag="runId")
    owner_id: Optional[NillableElement] = element(tag="ownerId")
    phase: Optional[ExecutionPhase] = element(tag="phase", default=ExecutionPhase.PENDING)
    quote: Optional[NillableElement] = element(tag="quote")
    creation_time: Optional[VODateTime] = element(
        tag="creationTime", default_factory=lambda: VODateTime.now(timezone.utc)
    )
    start_time: Optional[Union[NillableElement, DatetimeElement]] = element(tag="startTime")
    end_time: Optional[Union[NillableElement, DatetimeElement]] = element(tag="endTime")
    execution_duration: Optional[int] = element(tag="executionDuration", default=0)
    destruction: Optional[VODateTime] = element(
        tag="destruction",
        default_factory=lambda: VODateTime.now(timezone.utc) + timedelta(seconds=RESULT_EXPIRATION_SEC),
    )
    parameters: ParametersType = element(tag="parameters", default_factory=lambda: [])
    results: Optional[Results] = element(tag="results")
    error_summary: Optional[ErrorSummary] = element(tag="errorSummary")
    job_info: Optional[list[str]] = element(tag="jobInfo")

    @validator("run_id")
    def validate_runid_length(cls, value):
        """Validate the run_id is < 64 characters. Should also be handled by the FastAPI endpoint."""
        if value:
            if len(value) > 64:
                raise ValueError("runID value must be less than 64 characters")
        return value

    @validator("owner_id", pre=True, always=True)
    def validate_ownerid(cls, value):
        """Set the owner_id element if one was provided, otherwise set the element to nil"""
        return validate_nillable(value, str)

    @validator("quote", pre=True, always=True)
    def validate_quote(cls, value):
        """Set the quote element if one was provided, otherwise set the element to nil"""
        return validate_nillable(value, str)

    @validator("start_time", pre=True, always=True)
    def validate_starttime(cls, value):
        """Set the start_time element to nil at creation -
        it is expected to be there even if the job has not yet started"""
        # the VODateTime object is serialized/deserialized as its ISO formatted string
        return validate_nillable(value, str)

    @validator("end_time", pre=True, always=True)
    def validate_endtime(cls, value):
        """Set the end_time element to nil at creation -
        it is expected to be there even if the job has not yet started"""
        # the VODateTime object is serialized/deserialized as its ISO formatted string
        return validate_nillable(value, str)


class Job(BaseXmlModel, tag="job", ns="uws", nsmap=NSMAP):
    """The root element for a JobSummary response.

    Used to wrap the JobSummary element in an element of type <{uws}:job>
    """

    __root__: JobSummary


class Jobs(BaseXmlModel, tag="jobs", ns="uws", nsmap=NSMAP):
    """The root element for a Job List response

    Used to wrap a list of ShortJobDescription elements in a <{uws}:jobs> tag

    Attributes:
        version: the UWS service version
    Elements:
        The list of ShortJobDescription elements, each having <{uws}:jobref> tag
    """

    version: UWSVersions = attr(default=UWSVersions.V1_1)
    jobref: list[ShortJobDescription] = element(tag="jobref", default_factory=lambda: [])
