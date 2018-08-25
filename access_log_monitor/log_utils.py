from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Collection, Dict

import tailer

BoolCollectionPredicate = Callable[[Any], bool]


def read_last_line(filename: str) -> str:
    """Read the last line of the log at `filename`."""
    with open(filename) as f:
        lines = tailer.tail(f, 1)
        if lines:
            return lines[0]
        return ""


def most_common_by(value_of: Callable,
                   collection: Collection) -> Dict[str, Any]:
    """
    Given the iterable collection `collection`, find the most commonly
    occurring entry, counting by the values returned by the given callable
    `value_of`.

    Return a dict of the form {"value": None, "count": 0}
    """
    section_and_count = {"value": None, "count": 0}
    section_counts = Counter(value_of(e) for e in collection)
    most_common_section = section_counts.most_common(1)

    if most_common_section:
        value, count = most_common_section[0]
        section_and_count["value"] = value
        section_and_count["count"] = count

    return section_and_count


def percent(predicate: BoolCollectionPredicate,
            collection: Collection) -> float:
    """
    For the given iterable collection, compute the percentage of entries for
    which `predicate` evaluates to True, rounded to one decimal point.
    """
    if not collection:
        return 0
    num_subset = sum(predicate(e) is True for e in collection)
    return round(100 * num_subset / len(collection), 1)


def now_utc(**kwargs) -> datetime:
    """
    Return a timezone-aware datetime object for the current time, assumed to be
    in UTC, abbreviated to seconds.

    The following kwargs are accepted and are used to override the actual
    current value: year, month, day, hour, minute, second.
    """
    acceptable_kwargs = {"year", "month", "day", "hour", "minute", "second"}
    datetime_values = {
        k: v
        for k, v in kwargs.items()
        if k in acceptable_kwargs
    }
    datetime_values['microsecond'] = 0
    return datetime.now(tz=timezone.utc).replace(**datetime_values)


def is_interval_complete(start_time: datetime,
                         delta: timedelta,
                         current_time: datetime = None) -> bool:
    """
    Return true if the `current_time` has passed the time interval delineated
    by `start_time` and `delta`, else False.
    """
    current_time = current_time or now_utc()
    current_delta = current_time - start_time
    return current_delta >= delta
