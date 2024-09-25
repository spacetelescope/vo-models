"""Tests for TAPRegExt models."""

from unittest import TestCase
from xml.etree.ElementTree import canonicalize

from lxml import etree

from vo_models.tapregext.models import (
    DataLimit,
    DataLimits,
    DataModelType,
    Language,
    LanguageFeature,
    LanguageFeatureList,
    OutputFormat,
    TableAccess,
    TimeLimits,
    UploadMethod,
    Version,
)

TAPREGEXT_NAMESPACE_HEADER = """xmlns:xs="http://www.w3.org/2001/XMLSchema"
xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0"
xmlns:vm="http://www.ivoa.net/xml/VOMetadata/v0.1"
xmlns="http://www.ivoa.net/xml/TAPRegExt/v1.0"
"""

with open("tests/tapregext/TAPRegExt-v1.0-with-erratum1.xsd") as schema_file:
    tapregext_schema = etree.XMLSchema(etree.parse(schema_file))


class TestVersion(TestCase):
    """Tests the Version model."""

    test_version_model = Version(value="1.0", ivo_id="ivo://ivoa.net/std/TAP")
    test_version_xml = f'<Version {TAPREGEXT_NAMESPACE_HEADER} ivo-id="ivo://ivoa.net/std/TAP">1.0</Version>'

    def test_read_from_xml(self):
        """Test reading a Version element from XML."""
        version = Version.from_xml(self.test_version_xml)
        self.assertEqual(version.value, "1.0")
        self.assertEqual(version.ivo_id, "ivo://ivoa.net/std/TAP")

    def test_write_xml(self):
        """Test we can write a Version element to XML."""
        test_xml = self.test_version_model.to_xml(encoding=str, skip_empty=True)
        (
            self.assertEqual(
                canonicalize(test_xml),
                canonicalize(self.test_version_xml),
            ),
        )


class TestLanguageFeature(TestCase):
    """Tests the LanguageFeature model."""

    test_language_feature_model = LanguageFeature(form="Formal notation", description="A description")
    test_language_feature_xml = f"<LanguageFeature {TAPREGEXT_NAMESPACE_HEADER}><form>Formal notation</form><description>A description</description></LanguageFeature>"

    def test_read_from_xml(self):
        """Test reading a LanguageFeature element from XML."""
        language_feature = LanguageFeature.from_xml(self.test_language_feature_xml)
        self.assertEqual(language_feature.form, "Formal notation")
        self.assertEqual(language_feature.description, "A description")

    def test_write_xml(self):
        """Test we can write a LanguageFeature element to XML."""
        test_xml = self.test_language_feature_model.to_xml(encoding=str, skip_empty=True)
        self.assertEqual(
            canonicalize(test_xml),
            canonicalize(self.test_language_feature_xml),
        )


class TestOutputFormat(TestCase):
    """Tests the OutputFormat model."""

    test_output_format_model = OutputFormat(
        mime="application/x-votable+xml",
        alias=["VOTABLE"],
    )
    test_output_format_xml = (
        f"<OutputFormat {TAPREGEXT_NAMESPACE_HEADER}>"
        "<mime>application/x-votable+xml</mime>"
        "<alias>VOTABLE</alias>"
        "</OutputFormat>"
    )

    def test_read_from_xml(self):
        """Test reading an OutputFormat element from XML."""
        output_format = OutputFormat.from_xml(self.test_output_format_xml)
        self.assertEqual(output_format.mime, "application/x-votable+xml")
        self.assertEqual(output_format.alias[0], "VOTABLE")

    def test_write_xml(self):
        """Test we can write an OutputFormat element to XML."""
        output_format_xml = self.test_output_format_model.to_xml(encoding=str, skip_empty=True)
        self.assertEqual(
            canonicalize(etree.tostring(etree.fromstring(self.test_output_format_xml))),
            canonicalize(
                etree.tostring(etree.fromstring(output_format_xml)),
            ),
        )


class TestUploadMethod(TestCase):
    """Tests the UploadMethod model."""

    test_upload_method_model = UploadMethod(
        ivo_id="ivo://ivoa.net/std/TAP",
    )
    test_upload_method_xml = f'<UploadMethod {TAPREGEXT_NAMESPACE_HEADER} ivo-id="ivo://ivoa.net/std/TAP"/>'

    def test_read_from_xml(self):
        """Test reading an UploadMethod element from XML."""
        upload_method = UploadMethod.from_xml(self.test_upload_method_xml)
        self.assertEqual(upload_method.ivo_id, "ivo://ivoa.net/std/TAP")

    def test_write_xml(self):
        """Test we can write an UploadMethod element to XML."""
        test_xml = self.test_upload_method_model.to_xml(encoding=str, skip_empty=True)
        self.assertEqual(
            canonicalize(self.test_upload_method_xml),
            canonicalize(test_xml),
        )


