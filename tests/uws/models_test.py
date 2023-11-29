"""Tests for the XML serialization of UWS elements"""

from datetime import timezone as tz
from typing import Optional
from unittest import TestCase

from lxml import etree
from pydantic_xml import element

from vo.models.xml.generics import VODateTime
from vo.models.xml.uws import (
    ErrorSummary,
    Jobs,
    JobSummary,
    Parameter,
    Parameters,
    ResultReference,
    Results,
    ShortJobDescription,
)
from vo.models.xml.uws.types import ExecutionPhase

UWS_NAMESPACE_HEADER = """xmlns:uws="http://www.ivoa.net/xml/UWS/v1.0"
xmlns:xlink="http://www.w3.org/1999/xlink"
xmlns:xsd="http://www.w3.org/2001/XMLSchema"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
"""

# New schema versions can be downloaded from https://www.ivoa.net/xml/ under "UWS - Universal Worker Service"
# The most current version is 1.1, found here: https://www.ivoa.net/xml/UWS/UWS-v1.1.xsd
with open("tests/uws/UWS-Schema-V1.0.xsd", "r") as schema_file:
    uws_schema = etree.XMLSchema(etree.parse(schema_file))


class TestErrorSummaryType(TestCase):
    """Tests for the UWS errorSummary complex type"""

    test_error_summary_xml = f"""<uws:errorSummary {UWS_NAMESPACE_HEADER}
    type="transient"
    hasDetail="true">
    <uws:message>Invalid query.</uws:message>
    </uws:errorSummary>
    """

    def test_read_from_xml(self):
        """Test reading from XML"""

        error_summary = ErrorSummary.from_xml(self.test_error_summary_xml)
        self.assertEqual(error_summary.type, "transient")
        self.assertEqual(error_summary.has_detail, True)
        self.assertEqual(error_summary.message, "Invalid query.")

    def test_write_to_xml(self):
        """Test writing to XML"""

        error_summary = ErrorSummary(type="transient", has_detail=True, message="Invalid query.")
        error_summary_xml = error_summary.to_xml(encoding=str)
        self.assertIn('type="transient"', error_summary_xml)
        self.assertIn('hasDetail="true"', error_summary_xml)
        self.assertIn("<uws:message>Invalid query.</uws:message>", error_summary_xml)


class TestParameterType(TestCase):
    """Tests for the UWS Parameter complex type"""

    test_parameter_xml = (
        f'<uws:parameter {UWS_NAMESPACE_HEADER} byReference="false" id="param1" isPost="false">'
        "test_value"
        "</uws:parameter>"
    )

    def test_read_from_xml(self):
        """Test reading from XML"""

        parameter = Parameter.from_xml(self.test_parameter_xml)
        self.assertEqual(parameter.by_reference, False)
        self.assertEqual(parameter.id, "param1")
        self.assertEqual(parameter.is_post, False)
        self.assertEqual(parameter.value, "test_value")

    def test_write_to_xml(self):
        """Test writing to XML"""

        parameter = Parameter(by_reference=False, id="param1", is_post=False, value="test_value")
        parameter_xml = parameter.to_xml(encoding=str)
        self.assertIn('byReference="false"', parameter_xml)
        self.assertIn('id="param1"', parameter_xml)
        self.assertIn('isPost="false"', parameter_xml)
        self.assertIn("test_value", parameter_xml)


class TestResultReferenceType(TestCase):
    """Test the UWS ResultReference complex type"""

    test_result_reference_xml = (
        f"<uws:result {UWS_NAMESPACE_HEADER} "
        'id="result1" mime-type="text/xml" '
        'xlink:href="http://testlink.com/" '
        'size="1234" '
        'xlink:type="simple" />'
    )

    def test_read_from_xml(self):
        """Test reading from XML"""

        result_reference = ResultReference.from_xml(self.test_result_reference_xml)
        self.assertEqual(result_reference.id, "result1")
        self.assertEqual(result_reference.mime_type, "text/xml")
        self.assertEqual(result_reference.href, "http://testlink.com/")
        self.assertEqual(result_reference.type, "simple")
        self.assertEqual(result_reference.size, 1234)

    def test_write_to_xml(self):
        """Test writing to XML"""

        result_reference = ResultReference(
            id="result1",
            mime_type="text/xml",
            href="http://testlink.com/",
            type="simple",
            size=1234,
        )
        result_reference_xml = result_reference.to_xml(encoding=str)
        self.assertIn('id="result1"', result_reference_xml)
        self.assertIn('mime-type="text/xml"', result_reference_xml)
        self.assertIn('xlink:href="http://testlink.com/"', result_reference_xml)
        self.assertIn('xlink:type="simple"', result_reference_xml)
        self.assertIn('size="1234"', result_reference_xml)


