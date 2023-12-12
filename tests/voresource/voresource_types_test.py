"""Tests for VOResource simple types"""
from unittest import TestCase

from vo_models.voresource.types import UTCTimestamp


class TestUTCTimestampModel(TestCase):
    """Test UTCTimestamp parsing"""

    def test_utctimestamp_parse(self):
        """Test that datetimes are parsed and output in correct format"""

        # Test allowed string formats
        good_vo_utc = "2023-03-15T18:27:18.758Z"

        # 2023-03-15T18:27:18.758 (No timezone - Z UTC assumed)
        vo_utc = UTCTimestamp.fromisoformat("2023-03-15T18:27:18.758")
        self.assertIsInstance(vo_utc, UTCTimestamp)
        self.assertEqual(vo_utc.isoformat(), good_vo_utc)

        # 2023-03-15T18:27:18.758Z (Zulu UTC - T separator)
        vo_utc = UTCTimestamp.fromisoformat("2023-03-15T18:27:18.758Z")
        self.assertIsInstance(vo_utc, UTCTimestamp)
        self.assertEqual(vo_utc.isoformat(), good_vo_utc)

        # 2023-03-15 18:27:18.758Z (Zulu UTC - space separator)
        vo_utc = UTCTimestamp.fromisoformat("2023-03-15 18:27:18.758Z")
        self.assertIsInstance(vo_utc, UTCTimestamp)
        self.assertEqual(vo_utc.isoformat(), good_vo_utc)

        # 2023-03-15T18:27:18.758+00:00 (UTC w/ offset - T separator)
        vo_utc = UTCTimestamp.fromisoformat("2023-03-15T18:27:18.758+00:00")
        self.assertIsInstance(vo_utc, UTCTimestamp)
        self.assertEqual(vo_utc.isoformat(), good_vo_utc)

        # 2023-03-15 18:27:18.758+00:00 (UTC w/ offset - space separator)
        vo_utc = UTCTimestamp.fromisoformat("2023-03-15 18:27:18.758+00:00")
        self.assertIsInstance(vo_utc, UTCTimestamp)
        self.assertEqual(vo_utc.isoformat(), good_vo_utc)

        # Test that we reject non-UTC datetimes
        with self.assertRaises(ValueError):
            # pylint: disable=protected-access
            UTCTimestamp._validate("20230315T18:27:18.758")
