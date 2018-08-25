import io
from collections import namedtuple
from datetime import timedelta
from inspect import cleandoc

from freezegun import freeze_time

from . import log_utils


def test_read_last_line_returns_the_last_line_as_string(mocker):
    text = """
    1 line
    2 line
    3 line\0
    """
    mocker.patch("builtins.open", return_value=io.StringIO(cleandoc(text)))
    last_line = log_utils.read_last_line(filename="")
    assert last_line == "3 line"


def test_read_last_line_fails_with_empty_string(mocker):
    mocker.patch("builtins.open", return_value=io.StringIO())
    last_line = log_utils.read_last_line(filename="")
    assert last_line == ""


def test_most_common_by_counts_by_given_callable_result():
    num = namedtuple("num", "n parity is_prime")
    collection = (
        num(n=1, parity="odd", is_prime=False),
        num(n=2, parity="even", is_prime=True),
        num(n=4, parity="even", is_prime=False),
        num(n=6, parity="even", is_prime=False),
    )
    result = log_utils.most_common_by(lambda e: e.parity, collection)
    assert result == dict(value="even", count=3)

    result = log_utils.most_common_by(lambda e: e.is_prime, collection)
    assert result == dict(value=False, count=3)


def test_most_common_by_returns_first_by_insertion_if_ordered_and_no_winner():
    num = namedtuple("num", "n")
    collection = [num(n=1), num(n=2), num(n=4), num(n=6)]
    result = log_utils.most_common_by(lambda e: e.n, collection)
    assert result == dict(value=1, count=1)


def test_percent_computes_percents_correctly_by_predicate():
    collection = [1, 1, 2, 2, 5]
    assert log_utils.percent(lambda e: e == 1, collection) == 40.0
    assert log_utils.percent(lambda e: e == 2, collection) == 40.0
    assert log_utils.percent(lambda e: e == 5, collection) == 20.0
    assert log_utils.percent(lambda e: e == 6, collection) == 0.0


@freeze_time("2018-04-02 12:33:40.10pm", tz_offset=0)
def test_now_utc_abbreviates_microseconds():
    assert str(log_utils.now_utc()) == "2018-04-02 12:33:40+00:00"


@freeze_time("2018-04-02 12:33:40.10pm", tz_offset=0)
def test_now_utc_sets_values_with_kwargs():
    actual_time = log_utils.now_utc(month=1, day=3, hour=8, minute=5, second=1)
    assert str(actual_time) == "2018-01-03 08:05:01+00:00"


@freeze_time("5pm", tz_offset=0)
def test_is_interval_complete_returns_false_if_not():
    one_hr_ago = log_utils.now_utc(hour=16)
    two_hrs_delta = timedelta(hours=2)

    result = log_utils.is_interval_complete(
        start_time=one_hr_ago, delta=two_hrs_delta)

    assert result is False


@freeze_time("5pm", tz_offset=0)
def test_is_interval_complete_returns_true_if_it_is():
    two_hrs_ago = log_utils.now_utc(hour=15)
    one_hr_delta = timedelta(hours=1)

    result = log_utils.is_interval_complete(
        start_time=two_hrs_ago, delta=one_hr_delta)

    assert result is True