class TestResultsElement(TestCase):
    """Test the results list element"""

    test_results_xml = (
        f"<uws:results {UWS_NAMESPACE_HEADER} >"
        "<uws:result id='result1' mime-type='text/xml' xlink:href='http://testlink.com/' />"
        "<uws:result id='result2' mime-type='text/xml' xlink:href='http://testlink.com/' />"
        "</uws:results>"
    )

    def test_read_from_xml(self):
        """Test reading from XML"""

        results = Results.from_xml(self.test_results_xml)
        self.assertEqual(len(results.results), 2)
        self.assertEqual(results.results[0].id, "result1")
        self.assertEqual(results.results[1].id, "result2")

    def test_write_to_xml(self):
        """Test writing to XML"""

        results_list = Results(
            results=[
                ResultReference(
                    id="result1",
                    mime_type="text/xml",
                    href="http://testlink.com/",
                ),
                ResultReference(
                    id="result2",
                    mime_type="text/xml",
                    href="http://testlink.com/",
                ),
            ]
        )
        results_xml = results_list.to_xml(encoding=str, skip_empty=True)
        self.assertIn('id="result1"', results_xml)
        self.assertIn('id="result2"', results_xml)

    def test_validate(self):
        """Test validation against XML schema"""

        results = Results(
            results=[
                ResultReference(
                    id="result1",
                    mime_type="text/xml",
                    href="http://testlink.com/",
                ),
                ResultReference(
                    id="result2",
                    mime_type="text/xml",
                    href="http://testlink.com/",
                ),
            ]
        )
        results_xml = etree.fromstring(results.to_xml(encoding=str, skip_empty=True))
        uws_schema.assertValid(results_xml)


class TestShortJobDescriptionType(TestCase):
    """Test the UWS ShortJobDescription complex type"""

    test_short_job_description_xml = (
        f'<uws:jobref {UWS_NAMESPACE_HEADER} id="id1" xlink:type="simple" xlink:href="http://uri1">'
        "<uws:phase>PENDING</uws:phase>"
        "<uws:runId>runId1</uws:runId>"
        "<uws:creationTime>1900-01-01T01:01:01Z</uws:creationTime>"
        "</uws:jobref>"
    )

    def test_read_from_xml(self):
        """Test reading from XML"""

        short_job_description = ShortJobDescription.from_xml(self.test_short_job_description_xml)
        self.assertEqual(short_job_description.job_id, "id1")
        self.assertEqual(short_job_description.type, "simple")
        self.assertEqual(short_job_description.href, "http://uri1")
        self.assertEqual(short_job_description.phase, "PENDING")
        self.assertEqual(short_job_description.run_id, "runId1")
        self.assertEqual(short_job_description.owner_id.value, None)
        self.assertEqual(short_job_description.creation_time, VODateTime(1900, 1, 1, 1, 1, 1, tzinfo=tz.utc))

    def test_write_to_xml(self):
        """Test writing to XML"""

        short_job_description = ShortJobDescription(
            job_id="id1",
            owner_id=None,
            type="simple",
            href="http://uri1",
            phase="PENDING",
            run_id="runId1",
            creation_time=VODateTime(1900, 1, 1, 1, 1, 1, tzinfo=tz.utc),
        )
        short_job_description_xml = short_job_description.to_xml(skip_empty=True, encoding=str)
        self.assertIn('id="id1"', short_job_description_xml)
        self.assertIn('<uws:ownerId xsi:nil="true"/>', short_job_description_xml)
        self.assertIn('xlink:type="simple"', short_job_description_xml)
        self.assertIn('xlink:href="http://uri1"', short_job_description_xml)
        self.assertIn("<uws:phase>PENDING</uws:phase>", short_job_description_xml)
        self.assertIn("<uws:runId>runId1</uws:runId>", short_job_description_xml)
        self.assertIn("<uws:creationTime>1900-01-01T01:01:01.000Z</uws:creationTime>", short_job_description_xml)


