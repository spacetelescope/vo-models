"""Tests for VOResource simple types"""
from datetime import datetime, timedelta, timezone
from unittest import TestCase

from pydantic import BaseModel

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

    def test_utctimestamp_offsets(self):
        """Test that non-UTC offsets are converted to UTC instead of being dropped"""

        offset_cases = {
            "2023-03-15T18:27:18.758+05:00": "2023-03-15T13:27:18.758Z",
            "2023-03-15T18:27:18.758-05:00": "2023-03-15T23:27:18.758Z",
            "2023-03-15 18:27:18.758-05:00": "2023-03-15T23:27:18.758Z",
            # Offsets can move the date as well
            "2023-03-15T22:00:00.000-05:30": "2023-03-16T03:30:00.000Z",
        }

        for value, expected in offset_cases.items():
            with self.subTest(value=value):
                vo_utc = UTCTimestamp.fromisoformat(value)
                self.assertIsInstance(vo_utc, UTCTimestamp)
                self.assertEqual(vo_utc.isoformat(), expected)

    def test_utctimestamp_from_datetime(self):
        """Test that naive and aware datetimes are accepted and converted to UTC"""

        naive = datetime(2023, 3, 15, 18, 27, 18, 758000)
        self.assertEqual(UTCTimestamp._validate(naive).isoformat(), "2023-03-15T18:27:18.758Z")

        for hours, expected in ((-5, "2023-03-15T23:27:18.758Z"), (5, "2023-03-15T13:27:18.758Z")):
            with self.subTest(hours=hours):
                aware = naive.replace(tzinfo=timezone(timedelta(hours=hours)))
                vo_utc = UTCTimestamp._validate(aware)
                self.assertIsInstance(vo_utc, UTCTimestamp)
                self.assertEqual(vo_utc.isoformat(), expected)
                self.assertEqual(vo_utc, aware)

    def test_utctimestamp_pydantic_offsets(self):
        """Test that offsets are converted when validated through a pydantic model"""

        class Model(BaseModel):
            """Model with a UTCTimestamp field"""

            timestamp: UTCTimestamp

        for value, expected in (
            ("2023-03-15T18:27:18.758Z", "2023-03-15T18:27:18.758Z"),
            ("2023-03-15T18:27:18.758+05:00", "2023-03-15T13:27:18.758Z"),
            ("2023-03-15T18:27:18.758-05:00", "2023-03-15T23:27:18.758Z"),
            (
                datetime(2023, 3, 15, 18, 27, 18, 758000, tzinfo=timezone(timedelta(hours=-5))),
                "2023-03-15T23:27:18.758Z",
            ),
        ):
            with self.subTest(value=value):
                model = Model(timestamp=value)
                self.assertIsInstance(model.timestamp, UTCTimestamp)
                self.assertEqual(model.model_dump()["timestamp"], expected)
