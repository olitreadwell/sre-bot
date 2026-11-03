"""Unit tests for modules/incident/utils.py.

Verifies convert_utc_datetime_to_tz() and convert_tz_datetime_to_utc() convert
between UTC and a named timezone correctly, including the default timezone
argument and the round trip between the two functions.
"""

from datetime import datetime

import pytest
import pytz

from modules.incident.utils import (
    convert_tz_datetime_to_utc,
    convert_utc_datetime_to_tz,
)


@pytest.mark.unit
def test_convert_utc_datetime_to_tz_uses_default_timezone() -> None:
    """With no tz argument, the result is in America/Montreal."""
    utc_time = datetime(2024, 1, 15, 17, 0, 0)

    result = convert_utc_datetime_to_tz(utc_time)

    assert result.tzinfo is not None
    assert result.tzinfo.zone == "America/Montreal"
    assert result.hour == 12  # UTC-5 in January (EST, no daylight saving)


@pytest.mark.unit
def test_convert_utc_datetime_to_tz_uses_given_timezone() -> None:
    """A tz argument converts to that timezone instead of the default."""
    utc_time = datetime(2024, 1, 15, 17, 0, 0)

    result = convert_utc_datetime_to_tz(utc_time, tz="Europe/London")

    assert result.tzinfo is not None
    assert result.tzinfo.zone == "Europe/London"
    assert result.hour == 17


@pytest.mark.unit
def test_convert_tz_datetime_to_utc_uses_default_timezone() -> None:
    """With no tz argument, the naive datetime is read as America/Montreal."""
    local_time = datetime(2024, 1, 15, 12, 0, 0)

    result = convert_tz_datetime_to_utc(local_time)

    assert result.tzinfo == pytz.utc
    assert result.hour == 17  # America/Montreal is UTC-5 in January


@pytest.mark.unit
def test_convert_tz_datetime_to_utc_uses_given_timezone() -> None:
    """A tz argument reads the naive datetime as that timezone instead."""
    local_time = datetime(2024, 1, 15, 17, 0, 0)

    result = convert_tz_datetime_to_utc(local_time, tz="Europe/London")

    assert result.tzinfo == pytz.utc
    assert result.hour == 17


@pytest.mark.unit
def test_convert_functions_round_trip() -> None:
    """Converting UTC to a timezone and back returns the original instant."""
    utc_time = datetime(2024, 6, 1, 9, 30, 0)

    local_time = convert_utc_datetime_to_tz(utc_time, tz="America/Montreal")
    back_to_utc = convert_tz_datetime_to_utc(local_time.replace(tzinfo=None), tz="America/Montreal")

    assert back_to_utc.replace(tzinfo=None) == utc_time