class TestTimeLimits(TestCase):
    """Tests the TimeLimits model."""

    test_time_limits_model = TimeLimits(default=10, hard=100)
    test_time_limits_xml = (
        f"<TimeLimits {TAPREGEXT_NAMESPACE_HEADER}><default>10</default><hard>100</hard></TimeLimits>"
    )

    def test_read_from_xml(self):
        """Test reading a TimeLimits element from XML."""
        time_limits = TimeLimits.from_xml(self.test_time_limits_xml)
        self.assertEqual(time_limits.default, 10)
        self.assertEqual(time_limits.hard, 100)

    def test_write_xml(self):
        """Test we can write a TimeLimits element to XML."""
        test_xml = self.test_time_limits_model.to_xml(encoding=str, skip_empty=True)
        self.assertEqual(
            canonicalize(test_xml),
            canonicalize(self.test_time_limits_xml),
        )


class TestDataLimits(TestCase):
    """Tests the DataLimits model."""

    test_data_limits_model = DataLimits(
        default={"value": 10, "unit": "row"},
        hard={"value": 100, "unit": "row"},
    )
    test_data_limits_xml = (
        f"<DataLimits {TAPREGEXT_NAMESPACE_HEADER}>"
        '<default unit="row">10</default>'
        '<hard unit="row">100</hard>'
        "</DataLimits>"
    )

    def test_read_from_xml(self):
        """Test reading a DataLimits element from XML."""
        data_limits = DataLimits.from_xml(self.test_data_limits_xml)
        self.assertEqual(data_limits.default.value, 10)
        self.assertEqual(data_limits.hard.value, 100)

    def test_write_xml(self):
        """Test we can write a DataLimits element to XML."""
        test_xml = self.test_data_limits_model.to_xml(encoding=str, skip_empty=True)
        self.assertEqual(
            canonicalize(test_xml),
            canonicalize(self.test_data_limits_xml),
        )


class TestDataLimit(TestCase):
    """Tests the DataLimit model."""

    test_data_limit_model = DataLimit(value=10, unit="byte")
    test_data_limit_xml = f'<DataLimit {TAPREGEXT_NAMESPACE_HEADER} unit="byte">10</DataLimit>'

    def test_read_from_xml(self):
        """Test reading a DataLimit element from XML."""
        data_limit = DataLimit.from_xml(self.test_data_limit_xml)
        self.assertEqual(data_limit.value, 10)
        self.assertEqual(data_limit.unit, "byte")

    def test_write_xml(self):
        """Test we can write a DataLimit element to XML."""
        test_xml = self.test_data_limit_model.to_xml(encoding=str, skip_empty=True)
        self.assertEqual(
            canonicalize(test_xml),
            canonicalize(self.test_data_limit_xml),
        )


class TestLanguageFeatureList(TestCase):
    """Tests the LanguageFeatureList model."""

    test_language_feature_list_model = LanguageFeatureList(
        feature=[
            LanguageFeature(form="Formal notation", description="A description"),
            LanguageFeature(form="Informal notation", description="Another description"),
        ],
        type="adql-some-feature",
    )
    test_language_feature_list_xml = (
        f'<LanguageFeatureList {TAPREGEXT_NAMESPACE_HEADER} type="adql-some-feature">'
        "<feature><form>Formal notation</form><description>A description</description></feature>"
        "<feature><form>Informal notation</form><description>Another description</description></feature>"
        "</LanguageFeatureList>"
    )

    def test_read_from_xml(self):
        """Test reading a LanguageFeatureList element from XML."""
        language_feature_list = LanguageFeatureList.from_xml(self.test_language_feature_list_xml)
        self.assertEqual(language_feature_list.feature[0].form, "Formal notation")
        self.assertEqual(language_feature_list.feature[0].description, "A description")
        self.assertEqual(language_feature_list.feature[1].form, "Informal notation")
        self.assertEqual(language_feature_list.feature[1].description, "Another description")

    def test_write_xml(self):
        """Test we can write a LanguageFeatureList element to XML."""
        test_xml = self.test_language_feature_list_model.to_xml(encoding=str, skip_empty=True)
        self.assertEqual(
            canonicalize(test_xml),
            canonicalize(self.test_language_feature_list_xml),
        )


