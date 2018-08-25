import os
from typing import Optional

from . import log_utils
from .log_line import LogLine


class LogManager:
    """
    Models the log file at the given path.
    The path is overridable. Maintains the time of the most recent update.
    """

    def __init__(self, path: str) -> None:
        self.path = path
        self.mru_time = self.last_updated_at

    @property
    def last_entry(self) -> Optional[LogLine]:
        """Return the last entry from the log at `self.path`."""
        line = log_utils.read_last_line(self.path)
        return LogLine.from_log_line(line)

    @property
    def last_updated_at(self) -> float:
        return round(os.stat(self.path).st_mtime, 4)

    @property
    def has_been_updated(self) -> bool:
        """
        If the target log file has been updated since the last time it was
        checked, record the new most-recent-update time and return True. Else
        return False.
        """
        last_update = self.last_updated_at

        if last_update > self.mru_time:
            self.mru_time = last_update
            return True

        return False
