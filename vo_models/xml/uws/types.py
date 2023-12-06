"""UWS Simple Types"""

from enum import Enum

from pydantic_xml import RootXmlModel


class ErrorType(str, Enum):
    """Enum for error types."""

    TRANSIENT = "transient"
    FATAL = "fatal"

class UWSVersion(str, Enum):
    """The version of the UWS standard that the server complies with."""

    V1_1 = "1.1"
    V1_0 = "1.0"

class ExecutionPhase(str, Enum):
    """Enumeration of possible phases of job execution

    PENDING:    The first phase a job is entered into - this is where a job is being set up but no request to run
                has occurred.
    QUEUED:     A job has been accepted for execution but is waiting in a queue.
    EXECUTING:  A job is running
    COMPLETED:  A job has completed successfully.
    ERROR:      Some form of error has occurred.
    UNKNOWN:    The job is in an unknown state.
    HELD:       The job is HELD pending execution and will not automatically be executed - can occur after a
                PHASE=RUN request has been made (cf PENDING).
    SUSPENDED:  The job has been suspended by the system during execution.
    ABORTED:    The job has been aborted, either by user request or by the server because of lack or overuse of
                resources.
    ARCHIVED:   The job has been archived by the server at destruction time. An archived job
                may have deleted the results to reclaim resources, but must have job metadata preserved.
                This is an alternative that the server may choose in contrast to completely destroying
                all record of the job.
    """
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"
    HELD = "HELD"
    SUSPENDED = "SUSPENDED"
    ABORTED = "ABORTED"
    ARCHIVED = "ARCHIVED"