class TestLanguage(TestCase):
    """Tests the Language model."""

    test_language_model = Language(
        name="ADQL",
        version=[Version(value="2.0", ivo_id="ivo://ivoa.net/std/ADQL")],
        description="Astronomical Data Query Language",
        language_features=[
            LanguageFeatureList(
                feature=[
                    LanguageFeature(form="Formal notation", description="A description"),
                    LanguageFeature(form="Informal notation", description="Another description"),
                ],
                type="adql-some-feature",
            )
        ],
    )
    test_language_xml = (
        f"<Language {TAPREGEXT_NAMESPACE_HEADER}>"
        "<name>ADQL</name>"
        "<version ivo-id='ivo://ivoa.net/std/ADQL'>2.0</version>"
        "<description>Astronomical Data Query Language</description>"
        '<languageFeatures type="adql-some-feature">'
        "<feature><form>Formal notation</form><description>A description</description></feature>"
        "<feature><form>Informal notation</form><description>Another description</description></feature>"
        "</languageFeatures>"
        "</Language>"
    )

    def test_read_from_xml(self):
        """Test reading a Language element from XML."""
        language = Language.from_xml(self.test_language_xml)
        self.assertEqual(language.name, "ADQL")
        self.assertEqual(language.version[0].value, "2.0")
        self.assertEqual(language.description, "Astronomical Data Query Language")
        self.assertEqual(language.language_features[0].feature[0].form, "Formal notation")
        self.assertEqual(language.language_features[0].feature[0].description, "A description")
        self.assertEqual(language.language_features[0].feature[1].form, "Informal notation")
        self.assertEqual(language.language_features[0].feature[1].description, "Another description")

    def test_write_xml(self):
        """Test we can write a Language element to XML."""
        test_xml = self.test_language_model.to_xml(encoding=str, skip_empty=True)
        self.assertEqual(
            canonicalize(test_xml),
            canonicalize(self.test_language_xml),
        )


class TestTableAccess(TestCase):
    """Tests the TableAccess model."""

    test_table_access_model = TableAccess(
        data_model=[DataModelType(value="VOTable", ivo_id="ivo://ivoa.net/std/VOTable")],
        language=[
            Language(
                name="ADQL",
                version=[Version(value="2.0", ivo_id="ivo://ivoa.net/std/ADQL-2.0")],
                description="Astronomical Data Query Language",
                language_features=[
                    LanguageFeatureList(
                        feature=[
                            LanguageFeature(form="Formal notation", description="A description"),
                            LanguageFeature(form="Informal notation", description="Another description"),
                        ],
                        type="adql-some-feature",
                    )
                ],
            )
        ],
        output_format=[
            OutputFormat(
                mime="application/x-votable+xml",
                alias=["VOTABLE"],
            )
        ],
        retention_period=TimeLimits(default=10, hard=100),
        output_limit=DataLimits(
            default={"value": 10, "unit": "row"},
            hard={"value": 100, "unit": "row"},
        ),
    )
    test_table_access_xml = (
        f'<capability {TAPREGEXT_NAMESPACE_HEADER} standardID="ivo://ivoa.net/std/TAP">'
        "<dataModel ivo-id='ivo://ivoa.net/std/VOTable'>VOTable</dataModel>"
        "<language>"
        "<name>ADQL</name>"
        '<version ivo-id="ivo://ivoa.net/std/ADQL-2.0">2.0</version>'
        "<description>Astronomical Data Query Language</description>"
        '<languageFeatures type="adql-some-feature">'
        "<feature><form>Formal notation</form><description>A description</description></feature>"
        "<feature><form>Informal notation</form><description>Another description</description></feature>"
        "</languageFeatures>"
        "</language>"
        "<outputFormat><mime>application/x-votable+xml</mime><alias>VOTABLE</alias></outputFormat>"
        "<retentionPeriod><default>10</default><hard>100</hard></retentionPeriod>"
        "<outputLimit>"
        '<default unit="row">10</default>'
        '<hard unit="row">100</hard>'
        "</outputLimit>"
        "</capability>"
    )

    def test_read_from_xml(self):
        """Test reading a TableAccess element from XML."""
        table_access = TableAccess.from_xml(self.test_table_access_xml)
        self.assertEqual(table_access.data_model[0].value, "VOTable")
        self.assertEqual(table_access.data_model[0].ivo_id, "ivo://ivoa.net/std/VOTable")
        self.assertEqual(table_access.language[0].name, "ADQL")
        self.assertEqual(table_access.language[0].version[0].value, "2.0")
        self.assertEqual(table_access.language[0].description, "Astronomical Data Query Language")
        self.assertEqual(table_access.language[0].language_features[0].feature[0].form, "Formal notation")
        self.assertEqual(table_access.language[0].language_features[0].feature[0].description, "A description")
        self.assertEqual(table_access.language[0].language_features[0].feature[1].form, "Informal notation")
        self.assertEqual(table_access.language[0].language_features[0].feature[1].description, "Another description")
        self.assertEqual(table_access.output_format[0].mime, "application/x-votable+xml")
        self.assertEqual(table_access.output_format[0].alias[0], "VOTABLE")
        self.assertEqual(table_access.retention_period.default, 10)
        self.assertEqual(table_access.retention_period.hard, 100)
        self.assertEqual(table_access.output_limit.default.value, 10)
        self.assertEqual(table_access.output_limit.hard.value, 100)

    def test_write_xml(self):
        """Test we can write a TableAccess element to XML."""
        test_xml = self.test_table_access_model.to_xml(encoding=str, skip_empty=True)
        self.assertEqual(
            canonicalize(test_xml),
            canonicalize(self.test_table_access_xml),
        )
