from collections import deque
from datetime import datetime
from typing import Optional

from .log_line import LogLine


class LogDeque:
    """
    A data structure designed to hold log entries
    from newest to oldest in left-to-right fashion.

    Uses a deque for efficient inserting.
    """

    def __init__(self, entries: Optional[list] = None) -> None:
        self.entries: deque = deque(entries or [])

    def add(self, timestamp: datetime, entry: LogLine):
        """
        Add a log entry with timestamp `timestamp` to the LogDeque.
        Inserts in chronological order from latest to oldest.
        """
        if len(self.entries) == 0:
            self.entries.appendleft((timestamp, entry))
            return self

        i = 0
        curr_entry_time, _ = self.entries[0]
        while timestamp < curr_entry_time:
            i += 1
            if i > len(self.entries) - 1:
                break
            curr_entry_time, _ = self.entries[i]

        self.entries.insert(i, (timestamp, entry))
        return self

    def peek(self, since_time: datetime) -> list:
        """
        Return all entries added to the LogDeque since the given time
        `since_time`. Exploits the latest-to-oldest ordering of entries to
        avoid unnecessary iteration.
        """
        peeked_entries: deque = deque()

        for timestamp, entry in self.entries:
            entry_was_on_or_after_requested_time = since_time <= timestamp
            if entry_was_on_or_after_requested_time:
                peeked_entries.append(entry)
            else:
                break

        return list(peeked_entries)

    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        return iter(self.entries)