class TestGenericParametersElement(TestCase):
    """Test the generic UWS Parameters element"""

    class TestParameters(Parameters):
        """A test generic Parameters class"""

        param1: Optional[Parameter] = element(tag="parameter")
        param2: Optional[Parameter] = element(tag="parameter")
        param3: Optional[Parameter] = element(tag="parameter")

    test_parameters_xml = (
        f"<uws:parameters {UWS_NAMESPACE_HEADER}>"
        '<uws:parameter id="param1" type="xs:string">value1</uws:parameter>'
        '<uws:parameter id="param2" type="xs:string">value2</uws:parameter>'
        '<uws:parameter id="param3" type="xs:string">value3</uws:parameter>'
        "</uws:parameters>"
    )

    def test_base_parameters(self):
        """Test the base Parameters element - no subclass"""

        parameters = Parameters(
            parameter=[
                Parameter(id="param1", type="xs:string", value="value1"),
                Parameter(id="param2", type="xs:string", value="value2"),
                Parameter(id="param3", type="xs:string", value="value3"),
            ]
        )
        # pylint: disable=no-member
        parameter_values = [param.value for param in parameters.parameter]
        self.assertEqual(parameter_values, ["value1", "value2", "value3"])

    def test_read_from_dict(self):
        """Test reading base Parameters from dict"""

        # Occurs when reading from cache
        param_dict = {
            "param1": {"id": "param1", "type": "xs:string", "value": "value1"},
            "param2": {"id": "param2", "type": "xs:string", "value": "value2"},
            "param3": {"id": "param3", "type": "xs:string", "value": "value3"},
        }
        # pylint: disable=no-member
        parameters = Parameters(**param_dict)
        self.assertEqual(parameters.param1.value, "value1")
        self.assertEqual(parameters.param2.value, "value2")
        self.assertEqual(parameters.param3.value, "value3")

    def test_read_from_xml(self):
        """Test reading from XML"""

        parameters = self.TestParameters.from_xml(self.test_parameters_xml)
        self.assertEqual(len(parameters.dict()), 3)

        self.assertEqual(parameters.param1.id, "param1")
        self.assertEqual(parameters.param2.id, "param2")
        self.assertEqual(parameters.param3.id, "param3")

        self.assertEqual(parameters.param1.value, "value1")
        self.assertEqual(parameters.param2.value, "value2")
        self.assertEqual(parameters.param3.value, "value3")

    def test_write_to_xml(self):
        """Test writing to XML"""

        parameters = self.TestParameters(
            param1=Parameter(id="param1", type="xs:string", value="value1"),
            param2=Parameter(id="param2", type="xs:string", value="value2"),
            param3=Parameter(id="param3", type="xs:string", value="value3"),
        )
        parameters_xml = parameters.to_xml(skip_empty=True, encoding=str)
        self.assertIn('id="param1"', parameters_xml)
        self.assertIn('id="param2"', parameters_xml)
        self.assertIn('id="param3"', parameters_xml)

        self.assertIn("value1", parameters_xml)
        self.assertIn("value2", parameters_xml)
        self.assertIn("value3", parameters_xml)

    def test_validate(self):
        """Test validation against XML schema"""

        parameters = self.TestParameters(
            param1=Parameter(id="param1", type="xs:string", value="value1"),
            param2=Parameter(id="param2", type="xs:string", value="value2"),
            param3=Parameter(id="param3", type="xs:string", value="value3"),
        )
        parameters_xml = etree.fromstring(parameters.to_xml(skip_empty=True, encoding=str))
        uws_schema.assertValid(parameters_xml)


