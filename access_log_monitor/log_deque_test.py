from freezegun import freeze_time

from .log_deque import LogDeque
from .log_utils import now_utc


@freeze_time("2018-01-10 3pm", tick=True)
def test_peek_returns_all_entries_since_given_time():
    entries = [
        (now_utc(hour=11), "a few hours ago"),
        (now_utc(day=5), "a few days ago"),
        (now_utc(year=2010), "8 years ago"),
        (now_utc(year=2000), "18 years ago"),
    ]
    recents = LogDeque(entries).peek(since_time=now_utc(year=2012))
    assert recents == ["a few hours ago", "a few days ago"]


@freeze_time("2018-01-10 3pm", tick=True)
def test_peek_returns_empty_list_if_no_entries_match():
    entries = [
        (now_utc(hour=11), "a few hours ago"),
        (now_utc(day=5), "a few days ago"),
        (now_utc(year=2010), "8 years ago"),
        (now_utc(year=2000), "18 years ago"),
    ]
    recents = LogDeque(entries).peek(since_time=now_utc())
    assert recents == []


def test_add_inserts_in_descending_chrono_order_when_inserted_in_desc_order():
    store = (LogDeque()
             .add(now_utc(hour=11), "hours ago")
             .add(now_utc(day=5), "days ago")
             .add(now_utc(year=2010), "years ago")
             .add(now_utc(year=1990), "decades ago"))  # yapf: disable

    actual_ordering = [entry for time, entry in store]
    expected_ordering = ["hours ago", "days ago", "years ago", "decades ago"]
    assert actual_ordering == expected_ordering


def test_add_inserts_in_descending_chrono_order_when_inserted_in_asc_order():
    store = (LogDeque()
             .add(now_utc(year=1990), "decades ago")
             .add(now_utc(year=2010), "years ago")
             .add(now_utc(day=5), "days ago")
             .add(now_utc(hour=11), "hours ago"))  # yapf: disable

    actual_ordering = [entry for time, entry in store]
    expected_ordering = ["hours ago", "days ago", "years ago", "decades ago"]
    assert actual_ordering == expected_ordering


def test_add_inserts_in_descending_chrono_order_when_inserted_in_mixed_order():
    store = (LogDeque()
             .add(now_utc(year=2010), "years ago")
             .add(now_utc(hour=11), "hours ago")
             .add(now_utc(year=1990), "decades ago")
             .add(now_utc(day=5), "days ago"))  # yapf: disable

    actual_ordering = [entry for time, entry in store]
    expected_ordering = ["hours ago", "days ago", "years ago", "decades ago"]
    assert actual_ordering == expected_ordering
