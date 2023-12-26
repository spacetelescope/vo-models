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

print(error_summary.to_xml())
# [error-summary-model-end]

# [error-summary-xml-start]
error_summary_xml = """
<uws:errorSummary
    xmlns:uws="http://www.ivoa.net/xml/UWS/v1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    type="fatal" hasDetail="true">
    <uws:message>The job failed because of a missing parameter.</uws:message>
</uws:errorSummary>
"""
# [error-summary-xml-end]