class TestJobSummaryElement(TestCase):
    """Test the UWS JobSummary element"""

    class TestParameters(Parameters):
        """A test generic Parameters class"""

        param1: Optional[Parameter] = element(tag="parameter")
        param2: Optional[Parameter] = element(tag="parameter")

    job_summary_xml = (
        f'<uws:job {UWS_NAMESPACE_HEADER} version="1.1">'
        "<uws:jobId>jobId1</uws:jobId>"
        "<uws:runId>runId1</uws:runId>"
        "<uws:ownerId>ownerId1</uws:ownerId>"
        "<uws:phase>PENDING</uws:phase>"
        '<uws:quote xsi:nil="true" />'
        "<uws:creationTime>1900-01-01T01:01:01.000Z</uws:creationTime>"
        "<uws:startTime>1900-01-01T01:01:01.000Z</uws:startTime>"
        "<uws:endTime>1900-01-01T01:01:01.000Z</uws:endTime>"
        "<uws:executionDuration>0</uws:executionDuration>"
        "<uws:destruction>1900-01-01T01:01:01.000Z</uws:destruction>"
        "<uws:parameters>"
        '<uws:parameter id="param1">value1</uws:parameter>'
        '<uws:parameter id="param2">value2</uws:parameter>'
        "</uws:parameters>"
        "<uws:results />"
        "<uws:errorSummary />"
        "<uws:jobInfo>jobInfo1</uws:jobInfo>"
        "</uws:job>"
    )

    def test_read_from_xml(self):
        """Test reading from XML"""

        job_summary = JobSummary[self.TestParameters].from_xml(self.job_summary_xml)
        self.assertEqual(job_summary.job_id, "jobId1")
        self.assertEqual(job_summary.run_id, "runId1")
        self.assertEqual(job_summary.owner_id.value, "ownerId1")
        self.assertEqual(job_summary.phase, ExecutionPhase.PENDING.value)
        self.assertEqual(job_summary.quote.value, None)
        self.assertEqual(job_summary.creation_time, VODateTime(1900, 1, 1, 1, 1, 1, tzinfo=tz.utc))
        self.assertEqual(job_summary.start_time.value, VODateTime(1900, 1, 1, 1, 1, 1, tzinfo=tz.utc).isoformat())
        self.assertEqual(job_summary.end_time.value, VODateTime(1900, 1, 1, 1, 1, 1, tzinfo=tz.utc).isoformat())
        self.assertEqual(job_summary.execution_duration, 0)
        self.assertEqual(job_summary.destruction, VODateTime(1900, 1, 1, 1, 1, 1, tzinfo=tz.utc))
        self.assertEqual(len(job_summary.parameters.dict()), 2)
        self.assertEqual(job_summary.parameters.param1.id, "param1")
        self.assertEqual(job_summary.parameters.param2.id, "param2")
        self.assertEqual(job_summary.parameters.param1.value, "value1")
        self.assertEqual(job_summary.parameters.param2.value, "value2")
        self.assertEqual(len(job_summary.results.results), 0)
        self.assertEqual(job_summary.error_summary.message, "")
        self.assertEqual(job_summary.job_info[0], "jobInfo1")

    def test_write_to_xml(self):
        """Test writing to XML"""

        job_summary = JobSummary[self.TestParameters](
            job_id="jobId1",
            run_id="runId1",
            owner_id="ownerId1",
            phase=ExecutionPhase.PENDING,
            quote=None,
            creation_time=VODateTime(1900, 1, 1, 1, 1, 1, tzinfo=tz.utc),
            start_time=None,
            end_time=None,
            execution_duration=0,
            destruction=VODateTime(1900, 1, 1, 1, 1, 1, tzinfo=tz.utc),
            parameters=self.TestParameters(
                param1=Parameter(id="param1", type="xs:string", value="value1"),
                param2=Parameter(id="param2", type="xs:string", value="value2"),
            ),
            results=Results(),
            error_summary=ErrorSummary(),
            job_info=["jobInfo1"],
        )
        job_summary_xml = job_summary.to_xml(skip_empty=True, encoding=str)
        self.assertIn("jobId1", job_summary_xml)
        self.assertIn("runId1", job_summary_xml)
        self.assertIn("ownerId1", job_summary_xml)
        self.assertIn("PENDING", job_summary_xml)
        self.assertIn("1900-01-01T01:01:01.000Z", job_summary_xml)
        self.assertIn("1900-01-01T01:01:01.000Z", job_summary_xml)
        self.assertIn("1900-01-01T01:01:01.000Z", job_summary_xml)
        self.assertIn("1900-01-01T01:01:01.000Z", job_summary_xml)
        self.assertIn("value1", job_summary_xml)
        self.assertIn("value2", job_summary_xml)
        self.assertIn("jobInfo1", job_summary_xml)

    def test_validate(self):
        """Validate against the schema"""

        job_summary = JobSummary[self.TestParameters](
            job_id="jobId1",
            run_id="runId1",
            owner_id="ownerId1",
            phase=ExecutionPhase.PENDING,
            quote=None,
            creation_time=VODateTime(1900, 1, 1, 1, 1, 1, tzinfo=tz.utc),
            start_time=None,
            end_time=None,
            execution_duration=0,
            destruction=VODateTime(1900, 1, 1, 1, 1, 1, tzinfo=tz.utc),
            parameters=self.TestParameters(
                param1=Parameter(id="param1", value="value1"),
                param2=Parameter(id="param2", value="value2"),
            ),
            results=Results(results=[ResultReference(id="result1")]),
            error_summary=None,
        )
        job_summary_xml = etree.fromstring(job_summary.to_xml(skip_empty=True, encoding=str))
        uws_schema.assertValid(job_summary_xml)


