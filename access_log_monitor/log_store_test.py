from datetime import datetime

from .log_line import LogLine
from .log_store import DequeDataStore


def test_adding_non_loglines_is_a_no_op():
    store = DequeDataStore().add(None).add("").add(True).add(1)
    assert len(store.datastore) is 0
    assert list(store.datastore) == []


def test_adding_an_entry_parses_date():
    store = DequeDataStore()
    assert list(store.datastore) == []

    entry1 = LogLine(timestamp="2000-01 +0000", timestamp_format="%Y-%m %z")
    entry2 = LogLine(timestamp="1999-02 +0000", timestamp_format="%Y-%m %z")
    entry3 = LogLine(timestamp="1990-03 +0000", timestamp_format="%Y-%m %z")

    store.add(entry1).add(entry2).add(entry3)

    assert len(store.datastore) is 3
    assert all(isinstance(t, datetime) for t, e in store.datastore)
    assert all(isinstance(e, LogLine) for t, e in store.datastore)
    assert list(t.year for t, e in store.datastore) == [2000, 1999, 1990]
    assert list(t.month for t, e in store.datastore) == [1, 2, 3]
