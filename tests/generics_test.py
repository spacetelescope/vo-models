"""Tests for generic VO xml models"""
from unittest import TestCase
from xml.etree.ElementTree import canonicalize

from vo.models.xml.generics import NillElement, VODateTime


class TestVODatetimeModel(TestCase):
    """Test VODatetime parsing"""

    def test_vodatetime_parse(self):
        """Test that datetimes are parsed and output in correct format"""

        # Test allowed string formats
        good_vo_dt = "2023-03-15T18:27:18.758Z"

        # 2023-03-15T18:27:18.758 (No timezone - Z UTC assumed)
        vo_dt = VODateTime.fromisoformat("2023-03-15T18:27:18.758")
        self.assertIsInstance(vo_dt, VODateTime)
        self.assertEqual(vo_dt.isoformat(), good_vo_dt)

        # 2023-03-15T18:27:18.758Z (Zulu UTC - T separator)
        vo_dt = VODateTime.fromisoformat("2023-03-15T18:27:18.758Z")
        self.assertIsInstance(vo_dt, VODateTime)
        self.assertEqual(vo_dt.isoformat(), good_vo_dt)

        # 2023-03-15 18:27:18.758Z (Zulu UTC - space separator)
        vo_dt = VODateTime.fromisoformat("2023-03-15 18:27:18.758Z")
        self.assertIsInstance(vo_dt, VODateTime)
        self.assertEqual(vo_dt.isoformat(), good_vo_dt)

        # 2023-03-15T18:27:18.758+00:00 (UTC w/ offset - T separator)
        vo_dt = VODateTime.fromisoformat("2023-03-15T18:27:18.758+00:00")
        self.assertIsInstance(vo_dt, VODateTime)
        self.assertEqual(vo_dt.isoformat(), good_vo_dt)

        # 2023-03-15 18:27:18.758+00:00 (UTC w/ offset - space separator)
        vo_dt = VODateTime.fromisoformat("2023-03-15 18:27:18.758+00:00")
        self.assertIsInstance(vo_dt, VODateTime)
        self.assertEqual(vo_dt.isoformat(), good_vo_dt)

        # Test that we reject non-UTC datetimes
        with self.assertRaises(ValueError):
            VODateTime.validate("20230315T18:27:18.758")


class TestNillElement(TestCase):
    """Test NillElement parsing"""

    nil_xml = (
        """<NillElement xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"></NillElement>"""
    )
    non_nil_xml = (
        """<NillElement xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">test_val</NillElement>"""
    )

    def test_to_xml(self):
        """Test generating XML from NillElement"""

        test_element = NillElement(value="test_val")
        test_xml = test_element.to_xml(encoding=str)

        self.assertEqual(canonicalize(test_xml, strip_text=True), canonicalize(self.non_nil_xml, strip_text=True))

        test_element = NillElement(value=None)
        test_xml = test_element.to_xml(encoding=str)

        self.assertEqual(canonicalize(test_xml, strip_text=True), canonicalize(self.nil_xml, strip_text=True))


    def test_from_xml(self):
        """Test reading a NillElement from XML"""

        # Element with a value defined
        test_element = NillElement.from_xml(self.non_nil_xml)

        assert isinstance(test_element, NillElement)
        assert test_element.value == "test_val"
        assert test_element.nil is None

        # Test we can round-trip back to XML
        test_xml = test_element.to_xml(encoding=str)

        self.assertEqual(canonicalize(test_xml, strip_text=True), canonicalize(self.non_nil_xml, strip_text=True))

        # Element without a value defined
        test_element = NillElement.from_xml(self.nil_xml)

        assert isinstance(test_element, NillElement)
        assert test_element.value is None
        assert test_element.nil == "true"

        test_xml = test_element.to_xml(encoding=str)

        self.assertEqual(canonicalize(test_xml, strip_text=True), canonicalize(self.nil_xml, strip_text=True))
