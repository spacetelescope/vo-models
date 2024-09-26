"""Example snippets for VOSI capabilities."""

from vo_models.tapregext.models import (
    DataLimit,
    DataLimits,
    Language,
    LanguageFeature,
    LanguageFeatureList,
    OutputFormat,
    TableAccess,
    Version,
)
from vo_models.vodataservice.models import ParamHTTP
from vo_models.voresource.models import AccessURL, Capability, WebBrowser
from vo_models.vosi.capabilities.models import VOSICapabilities

# pylint: disable=invalid-name

# [capabilities-model-start]
vosi_capabilities_model = VOSICapabilities(
    capability=[
        TableAccess(
            type="tr:TableAccess",
            interface=[
                ParamHTTP(
                    role="std",
                    version="1.1",
                    access_url=[AccessURL(use="full", value="https://someservice.edu/tap")],
                )
            ],
            language=[
                Language(
                    name="ADQL",
                    version=[Version(value="2.0", ivo_id="ivo://ivoa.net/std/ADQL#v2.0")],
                    description="ADQL-2.0. Positional queries using CONTAINS with POINT and CIRCLE are supported.",
                    language_features=[
                        LanguageFeatureList(
                            type="ivo://ivoa.net/std/TAPRegExt#features-adql-geo",
                            feature=[
                                LanguageFeature(form="POINT"),
                                LanguageFeature(form="CIRCLE"),
                            ],
                        ),
                    ],
                )
            ],
            output_format=[
                OutputFormat(
                    mime="application/x-votable+xml",
                    alias=["votable"],
                    ivo_id="ivo://ivoa.net/std/TAPRegExt#output-votable-td",
                ),
                OutputFormat(
                    mime="text/csv;header=present",
                    alias=["csv"],
                ),
            ],
            output_limit=DataLimits(
                default=DataLimit(unit="row", value=100000),
                hard=DataLimit(unit="row", value=100000),
            ),
        ),
        Capability(
            standard_id="ivo://ivoa.net/std/VOSI#capabilities",
            interface=[
                ParamHTTP(
                    role="std",
                    access_url=[AccessURL(use="full", value="https://someservice.edu/tap/capabilities")],
                )
            ],
        ),
        Capability(
            standard_id="ivo://ivoa.net/std/VOSI#availability",
            interface=[
                ParamHTTP(
                    role="std",
                    access_url=[AccessURL(use="full", value="https://someservice.edu/tap/availability")],
                )
            ],
        ),
        Capability(
            standard_id="ivo://ivoa.net/std/VOSI#tables",
            interface=[
                ParamHTTP(
                    role="std",
                    version="1.1",
                    access_url=[AccessURL(use="full", value="https://someservice.edu/tap/tables")],
                )
            ],
        ),
        Capability(
            standard_id="ivo://ivoa.net/std/DALI#examples",
            interface=[
                WebBrowser(
                    access_url=[AccessURL(use="full", value="https://someservice.edu/tap/examples")],
                )
            ],
        ),
    ]
)
# [capabilities-model-end]

# [capabilities-xml-start]
capabilities_xml = """<vosi:capabilities>
        <capability standardID="ivo://ivoa.net/std/TAP" xsi:type="tr:TableAccess">
            <interface role="std" xsi:type="vs:ParamHTTP" version="1.1">
                <accessURL use="full">https://someservice.edu/tap</accessURL>
            </interface>
            <language>
                <name>ADQL</name>
                <version ivo-id="ivo://ivoa.net/std/ADQL#v2.0">2.0</version>
                <description>
                    ADQL-2.0. Positional queries using CONTAINS with POINT and CIRCLE are supported.
                </description>
                <languageFeatures type="ivo://ivoa.net/std/TAPRegExt#features-adql-geo">
                    <feature>
                        <form>POINT</form>
                    </feature>
                    <feature>
                        <form>CIRCLE</form>
                    </feature>
                </languageFeatures>
            </language>
            <outputFormat ivo-id="ivo://ivoa.net/std/TAPRegExt#output-votable-td">
                <mime>application/x-votable+xml</mime>
                <alias>votable</alias>
            </outputFormat>
            <outputFormat>
                <mime>text/csv;header=present</mime>
                <alias>csv</alias>
            </outputFormat>
            <outputLimit>
                <default unit="row">100000</default>
                <hard unit="row">100000</hard>
            </outputLimit>
        </capability>
        <capability standardID="ivo://ivoa.net/std/VOSI#capabilities">
            <interface xsi:type="vs:ParamHTTP" role="std">
                <accessURL use="full">
                    https://someservice.edu/tap/capabilities
    </accessURL>
            </interface>
        </capability>
        <capability standardID="ivo://ivoa.net/std/VOSI#availability">
            <interface xsi:type="vs:ParamHTTP" role="std">
                <accessURL use="full">
                    https://someservice.edu/tap/availability
    </accessURL>
            </interface>
        </capability>
        <capability standardID="ivo://ivoa.net/std/VOSI#tables">
            <interface xsi:type="vs:ParamHTTP" role="std" version="1.1">
                <accessURL use="full">
                    https://someservice.edu/tap/tables
    </accessURL>
            </interface>
        </capability>
        <capability standardID="ivo://ivoa.net/std/DALI#examples">
            <interface xsi:type="vr:WebBrowser">
                <accessURL use="full">
                    https://someservice.edu/tap/examples
    </accessURL>
            </interface>
        </capability>
    </vosi:capabilities>
"""  # [capabilities-xml-end]
