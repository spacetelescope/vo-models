"""Tests for VOSI Capabilities models."""

from datetime import timezone as tz
from unittest import TestCase
from xml.etree.ElementTree import canonicalize

from lxml import etree

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
from vo_models.voresource.models import AccessURL, Capability, Interface, WebBrowser
from vo_models.vosi.capabilities.models import VOSICapabilities

CAPABILITIES_HEADER = """xmlns:vosi="http://www.ivoa.net/xml/VOSICapabilities/v1.0"
xmlns="http://www.ivoa.net/xml/VOResource/v1.0"
xmlns:vs="http://www.ivoa.net/xml/VODataService/v1.0"
xmlns:tr="http://www.ivoa.net/xml/TAPRegExt/v1.0"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
"""


class TestVOSICapabilities(TestCase):
    """Tests the VOSI Capabilities complex type.

    This test uses a simulated capabilities document for a TAP service.
    """

    test_capabilities_xml = f"""<vosi:capabilities {CAPABILITIES_HEADER}>
        <capability standardID="ivo://ivoa.net/std/TAP" xsi:type="tr:TableAccess">
            <interface role="std" xsi:type="vs:ParamHTTP" version="1.1">
                <accessURL use="full">https://someservice.edu/tap</accessURL>
            </interface>
            <language>
                <name>ADQL</name>
                <version ivo-id="ivo://ivoa.net/std/ADQL#v2.0">2.0</version>
                <description>
                    ADQL-2.0. Positional queries using CONTAINS with POINT, and CIRCLE are supported.
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
    """

    test_tap_capabilities = TableAccess(
        type="tr:TableAccess",
        interface=[
            Interface(
                role="std",
                type="vs:ParamHTTP",
                version="1.1",
                access_url=[AccessURL(use="full", value="https://someservice.edu/tap")],
            )
        ],
        language=[
            Language(
                name="ADQL",
                version=[Version(value="2.0", ivo_id="ivo://ivoa.net/std/ADQL#v2.0")],
                description="ADQL-2.0. Positional queries using CONTAINS with POINT, CIRCLE, BOX, and POLYGON are supported.",
                language_features=[
                    LanguageFeatureList(
                        type="ivo://ivoa.net/std/TAPRegExt#features-adql-geo",
                        feature=[
                            LanguageFeature(form="POINT"),
                            LanguageFeature(form="CIRCLE"),
                            LanguageFeature(form="BOX"),
                            LanguageFeature(form="POLYGON"),
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
    )

    test_vosi_capabilities = Capability(
        standard_id="ivo://ivoa.net/std/VOSI#capabilities",
        interface=[
            Interface(
                type="vs:ParamHTTP",
                role="std",
                access_url=[AccessURL(use="full", value="https://someservice.edu/tap/capabilities")],
            )
        ],
    )
    test_vosi_availability = Capability(
        standard_id="ivo://ivoa.net/std/VOSI#availability",
        interface=[
            Interface(
                type="vs:ParamHTTP",
                role="std",
                access_url=[AccessURL(use="full", value="https://someservice.edu/tap/availability")],
            )
        ],
    )
    test_vosi_tables = Capability(
        standard_id="ivo://ivoa.net/std/VOSI#tables",
        interface=[
            Interface(
                type="vs:ParamHTTP",
                role="std",
                version="1.1",
                access_url=[AccessURL(use="full", value="https://someservice.edu/tap/tables")],
            )
        ],
    )
    test_dali_examples = Capability(
        standard_id="ivo://ivoa.net/std/DALI#examples",
        interface=[
            WebBrowser(
                access_url=[AccessURL(use="full", value="https://someservice.edu/tap/examples")],
            )
        ],
    )
    test_vosi_capabilities_model = VOSICapabilities(
        capability=[
            test_tap_capabilities,
            test_vosi_capabilities,
            test_vosi_availability,
            test_vosi_tables,
            test_dali_examples,
        ]
    )

    def _get_capability(self, capabilities: VOSICapabilities, standard_id: str) -> Capability:
        """Get a capability from the test capabilities."""
        for cap in capabilities.capability:
            if str(cap.standard_id) == standard_id:
                return cap
        return None

    def test_read_from_xml(self):
        """Test reading VOSI Capabilities from XML."""
        capabilities = VOSICapabilities.from_xml(self.test_capabilities_xml)

        self.assertEqual(len(capabilities.capability), 5)

        # Check the TAP capability
        tap_capability: TableAccess = self._get_capability(capabilities, "ivo://ivoa.net/std/TAP")
        self.assertIsNotNone(tap_capability)
        self.assertEqual(tap_capability, self.test_tap_capabilities)
        self.assertEqual(len(tap_capability.interface), 1)
        self.assertIsNotNone(tap_capability.output_limit)
        self.assertEqual(len(tap_capability.language), 1)

        # Check the VOSI capabilities
        vosi_capabilities = self._get_capability(capabilities, "ivo://ivoa.net/std/VOSI#capabilities")
        self.assertIsNotNone(vosi_capabilities)
        self.assertEqual(vosi_capabilities, self.test_vosi_capabilities)

        # Check the VOSI availability
        vosi_availability = self._get_capability(capabilities, "ivo://ivoa.net/std/VOSI#availability")
        self.assertIsNotNone(vosi_availability)
        self.assertEqual(vosi_availability, self.test_vosi_availability)

        # Check the VOSI tables
        vosi_tables = self._get_capability(capabilities, "ivo://ivoa.net/std/VOSI#tables")
        self.assertIsNotNone(vosi_tables)
        self.assertEqual(vosi_tables, self.test_vosi_tables)

        # Check the DALI examples
        dali_examples = self._get_capability(capabilities, "ivo://ivoa.net/std/DALI#examples")
        self.assertIsNotNone(dali_examples)
        self.assertEqual(dali_examples, self.test_dali_examples)

    def test_write_to_xml(self):
        """Test writing VOSI Capabilities to XML."""
        test_xml = self.test_vosi_capabilities_model.to_xml(encoding=str, skip_empty=True)
        self.assertEqual(
            canonicalize(test_xml, strip_text=True),
            canonicalize(self.test_capabilities_xml, strip_text=True),
        )
