import abc
from datetime import datetime
from typing import Optional

from .log_deque import LogDeque
from .log_line import LogLine


class LogStore(metaclass=abc.ABCMeta):
    """
    Abstract base class for classes that abstract away the implementation
    details of working with particular data stores.

    Example possible subclasses:
    - DataFrameDataStore
    - DataTensorDataStore
    - SqliteDataStore
    - PostgresDataStore
    - BitmapDataStore
    """

    @abc.abstractmethod
    def add(self, entry: Optional[LogLine]) -> None:
        pass

    @abc.abstractmethod
    def peek(self, since: datetime) -> list:
        pass


class DequeDataStore(LogStore):
    """
    An in-memory DataStore the uses a LogDeque.
    """

    def __init__(self):
        self.datastore = LogDeque()

    def add(self, entry: Optional[LogLine]):
        """
        Adds an entry. If the given `entry` is falsy, no-ops.
        Otherwise parses the timestamp for the LogLine instance using
        datetime.strptime and adds the model to the datastore.
        """
        if not isinstance(entry, LogLine):
            return self

        timestamp = datetime.strptime(entry.timestamp, entry.timestamp_format)
        self.datastore.add(timestamp, entry)

        return self

    def peek(self, since: datetime) -> list:
        "Delegates to the underlying datastore."
        return self.datastore.peek(since)
