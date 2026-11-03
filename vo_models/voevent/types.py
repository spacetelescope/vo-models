"""Simple Types used in VOEvent Models."""

from enum import Enum


class RoleValues(str, Enum):
    """Enumeration of the possible roles of a VOEvent packet."""

    OBSERVATION = "observation"
    PREDICTION = "prediction"
    UTILITY = "utility"
    TEST = "test"


class DataType(str, Enum):
    """Enumeration of the possible data types for a Param."""

    STRING = "string"
    INT = "int"
    FLOAT = "float"


class CiteValues(str, Enum):
    """Enumeration of the possible citation types for a VOEvent packet."""

    FOLLOW_UP = "followup"
    SUPERSEDES = "supersedes"
    RETRACTION = "retraction"


class ContributorRole(str, Enum):
    """The list of contributor roles is extracted from the DataCite Schema v4.5."""

    CONTACT_PERSON = "ContactPerson"
    DATA_COLLECTOR = "DataCollector"
    DATA_CURATOR = "DataCurator"
    DATA_MANAGER = "DataManager"
    DISTRIBUTOR = "Distributor"
    EDITOR = "Editor"
    HOSTING_INSTITUTION = "HostingInstitution"
    PRODUCER = "Producer"
    PROJECT_LEADER = "ProjectLeader"
    PROJECT_MANAGER = "ProjectManager"
    PROJECT_MEMBER = "ProjectMember"
    REGISTRATION_AGENCY = "RegistrationAgency"
    REGISTRATION_AUTHORITY = "RegistrationAuthority"
    RELATED_PERSON = "RelatedPerson"
    RESEARCHER = "Researcher"
    RESEARCH_GROUP = "ResearchGroup"
    RIGHTS_HOLDER = "RightsHolder"
    SPONSOR = "Sponsor"
    SUPERVISOR = "Supervisor"
    WORK_PACKAGE_LEADER = "WorkPackageLeader"
    OTHER = "Other"
