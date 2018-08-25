from collections import namedtuple

from freezegun import freeze_time

from .log_analyzer import LogAnalyzer
from .log_utils import now_utc


def test_requests_per_second_returns_zero_if_interval_too_short():
    avg_reqs_per_sec = LogAnalyzer().requests_per_second(
        since=now_utc(), current_time=now_utc())
    assert avg_reqs_per_sec == 0


@freeze_time("11am")
def test_requests_per_second_returns_zero_if_no_hits_over_interval():
    avg_reqs_per_sec = LogAnalyzer().requests_per_second(since=now_utc(hour=9))
    assert avg_reqs_per_sec == 0


@freeze_time("11:30:59")
def test_requests_per_second_returns_value_rounded_to_tenths_place(mocker):
    fakestore = namedtuple("fakestore", "peek")
    analyzer = LogAnalyzer(fakestore)
    one_minute_ago = now_utc(second=0)

    log_entries = list(range(120))
    mocker.patch.object(fakestore, "peek", return_value=log_entries)
    avg_reqs_per_sec = analyzer.requests_per_second(since=one_minute_ago)
    assert avg_reqs_per_sec == 2.0

    log_entries = list(range(90))
    mocker.patch.object(fakestore, "peek", return_value=log_entries)
    avg_reqs_per_sec = analyzer.requests_per_second(since=one_minute_ago)
    assert avg_reqs_per_sec == 1.5

    log_entries = list(range(60))
    mocker.patch.object(fakestore, "peek", return_value=log_entries)
    avg_reqs_per_sec = analyzer.requests_per_second(since=one_minute_ago)
    assert avg_reqs_per_sec == 1.0

    log_entries = list(range(30))
    mocker.patch.object(fakestore, "peek", return_value=log_entries)
    avg_reqs_per_sec = analyzer.requests_per_second(since=one_minute_ago)
    assert avg_reqs_per_sec == 0.5
