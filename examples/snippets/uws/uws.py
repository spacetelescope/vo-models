import datetime

from vo_models.uws import (
    ErrorSummary,
    Jobs,
    JobSummary,
    Parameter,
    Parameters,
    ResultReference,
    Results,
    ShortJobDescription,
)

# [error-summary-model-start]
error_summary = ErrorSummary(
    type="fatal",
    has_detail=True,
    message="The job failed because of a missing parameter.",
)

error_summary.to_xml()
# [error-summary-model-end]

# [error-summary-xml-start]
error_summary_xml = """
<uws:errorSummary
    type="fatal" hasDetail="true">
<uws:message>The job failed because of a missing parameter.</uws:message>
</uws:errorSummary>
"""  # [error-summary-xml-end]

# [parameter-model-start]
parameter = Parameter(
    id="lang",
    value="ADQL",
    is_post=False,
    by_reference=False,
)

parameter.to_xml()
# [parameter-model-end]

# [parameter-xml-start]
parameter_xml = """
<uws:parameter byReference="false" id="lang" isPost="false">
    ADQL
</uws:parameter>
"""  # [parameter-xml-end]


# [parameters-model-start]
class TAPParameters(Parameters):
    lang: Parameter = Parameter(id="lang")
    query: Parameter = Parameter(id="query")
    maxrec: Parameter = Parameter(id="maxrec")
    format: Parameter = Parameter(id="format")


parameters = TAPParameters(
    lang=Parameter(value="ADQL", id="lang"),
    query=Parameter(value="SELECT * FROM ivoa.obscore", id="query"),
    maxrec=Parameter(value=10, id="maxrec"),
    format=Parameter(value="votable", id="format"),
)
parameters.to_xml()
# [parameters-model-end]

# [parameters-xml-start]
parameters_xml = """
<uws:parameters>
    <uws:parameter byReference="false" id="lang" isPost="false">ADQL</uws:parameter>
    <uws:parameter byReference="false" id="query" isPost="false">SELECT * FROM ivoa.obscore</uws:parameter>
    <uws:parameter byReference="false" id="maxrec" isPost="false">10</uws:parameter>
    <uws:parameter byReference="false" id="format" isPost="false">votable</uws:parameter>
</uws:parameters>
"""  # [parameters-xml-end]

# [result-reference-model-start]
result_reference = ResultReference(
    id="result",
    href="http://example.com/result",
)

result_reference.to_xml()
# [result-reference-model-end]

# [result-reference-xml-start]
result_reference_xml = """
<uws:result
    id="result"
    xlink:type="simple"
    xlink:href="http://example.com/result"/>
"""  # [result-reference-xml-end]

# [results-model-start]
results = Results(
    results=[
        ResultReference(id="result1", href="http://example.com/result1"),
        ResultReference(id="result2", href="http://example.com/result2"),
    ],
)

results.to_xml()
# [results-model-end]

# [results-xml-start]
results_xml = """
<uws:results>
    <uws:result id="result1" xlink:type="simple" xlink:href="http://example.com/result1"/>
    <uws:result id="result2" xlink:type="simple" xlink:href="http://example.com/result2"/>
</uws:results>
"""  # [results-xml-end]

# [short-job-description-model-start]
short_job_description = ShortJobDescription(
    phase="PENDING",
    run_id="1234567890",
    owner_id="anon_user",
    creation_time=datetime.datetime.now(),
    job_id="job_1",
)

short_job_description.to_xml()
# [short-job-description-model-end]

# [short-job-description-xml-start]
short_job_description_xml = """
<uws:jobref id="job_1" xlink:type="simple" xlink:href="">
    <uws:phase>PENDING</uws:phase>
    <uws:runId>1234567890</uws:runId>
    <uws:ownerId>anon_user</uws:ownerId>
    <uws:creationTime>2023-12-27T12:19:46.889Z</uws:creationTime>
</uws:jobref>
"""  # [short-job-description-xml-end]

# [jobs-model-start]
jobs = Jobs(
    jobref=[
        ShortJobDescription(
            phase="PENDING",
            run_id="1234567890",
            owner_id="anon_user",
            job_id="job_1",
        ),
        ShortJobDescription(
            phase="COMPLETED",
            run_id="1234567891",
            owner_id="anon_user",
            job_id="job_2",
        ),
    ],
)

jobs.to_xml()
# [jobs-model-end]

# [jobs-xml-start]
jobs_xml = """
<uws:jobs>
    <uws:jobref id="job_1" xlink:type="simple" xlink:href="">
        <uws:phase>PENDING</uws:phase>
        <uws:runId>1234567890</uws:runId>
        <uws:ownerId>anon_user</uws:ownerId>
        <uws:creationTime></uws:creationTime>
    </uws:jobref>
    <uws:jobref id="job_2" xlink:type="simple" xlink:href="">
        <uws:phase>COMPLETED</uws:phase>
        <uws:runId>1234567891</uws:runId>
        <uws:ownerId>anon_user</uws:ownerId>
        <uws:creationTime></uws:creationTime>
    </uws:jobref>
</uws:jobs>
"""  # [jobs-xml-end]

# [job-summary-model-start]
parameters = TAPParameters(
    lang=Parameter(value="ADQL", id="lang"),
    query=Parameter(value="SELECT * FROM ivoa.obscore", id="query"),
    maxrec=Parameter(value=10, id="maxrec"),
    format=Parameter(value="votable", id="format"),
)

job_summary = JobSummary[TAPParameters](
    job_id = "job_1",
    owner_id = "anon_user",
    phase = "COMPLETED",
    creation_time = "2023-12-01T12:00:00.000Z",
    start_time = "2023-12-01T12:00:00.000Z",
    end_time = datetime.datetime.now(),
    parameters = parameters,
    results = Results(
        results=[
            ResultReference(id="result1", href="http://example.com/result1"),
            ResultReference(id="result2", href="http://example.com/result2"),
        ],
    ),
)

job_summary.to_xml()
# [job-summary-model-end]

# [job-summary-xml-start]
job_summary_xml = """
<uws:job xmlns:uws="http://www.ivoa.net/xml/UWS/v1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    version="1.1">
    <uws:jobId>job_1</uws:jobId>
    <uws:runId></uws:runId>
    <uws:ownerId>anon_user</uws:ownerId>
    <uws:phase>COMPLETED</uws:phase>
    <uws:quote xsi:nil="true"></uws:quote>
    <uws:creationTime>2023-12-01T12:00:00.000Z</uws:creationTime>
    <uws:startTime>2023-12-01T12:00:00.000Z</uws:startTime>
    <uws:endTime>2023-12-27T12:47:37.196Z</uws:endTime>
    <uws:executionDuration>0</uws:executionDuration>
    <uws:destruction xsi:nil="true"></uws:destruction>
    <uws:parameters>
        <uws:parameter byReference="false" id="lang" isPost="false">ADQL</uws:parameter>
        <uws:parameter byReference="false" id="query" isPost="false">SELECT * FROM ivoa.obscore</uws:parameter>
        <uws:parameter byReference="false" id="maxrec" isPost="false">10</uws:parameter>
        <uws:parameter byReference="false" id="format" isPost="false">votable</uws:parameter>
    </uws:parameters>
    <uws:results>
        <uws:result id="result1" xlink:type="simple" xlink:href="http://example.com/result1"/>
        <uws:result id="result2" xlink:type="simple" xlink:href="http://example.com/result2"/>
    </uws:results>
</uws:job>
"""  # [job-summary-xml-end]