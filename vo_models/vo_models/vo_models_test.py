"""Tests for vo-tap models and datatypes"""
from unittest import TestCase

import xmldiff.actions
import xmldiff.main


class VOModelTestBase:
    """Base class for VO model tests.

    VO model test classes that inherit from VOModelTestCase should have the following attributes:

    - test_xml: A string containing the XML to be tested. Considered the ground truth.
    - test_element: An instance of the model to be tested. Compared to the XML.
    - base_model: The model class to be tested. Used to instantiate the model from XML.

    Extra tests can be added to the inheriting class as needed.
    """

    # pylint: disable=no-member

    class VOModelTestCase(TestCase):
        """Default tests for VO models.

        Automatically runs the following tests:
        - test_read_xml: Test reading XML into model and that all elements are present.
        - test_write_xml: Test writing model to XML and no elements are missing.

        These tests ensure that the model can be round-tripped from XML and back again without losing any data.
        """

        def test_read_xml(self):
            """Test reading XML into model and that all elements are present.

            Compares the model created from the XML and ensures it matches the test element.
            """

            test_model = self.base_model.from_xml(self.test_xml)
            self.assertIsInstance(test_model, self.base_model)
            self.assertEqual(test_model, self.test_element)

        def test_write_xml(self):
            """Test writing model to XML.

            Compares the XML created from the model and ensures it matches the test XML.
            """
            xml = self.test_element.to_xml(skip_empty=True, encoding=str)
            assert_equal_xml(xml, self.test_xml)


def assert_equal_xml(xml1: bytes | str, xml2: bytes | str, skip_empty=True, skip_defaults=True):
    """Test whether two xml strings are equal, skipping empty elements and default attributes

    Args:
        xml1 (bytes | str): XML string to compare
        xml2 (bytes | str): XML string to compare
        skip_empty (bool, optional): Whether to skip the deletion of empty elements. Defaults to True.
        skip_defaults (bool, optional): Whether to skip the addition of default attributes. Defaults to True.
    """
    diffs = xmldiff.main.diff_texts(xml1, xml2, diff_options={"fast_match": True})

    if diffs:
        for diff in diffs:
            if isinstance(diff, xmldiff.actions.DeleteNode):
                # Skip raising over the removal of empty elements. We do this by default.
                if not skip_empty:
                    raise AssertionError(f"XML strings are not equal: {diff}")
            elif isinstance(diff, xmldiff.actions.InsertAttrib):
                # Skip raising over the addition of default attributes. We do this to conform to the standard.
                if not skip_defaults:
                    raise AssertionError(f"XML strings are not equal: {diff}")
            else:
                raise AssertionError(f"XML strings are not equal: {diff}")
