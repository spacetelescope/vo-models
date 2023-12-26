"""UWS Simple Types"""

from enum import Enum


class ErrorType(str, Enum):
    """Enum for error types."""

    TRANSIENT = "transient"
    """The error is transient and the job may be rerun."""
    FATAL = "fatal"
    """The error is fatal and the job may not be rerun."""


class UWSVersion(str, Enum):
    """The version of the UWS standard that the server complies with."""

    V1_1 = "1.1"
    """The server complies with UWS 1.1."""
    V1_0 = "1.0"
    """The server complies with UWS 1.0."""


class ExecutionPhase(str, Enum):
    """Enumeration of possible phases of job execution."""

    PENDING = "PENDING"
    """
    The first phase a job is entered into - this is where a job is being set up but no request to run has occurred.
    """
    QUEUED = "QUEUED"
    """
    A job has been accepted for execution but is waiting in a queue.
    """
    EXECUTING = "EXECUTING"
    """
    A job is running
    """
    COMPLETED = "COMPLETED"
    """
    A job has completed successfully.
    """
    ERROR = "ERROR"
    """
    Some form of error has occurred.
    """
    UNKNOWN = "UNKNOWN"
    """
    The job is in an unknown state.
    """
    HELD = "HELD"
    """
    The job is HELD pending execution and will not automatically be executed.
    Can occur after a PHASE=RUN request has been made (cf PENDING).
    """
    SUSPENDED = "SUSPENDED"
    """
    The job has been suspended by the system during execution.
    """
    ABORTED = "ABORTED"
    """
    The job has been aborted, either by user request or by the server because of lack or overuse of resources.
    """
    ARCHIVED = "ARCHIVED"
    """
    The job has been archived by the server at destruction time. An archived job may have deleted the results to reclaim
    resources, but must have job metadata preserved. This is an alternative that the server may choose in contrast to
    completely destroying all record of the job.
    """
