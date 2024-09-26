"""Snippets for TAPRegExt models and XML serialization."""
from vo_models.tapregext.models import (
    DataLimits,
    DataModelType,
    Language,
    LanguageFeature,
    LanguageFeatureList,
    OutputFormat,
    TableAccess,
    TimeLimits,
    Version,
)

# pylint: disable=invalid-name

# [TableAccess-model-start]
table_access_model = TableAccess(
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
# [TableAccess-model-end]

# [TableAccess-xml-start]
table_access_xml = """
<capability standardID="ivo://ivoa.net/std/TAP">
        <dataModel ivo-id='ivo://ivoa.net/std/VOTable'>VOTable</dataModel>
        <language>
                <name>ADQL</name>
                <version ivo-id="ivo://ivoa.net/std/ADQL-2.0">2.0</version>
                <description>Astronomical Data Query Language</description>
                <languageFeatures type="adql-some-feature">
                        <feature>
                                <form>Formal notation</form>
                                <description>A description</description>
                        </feature>
                        <feature>
                                <form>Informal notation</form>
                                <description>Another description</description>
                        </feature>
                </languageFeatures>
        </language>
        <outputFormat>
                <mime>application/x-votable+xml</mime>
                <alias>VOTABLE</alias>
        </outputFormat>
        <retentionPeriod>
                <default>10</default>
                <hard>100</hard>
        </retentionPeriod>
        <outputLimit>
                <default unit="row">10</default>
                <hard unit="row">100</hard>
        </outputLimit>
</capability>
"""  # [TableAccess-xml-end]