class TestJobsElement(TestCase):
    """Test the UWS Jobs element"""

    test_job_list_xml = (
        f'<uws:jobs {UWS_NAMESPACE_HEADER} version="1.1">'
        '<uws:jobref id="id1" xlink:type="simple" xlink:href="http://uri1">'
        "<uws:phase>PENDING</uws:phase>"
        '<uws:ownerId xsi:nil="true" />'
        "<uws:creationTime>1900-01-01T01:01:01Z</uws:creationTime>"
        "</uws:jobref>"
        "</uws:jobs>"
    )

    def test_read_from_xml(self):
        """Test reading from XML"""

        jobs_element = Jobs.from_xml(self.test_job_list_xml)
        self.assertEqual(len(jobs_element.jobref), 1)
        self.assertEqual(jobs_element.jobref[0].job_id, "id1")
        self.assertEqual(jobs_element.jobref[0].owner_id.value, None)
        self.assertEqual(jobs_element.jobref[0].phase, ExecutionPhase.PENDING)
        self.assertEqual(jobs_element.jobref[0].creation_time, VODateTime(1900, 1, 1, 1, 1, 1, tzinfo=tz.utc))

    def test_write_to_xml(self):
        """Test writing to XML"""

        jobs_element = Jobs(
            jobref=[
                ShortJobDescription(
                    job_id="id1",
                    phase=ExecutionPhase.PENDING,
                    creation_time=VODateTime(1900, 1, 1, 1, 1, 1, tzinfo=tz.utc),
                )
            ]
        )
        jobs_element_xml = jobs_element.to_xml(skip_empty=True, encoding=str)
        self.assertIn("id1", jobs_element_xml)
        self.assertIn("PENDING", jobs_element_xml)
        self.assertIn("1900-01-01T01:01:01.000Z", jobs_element_xml)

    def test_validate(self):
        """Validate against the schema"""

        jobs_element = Jobs(
            jobref=[
                ShortJobDescription(
                    job_id="id1",
                    phase=ExecutionPhase.PENDING,
                    creation_time=VODateTime(1900, 1, 1, 1, 1, 1, tzinfo=tz.utc),
                )
            ]
        )
        jobs_element_xml = etree.fromstring(jobs_element.to_xml(skip_empty=True, encoding=str))
        uws_schema.assertValid(jobs_element_xml)
